"""
Retrieval module: vector search + cross-encoder reranking.

Blueprint Â§6-7:
- Retrieve k=20 candidates via cosine similarity.
- Apply row-level ACL filter BEFORE retrieval.
- Rerank to top 5-8 with bge-reranker-large.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import structlog
from langchain_core.documents import Document

from app.config import get_settings
from app.vectordb.client import get_vector_store

logger = structlog.get_logger(__name__)
settings = get_settings()


@dataclass
class RetrievedChunk:
    chunk_id: str
    chunk_text: str
    score: float
    metadata: dict[str, Any]


def _build_acl_filter(user_roles: list[str]) -> dict[str, Any] | None:
    """
    Build a Chroma metadata filter that enforces row-level access control.
    A document is accessible if any of the user's roles appears in access_tags.
    The special tag "all-employees" grants access to everyone.
    """
    tags_to_check = list(set(user_roles + ["all-employees"]))
    if len(tags_to_check) <= 1:
        return {"access_tags": {"$in": tags_to_check}}
    # Build $or filter for each tag to enable row-level ACL filtering
    or_clauses = [{"access_tags": {"$in": [tag]}} for tag in tags_to_check]
    return {"$or": or_clauses}


@lru_cache(maxsize=1)
def _get_cross_encoder():
    """Load the cross-encoder reranker once and reuse it across requests."""
    from sentence_transformers import CrossEncoder  # type: ignore

    logger.info("loading_reranker_model", model=settings.reranker_model)
    return CrossEncoder(settings.reranker_model)


def _docs_to_chunks(docs: list[Document], scores: list[float] | None = None) -> list[RetrievedChunk]:
    result = []
    for i, doc in enumerate(docs):
        meta = doc.metadata or {}
        result.append(
            RetrievedChunk(
                chunk_id=meta.get("chunk_id", str(i)),
                chunk_text=doc.page_content,
                score=scores[i] if scores else 0.0,
                metadata=meta,
            )
        )
    return result


def retrieve(
    query: str,
    user_roles: list[str],
    top_k: int | None = None,
) -> list[RetrievedChunk]:
    """
    Perform vector similarity search with ACL pre-filtering.

    Returns up to top_k chunks ordered by similarity score.
    """
    k = top_k or settings.retrieval_top_k
    store = get_vector_store()
    acl_filter = _build_acl_filter(user_roles)

    logger.info(
        "vector_retrieval",
        query_preview=query[:80],
        user_roles=user_roles,
        top_k=k,
        acl_filter=str(acl_filter)[:120],
    )

    results: list[tuple[Document, float]] = store.similarity_search_with_relevance_scores(
        query,
        k=k,
        filter=acl_filter,
    )

    chunks = []
    for doc, score in results:
        meta = doc.metadata or {}
        chunks.append(
            RetrievedChunk(
                chunk_id=meta.get("chunk_id", ""),
                chunk_text=doc.page_content,
                score=score,
                metadata=meta,
            )
        )

    return chunks


def rerank(
    query: str,
    chunks: list[RetrievedChunk],
    top_n: int | None = None,
) -> list[RetrievedChunk]:
    """
    Rerank retrieved chunks using a cross-encoder model.

    Blueprint Â§7: bge-reranker-large cross-encoder.
    Falls back to score-sorted ordering if the model is unavailable.
    """
    n = top_n or settings.rerank_top_n
    if not chunks:
        return []

    try:
        logger.info("reranking", model=settings.reranker_model, candidates=len(chunks))
        cross_encoder = _get_cross_encoder()
        pairs = [(query, c.chunk_text) for c in chunks]
        scores = cross_encoder.predict(pairs).tolist()

        ranked = sorted(
            zip(chunks, scores),
            key=lambda x: x[1],
            reverse=True,
        )
        reranked = []
        for chunk, score in ranked[:n]:
            chunk.score = float(score)
            reranked.append(chunk)
        return reranked

    except Exception as exc:
        logger.warning(
            "reranker_unavailable",
            error=str(exc),
            fallback="score_sort",
        )
        return sorted(chunks, key=lambda c: c.score, reverse=True)[:n]


def retrieve_and_rerank(
    query: str,
    user_roles: list[str],
    top_k: int | None = None,
    top_n: int | None = None,
) -> list[RetrievedChunk]:
    """Full retrieval pipeline: vector search â†’ ACL filter â†’ rerank."""
    candidates = retrieve(query, user_roles, top_k=top_k)
    return rerank(query, candidates, top_n=top_n)