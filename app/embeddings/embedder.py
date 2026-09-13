"""
Embedding module.

Uses Ollama nomic-embed-text for local, free embeddings.
No API key required - runs entirely on-device via Ollama.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Protocol

import structlog

from app.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()


class EmbedderProtocol(Protocol):
    """Minimal interface any embedder must satisfy."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...

    def embed_query(self, text: str) -> list[float]: ...


@lru_cache(maxsize=1)
def get_embedder() -> EmbedderProtocol:
    """
    Return a cached embedder instance.

    - openai (default): Uses OpenAI text-embedding model. Requires OPENAI_API_KEY.
    - ollama: Uses Ollama nomic-embed-text locally. Requires Ollama running.
      Run: ollama pull nomic-embed-text
    """
    provider = settings.llm_provider

    if provider == "ollama":
        from langchain_ollama import OllamaEmbeddings

        ollama_url = settings.ollama_base_url
        model = "nomic-embed-text"
        logger.info("loading_embedder", provider="ollama", model=model, base_url=ollama_url)
        return OllamaEmbeddings(model=model, base_url=ollama_url)

    # Default: OpenAI embeddings
    from langchain_openai import OpenAIEmbeddings

    model = settings.openai_embedding_model
    logger.info("loading_embedder", provider="openai", model=model)
    return OpenAIEmbeddings(
        model=model,
        openai_api_key=settings.openai_api_key,
    )
