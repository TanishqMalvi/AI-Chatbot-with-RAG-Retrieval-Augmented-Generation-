"""
LLM factory.
Providers: openai | anthropic | ollama (free, local)
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
    if settings.llm_provider == "anthropic":
        return _build_anthropic()
    if settings.llm_provider == "ollama":
        return _build_ollama()
    return _build_openai()


def _build_openai() -> BaseChatModel:
    from langchain_openai import ChatOpenAI
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
    from langchain_anthropic import ChatAnthropic
    logger.info("loading_llm", provider="anthropic", model=settings.anthropic_model)
    return ChatAnthropic(
        model=settings.anthropic_model,
        anthropic_api_key=settings.anthropic_api_key,
        temperature=0.1,
        max_tokens=1024,
        timeout=30,
        max_retries=2,
    )


def _build_ollama() -> BaseChatModel:
    from langchain_ollama import ChatOllama
    logger.info("loading_llm", provider="ollama", model=settings.ollama_model)
    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=0.1,
        num_predict=1024,
    )
