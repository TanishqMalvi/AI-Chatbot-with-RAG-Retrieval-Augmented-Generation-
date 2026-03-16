"""
Chat endpoint.

Implements the full RAG pipeline:
  query → input_guard → query_rewrite → retrieve+rerank → generate → output_guard → respond

Blueprint §15 (minimal flow order).
"""

from __future__ import annotations

import time
from typing import Any

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, status
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from app.audit.logger import audit_log
from app.auth.jwt_handler import UserContext, get_current_user
from app.config import get_settings
from app.generation.llm import get_llm
from app.generation.prompts import SYSTEM_PROMPT
from app.guardrails.input_guard import sanitize_input
from app.guardrails.output_guard import validate_output
from app.retrieval.query_rewriter import rewrite_query
from app.retrieval.retriever import retrieve_and_rerank

logger = structlog.get_logger(__name__)
settings = get_settings()

router = APIRouter()


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="User question")
    conversation_history: list[dict[str, str]] = Field(
        default_factory=list,
        description="Previous turns: [{'role': 'user'|'assistant', 'content': '...'}]",
    )
    query_rewrite_strategy: str = Field(
        default="hyde",
        description="Query rewriting strategy: none | hyde | multi_query | both",
    )


class SourceChunk(BaseModel):
    doc_id: str
    filename: str
    section: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    confidence: float
    latency_ms: float
    request_id: str
    guardrail_meta: dict[str, Any]


# ---------------------------------------------------------------------------
# Token endpoint (demo – generates a JWT for testing)
# ---------------------------------------------------------------------------


class TokenRequest(BaseModel):
    user_id: str
    roles: list[str] = ["all-employees"]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/token", response_model=TokenResponse, tags=["Auth"])
async def issue_token(body: TokenRequest) -> TokenResponse:
    """
    Issue a JWT for the given user_id and roles.
    **For development / testing only.** In production, integrate with your IdP.
    """
    from app.auth.jwt_handler import create_access_token

    token = create_access_token(subject=body.user_id, roles=body.roles)
    return TokenResponse(access_token=token)


# ---------------------------------------------------------------------------
# Main chat endpoint
# ---------------------------------------------------------------------------


@router.post("/chat", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    request: Request,
    user: UserContext = Depends(get_current_user),
) -> ChatResponse:
    """
    RAG chat endpoint.

    Full pipeline:
    1. Input guardrails (PII redaction, prompt injection)
    2. Query rewriting (HyDE / multi-query)
    3. Vector retrieval + ACL filtering
    4. Cross-encoder reranking
    5. LLM generation with source citations
    6. Output guardrails (confidence, hallucination check)
    """
    t0 = time.perf_counter()
    request_id = getattr(request.state, "request_id", "unknown")

    audit_log(
        "chat_request",
        user_id=user.user_id,
        details={"query_preview": body.query[:80], "roles": user.roles},
        request_id=request_id,
    )

    # ── Step 1: Input guardrails ──────────────────────────────────────────
    clean_query, pii_types, is_injection = sanitize_input(body.query)

    if is_injection:
        audit_log(
            "prompt_injection_blocked",
            user_id=user.user_id,
            details={"query_preview": body.query[:80]},
            request_id=request_id,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query contains potentially harmful content and cannot be processed.",
        )

    if pii_types:
        logger.info("pii_redacted", types=pii_types, user=user.user_id)

    # ── Step 2: Query rewriting ───────────────────────────────────────────
    try:
        rewritten_queries = await rewrite_query(
            clean_query,
            strategy=body.query_rewrite_strategy,
        )
    except Exception as exc:
        logger.warning("query_rewrite_failed", error=str(exc))
        rewritten_queries = [clean_query]

    # ── Step 3 & 4: Retrieve + rerank (use best rewritten query) ─────────
    primary_query = rewritten_queries[0]
    chunks = retrieve_and_rerank(
        query=primary_query,
        user_roles=user.roles,
        top_k=settings.retrieval_top_k,
        top_n=settings.rerank_top_n,
    )

    # ── Step 5: Build context + generate ─────────────────────────────────
    context_parts = []
    for i, chunk in enumerate(chunks[: settings.max_context_chunks], 1):
        filename = chunk.metadata.get("filename", chunk.metadata.get("doc_id", "unknown"))
        context_parts.append(f"[{i}] {filename}\n{chunk.chunk_text}")
    context = "\n\n---\n\n".join(context_parts)

    # Format conversation history
    history_parts = []
    for turn in body.conversation_history[-6:]:  # last 3 turns
        role = turn.get("role", "user")
        content = turn.get("content", "")
        history_parts.append(f"{role.upper()}: {content}")
    history = "\n".join(history_parts) if history_parts else "None"

    system_content = SYSTEM_PROMPT.format(context=context, history=history)
    messages = [
        SystemMessage(content=system_content),
        HumanMessage(content=clean_query),
    ]

    llm = get_llm()
    try:
        ai_message = await llm.ainvoke(messages)
        raw_answer = ai_message.content
    except Exception as exc:
        logger.error("llm_generation_failed", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Generation service temporarily unavailable.",
        ) from exc

    # ── Step 6: Output guardrails ─────────────────────────────────────────
    final_answer, guard_meta = await validate_output(raw_answer, chunks)

    latency_ms = (time.perf_counter() - t0) * 1000

    audit_log(
        "chat_response",
        user_id=user.user_id,
        details={
            "latency_ms": round(latency_ms, 1),
            "num_chunks": len(chunks),
            "confidence": guard_meta.get("confidence"),
            "hallucinated": guard_meta.get("hallucinated"),
            "pii_redacted": bool(pii_types),
        },
        request_id=request_id,
    )

    sources = [
        SourceChunk(
            doc_id=c.metadata.get("doc_id", ""),
            filename=c.metadata.get("filename", c.metadata.get("doc_id", "")),
            section=c.metadata.get("section", ""),
            score=round(c.score, 4),
        )
        for c in chunks
    ]

    return ChatResponse(
        answer=final_answer,
        sources=sources,
        confidence=guard_meta.get("confidence", 0.0),
        latency_ms=round(latency_ms, 1),
        request_id=request_id,
        guardrail_meta=guard_meta,
    )
