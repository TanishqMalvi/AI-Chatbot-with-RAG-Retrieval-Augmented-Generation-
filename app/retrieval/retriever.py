"""
Retrieval module: vector search + cross-encoder reranking.

Blueprint §6-7:
- Retrieve k=20 candidates via cosine similarity.
- Apply row-level ACL filter BEFORE retrieval.
- Rerank to top 5-8 with bge-reranker-large.
"""

from __future__ import annotations

from dataclasses import dataclass
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

    Blueprint §9: Row-level security via metadata filtering BEFORE retrieval.
    A document is accessible if any of the user's roles appears in access_tags.
    The special tag "all-employees" grants access to everyone.

    For Chroma the filter uses the $or / $contains operators.
    For Pinecone the filter syntax is slightly different – adapt as needed.
    """
    # We store access_tags as a comma-separated string in Chroma.
    # Build an $or filter checking for each role + the universal tag.
    tags_to_check = list(set(user_roles + ["all-employees"]))

    if len(tags_to_check) == 1:
        return {"access_tags": {"$contains": tags_to_check[0]}}

    return {
        "$or": [
            {"access_tags": {"$contains": tag}}
            for tag in tags_to_check
        ]
    }


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
                score=float(score),
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

    Blueprint §7: bge-reranker-large cross-encoder.
    Falls back to score-sorted ordering if the model is unavailable.
    """
    n = top_n or settings.rerank_top_n
    if not chunks:
        return []

    try:
        from sentence_transformers import CrossEncoder  # type: ignore

        logger.info("reranking", model=settings.reranker_model, candidates=len(chunks))
        cross_encoder = CrossEncoder(settings.reranker_model)
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
        # Fallback: sort by original similarity score
        return sorted(chunks, key=lambda c: c.score, reverse=True)[:n]


def retrieve_and_rerank(
    query: str,
    user_roles: list[str],
    top_k: int | None = None,
    top_n: int | None = None,
) -> list[RetrievedChunk]:
    """Full retrieval pipeline: vector search → ACL filter → rerank."""
    candidates = retrieve(query, user_roles, top_k=top_k)
    return rerank(query, candidates, top_n=top_n)
