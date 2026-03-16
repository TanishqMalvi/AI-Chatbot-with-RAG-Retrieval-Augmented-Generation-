"""
LLM factory.

Blueprint §8:
- Default: GPT-4o-mini
- Fallback: Claude 3.5 Sonnet (set LLM_PROVIDER=anthropic)
- Context limited to MAX_CONTEXT_CHUNKS chunks.
"""

from __future__ import annotations

from functools import lru_cache

import structlog
from langchain_core.language_models.chat_models import BaseChatModel

from app.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()


@lru_cache(maxsize=1)
def get_llm() -> BaseChatModel:
    """Return a cached LLM instance based on LLM_PROVIDER env var."""
    if settings.llm_provider == "anthropic":
        return _build_anthropic()
    return _build_openai()


def _build_openai() -> BaseChatModel:
    from langchain_openai import ChatOpenAI  # type: ignore[import]

    logger.info("loading_llm", provider="openai", model=settings.openai_chat_model)
    return ChatOpenAI(
        model=settings.openai_chat_model,
        openai_api_key=settings.openai_api_key,
        temperature=0.1,
        max_tokens=1024,
        timeout=30,
        max_retries=2,
    )


def _build_anthropic() -> BaseChatModel:
    from langchain_anthropic import ChatAnthropic  # type: ignore[import]

    logger.info("loading_llm", provider="anthropic", model=settings.anthropic_model)
    return ChatAnthropic(
        model=settings.anthropic_model,
        anthropic_api_key=settings.anthropic_api_key,
        temperature=0.1,
        max_tokens=1024,
        timeout=30,
        max_retries=2,
    )
