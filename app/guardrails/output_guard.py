"""
Output guardrails.

Blueprint §9:
- LLM-as-judge for hallucination detection.
- Source citation enforcement.
- Confidence scoring.
"""

from __future__ import annotations

import re

import structlog
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.config import get_settings
from app.generation.llm import get_llm
from app.retrieval.retriever import RetrievedChunk

logger = structlog.get_logger(__name__)
settings = get_settings()

# ---------------------------------------------------------------------------
# Source citation enforcement
# ---------------------------------------------------------------------------

_CITATION_RE = re.compile(r"\[Source:[^\]]+\]", re.IGNORECASE)


def has_citations(answer: str) -> bool:
    """Check whether the answer contains at least one source citation."""
    return bool(_CITATION_RE.search(answer))


def enforce_citations(answer: str, chunks: list[RetrievedChunk]) -> str:
    """
    If the answer lacks citations, append a list of sources used.
    This is the last-resort citation enforcement step.
    """
    if has_citations(answer):
        return answer

    sources = list(
        dict.fromkeys(
            c.metadata.get("filename", c.metadata.get("doc_id", "unknown"))
            for c in chunks
        )
    )
    if not sources:
        return answer

    source_list = "; ".join(f"[Source: {s}]" for s in sources)
    return f"{answer}\n\n*Sources: {source_list}*"


# ---------------------------------------------------------------------------
# Confidence scoring based on retrieval scores
# ---------------------------------------------------------------------------


def compute_confidence(chunks: list[RetrievedChunk]) -> float:
    """
    Estimate answer confidence from the top retrieved chunk scores.

    Returns a float in [0, 1].
    """
    if not chunks:
        return 0.0
    top_scores = [c.score for c in chunks[:3]]
    return sum(top_scores) / len(top_scores)


def is_low_confidence(chunks: list[RetrievedChunk]) -> bool:
    return compute_confidence(chunks) < settings.confidence_threshold


# ---------------------------------------------------------------------------
# LLM-as-judge hallucination check
# ---------------------------------------------------------------------------

_HALLUCINATION_JUDGE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a factuality judge. Given CONTEXT and an ANSWER, determine whether the "
            "answer contains any claims NOT supported by the context. "
            "Respond with a single word: SUPPORTED or UNSUPPORTED.",
        ),
        (
            "human",
            "CONTEXT:\n{context}\n\nANSWER:\n{answer}",
        ),
    ]
)


async def llm_hallucination_check(
    answer: str,
    chunks: list[RetrievedChunk],
) -> bool:
    """
    Use an LLM to judge whether the answer is grounded in the retrieved context.

    Returns True if the answer is hallucinated (UNSUPPORTED).
    """
    if not settings.enable_hallucination_check:
        return False

    context = "\n\n".join(c.chunk_text for c in chunks[:4])
    chain = _HALLUCINATION_JUDGE_PROMPT | get_llm() | StrOutputParser()

    try:
        verdict = await chain.ainvoke({"context": context, "answer": answer})
        is_hallucinated = "UNSUPPORTED" in verdict.upper()
        logger.info(
            "hallucination_check",
            verdict=verdict.strip(),
            is_hallucinated=is_hallucinated,
        )
        return is_hallucinated
    except Exception as exc:
        logger.warning("hallucination_check_failed", error=str(exc))
        return False  # fail open (prefer availability over over-refusal)


# ---------------------------------------------------------------------------
# Full output validation pipeline
# ---------------------------------------------------------------------------


async def validate_output(
    answer: str,
    chunks: list[RetrievedChunk],
) -> tuple[str, dict]:
    """
    Run all output guardrails and return (final_answer, validation_metadata).
    """
    from app.generation.prompts import LOW_CONFIDENCE_RESPONSE

    meta: dict = {
        "citations_present": has_citations(answer),
        "confidence": round(compute_confidence(chunks), 3),
        "low_confidence": is_low_confidence(chunks),
        "hallucinated": False,
    }

    if meta["low_confidence"]:
        logger.warning("low_confidence_answer", confidence=meta["confidence"])
        return LOW_CONFIDENCE_RESPONSE, meta

    # Enforce citations
    answer = enforce_citations(answer, chunks)
    meta["citations_present"] = True

    # Hallucination check (async, may be slow – skip in high-traffic scenarios)
    meta["hallucinated"] = await llm_hallucination_check(answer, chunks)
    if meta["hallucinated"]:
        logger.warning("hallucination_detected")
        return LOW_CONFIDENCE_RESPONSE, meta

    return answer, meta
