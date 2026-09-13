"""
LLM factory.
Providers: openai | anthropic | ollama | gemini | openrouter
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
    if settings.llm_provider == "gemini":
        return _build_gemini()
    if settings.llm_provider == "openrouter":
        return _build_openrouter()
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
        num_predict=512,
    )


def _build_gemini() -> BaseChatModel:
    from langchain_google_genai import ChatGoogleGenerativeAI

    logger.info("loading_llm", provider="gemini", model=settings.gemini_model)
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.gemini_api_key,
        temperature=0.1,
        max_tokens=1024,
        timeout=30,
        max_retries=2,
    )


def _build_openrouter() -> BaseChatModel:
    from langchain_openai import ChatOpenAI

    logger.info(
        "loading_llm", provider="openrouter", model=settings.openrouter_model
    )
    return ChatOpenAI(
        model=settings.openrouter_model,
        openai_api_key=settings.openrouter_api_key,
        openai_api_base=settings.openrouter_base_url,
        temperature=0.1,
        max_tokens=1024,
        timeout=30,
        max_retries=2,
    )
