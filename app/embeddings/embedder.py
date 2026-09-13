"""
Embedding module.

Supports OpenAI, Ollama, and Hugging Face Inference API embeddings.
The embedding provider is configured independently from chat generation.
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

    - openai: Uses OpenAI text-embedding model. Requires OPENAI_API_KEY.
    - ollama: Uses Ollama nomic-embed-text locally. Requires Ollama running.
      Run: ollama pull nomic-embed-text
    - huggingface: Uses Hugging Face Inference API embeddings. Requires HUGGINGFACE_API_KEY.
    """
    provider = settings.embedding_provider

    if provider == "ollama":
        from langchain_ollama import OllamaEmbeddings

        ollama_url = settings.ollama_base_url
        model = "nomic-embed-text"
        logger.info("loading_embedder", provider="ollama", model=model, base_url=ollama_url)
        return OllamaEmbeddings(model=model, base_url=ollama_url)

    if provider == "huggingface":
        from langchain_huggingface import HuggingFaceEndpointEmbeddings

        model = settings.huggingface_embedding_model
        logger.info("loading_embedder", provider="huggingface", model=model)
        return HuggingFaceEndpointEmbeddings(
            model=model,
            task="feature-extraction",
            huggingfacehub_api_token=settings.huggingface_api_key,
        )

    # Default: OpenAI embeddings
    from langchain_openai import OpenAIEmbeddings

    model = settings.openai_embedding_model
    logger.info("loading_embedder", provider="openai", model=model)
    return OpenAIEmbeddings(
        model=model,
        openai_api_key=settings.openai_api_key,
    )
