"""
Application configuration using Pydantic Settings.
All values are read from environment variables or .env file.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "HealthTech-RAG-Assistant"
    app_env: Literal["development", "production", "test"] = "development"
    log_level: str = "INFO"

    # OpenAI
    openai_api_key: str = Field(default="", description="OpenAI API key")
    openai_embedding_model: str = "text-embedding-3-large"
    openai_chat_model: str = "gpt-4o-mini"

    # LLM Provider
    llm_provider: Literal["openai", "anthropic"] = "openai"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20241022"

    # Vector DB
    vector_db: Literal["chroma", "pinecone"] = "chroma"
    chroma_persist_dir: str = "./chroma_db"
    chroma_collection: str = "healthtech_rag"
    pinecone_api_key: str = ""
    pinecone_environment: str = "us-east-1-aws"
    pinecone_index_name: str = "healthtech-rag"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    # Retrieval
    retrieval_top_k: int = 20
    rerank_top_n: int = 6
    max_context_chunks: int = 6
    reranker_model: str = "BAAI/bge-reranker-large"

    # Guardrails
    enable_pii_redaction: bool = True
    enable_prompt_injection_check: bool = True
    enable_hallucination_check: bool = True
    confidence_threshold: float = 0.35

    # LangSmith observability
    langchain_tracing_v2: bool = False
    langchain_api_key: str = ""
    langchain_project: str = "healthtech-rag"

    # Ingestion
    ingest_batch_size: int = 32
    ingest_webhook_secret: str = "change-me-webhook-secret"

    @field_validator("openai_api_key")
    @classmethod
    def warn_missing_openai_key(cls, v: str) -> str:
        if not v:
            import warnings
            warnings.warn(
                "OPENAI_API_KEY is not set. Embedding and generation will fail.",
                stacklevel=2,
            )
        return v


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
