"""
Vector database client factory.

Blueprint §3:
- Development: Chroma (local, zero-config)
- Production:  Pinecone serverless (swap via VECTOR_DB=pinecone)

Blueprint §6 index design:
  {id, chunk_text, embedding, metadata: {doc_id, section, author, created_at, access_tags, pii_flags}}
  Cosine similarity.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import structlog

from app.config import get_settings
from app.embeddings.embedder import get_embedder

logger = structlog.get_logger(__name__)
settings = get_settings()


@lru_cache(maxsize=1)
def get_vector_store() -> Any:
    """
    Return a cached LangChain-compatible vector store.

    Switch between Chroma and Pinecone by setting VECTOR_DB env var.
    """
    if settings.vector_db == "pinecone":
        return _build_pinecone()
    return _build_chroma()


def _build_chroma() -> Any:
    """Build a Chroma vector store (local, persistent)."""
    from langchain_chroma import Chroma  # type: ignore[import]

    logger.info(
        "initializing_chroma",
        persist_dir=settings.chroma_persist_dir,
        collection=settings.chroma_collection,
    )
    return Chroma(
        collection_name=settings.chroma_collection,
        embedding_function=get_embedder(),
        persist_directory=settings.chroma_persist_dir,
        collection_metadata={"hnsw:space": "cosine"},
    )


def _build_pinecone() -> Any:
    """
    Build a Pinecone serverless vector store.

    Set these env vars to switch from Chroma → Pinecone:
      VECTOR_DB=pinecone
      PINECONE_API_KEY=pcsk_...
      PINECONE_ENVIRONMENT=us-east-1-aws
      PINECONE_INDEX_NAME=healthtech-rag
    """
    from langchain_community.vectorstores import Pinecone as LCPinecone  # type: ignore
    from pinecone import Pinecone, ServerlessSpec  # type: ignore

    pc = Pinecone(api_key=settings.pinecone_api_key)
    index_name = settings.pinecone_index_name

    existing = [idx.name for idx in pc.list_indexes()]
    if index_name not in existing:
        logger.info("creating_pinecone_index", index=index_name)
        pc.create_index(
            name=index_name,
            dimension=3072,  # text-embedding-3-large
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=settings.pinecone_environment),
        )

    logger.info("initializing_pinecone", index=index_name)
    return LCPinecone.from_existing_index(
        index_name=index_name,
        embedding=get_embedder(),
    )
