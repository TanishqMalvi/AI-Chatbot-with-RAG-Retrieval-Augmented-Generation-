"""
End-to-end ingestion pipeline.

Order: load → chunk → embed → upsert into vector store.
Supports batch processing and webhook-triggered ingestion.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import structlog

from app.config import get_settings
from app.embeddings.embedder import get_embedder
from app.ingestion.chunker import chunk_text
from app.ingestion.loader import load_document
from app.vectordb.client import get_vector_store

logger = structlog.get_logger(__name__)
settings = get_settings()


def _doc_id_from_path(file_path: Path) -> str:
    """Derive a stable doc_id from the file path."""
    return hashlib.sha256(str(file_path.resolve()).encode()).hexdigest()[:16]


def ingest_file(
    file_path: Path,
    metadata: dict[str, Any] | None = None,
) -> int:
    """
    Ingest a single file into the vector store.

    Returns the number of chunks upserted.
    """
    doc_id = _doc_id_from_path(file_path)
    logger.info("ingesting_file", path=str(file_path), doc_id=doc_id)

    # Step 1: Load
    text = load_document(file_path)
    if not text.strip():
        logger.warning("empty_document", path=str(file_path))
        return 0

    # Default metadata
    meta: dict[str, Any] = {
        "source": str(file_path),
        "filename": file_path.name,
        **(metadata or {}),
    }

    # Step 2: Chunk
    chunks = chunk_text(text, doc_id=doc_id, metadata=meta)
    if not chunks:
        return 0

    # Step 3: Embed (batched)
    embedder = get_embedder()
    texts = [c.chunk_text for c in chunks]
    embeddings = embedder.embed_documents(texts)

    # Step 4: Upsert into vector store
    store = get_vector_store()
    ids = [c.chunk_id for c in chunks]
    metadatas = []
    for c in chunks:
        m = dict(c.metadata)
        # Chroma requires metadata values to be str/int/float/bool
        if isinstance(m.get("access_tags"), list):
            m["access_tags"] = ",".join(m["access_tags"])
        if isinstance(m.get("pii_flags"), list):
            m["pii_flags"] = ",".join(m["pii_flags"])
        metadatas.append(m)

    store.add_texts(texts=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)

    logger.info("ingestion_complete", doc_id=doc_id, chunks_upserted=len(chunks))
    return len(chunks)


def ingest_directory(
    directory: Path,
    glob_pattern: str = "**/*",
    metadata_override: dict[str, Any] | None = None,
) -> dict[str, int]:
    """
    Recursively ingest all supported documents in a directory.

    Returns a dict mapping filename → chunks upserted.
    """
    results: dict[str, int] = {}
    supported_extensions = {".txt", ".md", ".pdf"}

    for file_path in sorted(directory.glob(glob_pattern)):
        if file_path.suffix.lower() not in supported_extensions:
            continue
        if not file_path.is_file():
            continue
        try:
            n = ingest_file(file_path, metadata=metadata_override)
            results[file_path.name] = n
        except Exception as exc:
            logger.error("ingest_file_failed", path=str(file_path), error=str(exc))
            results[file_path.name] = -1

    return results
