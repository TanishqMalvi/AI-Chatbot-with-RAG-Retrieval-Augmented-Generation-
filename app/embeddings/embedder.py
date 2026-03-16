"""
Embedding module.

Blueprint §4:
- Default: OpenAI text-embedding-3-large
- Fallback: text-embedding-3-small (set OPENAI_EMBEDDING_MODEL=text-embedding-3-small)
- Fine-tuning stub: sentence-transformers (see fine_tune_stub() below)
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

    Uses OpenAI by default. The model is controlled by OPENAI_EMBEDDING_MODEL.
    Switch to text-embedding-3-small to reduce cost (~6× cheaper, ~10% accuracy drop).
    """
    from langchain_openai import OpenAIEmbeddings  # type: ignore[import]

    logger.info("loading_embedder", model=settings.openai_embedding_model)
    return OpenAIEmbeddings(
        model=settings.openai_embedding_model,
        openai_api_key=settings.openai_api_key,
        chunk_size=settings.ingest_batch_size,
    )


# ---------------------------------------------------------------------------
# Fine-tuning stub (Blueprint §4 – domain-specific fine-tuning)
# ---------------------------------------------------------------------------


def fine_tune_stub(
    train_pairs: list[tuple[str, str]],
    model_name: str = "sentence-transformers/all-mpnet-base-v2",
    output_dir: str = "./finetuned-embedder",
    epochs: int = 3,
) -> None:
    """
    Stub for fine-tuning a sentence-transformer on domain-specific query-document pairs.

    Usage:
        pairs = [("What is the PTO policy?", "Employees receive 20 days PTO per year..."), ...]
        fine_tune_stub(pairs)

    After training, set OPENAI_EMBEDDING_MODEL to use the local model path with
    HuggingFaceEmbeddings instead of OpenAI.
    """
    try:
        from sentence_transformers import InputExample, SentenceTransformer  # type: ignore
        from sentence_transformers.losses import CosineSimilarityLoss  # type: ignore
        from torch.utils.data import DataLoader  # type: ignore
    except ImportError:
        logger.error("sentence_transformers_not_installed")
        return

    model = SentenceTransformer(model_name)
    train_examples = [
        InputExample(texts=[q, d], label=1.0) for q, d in train_pairs
    ]
    loader = DataLoader(train_examples, shuffle=True, batch_size=16)
    loss = CosineSimilarityLoss(model)

    model.fit(
        train_objectives=[(loader, loss)],
        epochs=epochs,
        warmup_steps=100,
        output_path=output_dir,
    )
    logger.info("fine_tuning_complete", output_dir=output_dir)
