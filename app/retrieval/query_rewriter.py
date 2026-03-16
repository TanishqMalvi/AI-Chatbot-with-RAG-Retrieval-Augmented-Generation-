"""
Query rewriting module.

Blueprint §7: HyDE (Hypothetical Document Embeddings) + multi-query expansion.
These techniques improve recall for ambiguous or short queries.
"""

from __future__ import annotations

import asyncio

import structlog
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.config import get_settings
from app.generation.llm import get_llm

logger = structlog.get_logger(__name__)
settings = get_settings()

# ---------------------------------------------------------------------------
# HyDE: generate a hypothetical answer, embed that instead of the raw query
# ---------------------------------------------------------------------------

_HYDE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert at HealthTech domain knowledge. "
            "Write a concise 2-3 sentence passage that would directly answer the question below. "
            "Do NOT say you don't know. Produce a plausible passage even if uncertain.",
        ),
        ("human", "{query}"),
    ]
)


async def generate_hyde_query(query: str) -> str:
    """Generate a hypothetical document passage for the given query."""
    chain = _HYDE_PROMPT | get_llm() | StrOutputParser()
    try:
        return await chain.ainvoke({"query": query})
    except Exception as exc:
        logger.warning("hyde_failed", error=str(exc))
        return query  # fall back to original query


# ---------------------------------------------------------------------------
# Multi-query: generate N alternative phrasings
# ---------------------------------------------------------------------------

_MULTI_QUERY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Generate {n} alternative phrasings of the question below. "
            "Return ONLY the rephrased questions, one per line, no numbering.",
        ),
        ("human", "{query}"),
    ]
)


async def generate_multi_queries(query: str, n: int = 3) -> list[str]:
    """Generate n alternative phrasings of the query."""
    chain = _MULTI_QUERY_PROMPT | get_llm() | StrOutputParser()
    try:
        result = await chain.ainvoke({"query": query, "n": n})
        variants = [line.strip() for line in result.splitlines() if line.strip()]
        return [query] + variants[:n]
    except Exception as exc:
        logger.warning("multi_query_failed", error=str(exc))
        return [query]


async def rewrite_query(query: str, strategy: str = "hyde") -> list[str]:
    """
    Rewrite a query using the specified strategy.

    Parameters
    ----------
    query:    Original user query.
    strategy: 'hyde' | 'multi_query' | 'both' | 'none'

    Returns a list of query strings to search with.
    """
    if strategy == "none":
        return [query]
    if strategy == "hyde":
        hyde = await generate_hyde_query(query)
        return [hyde]
    if strategy == "multi_query":
        return await generate_multi_queries(query)
    if strategy == "both":
        hyde_task = generate_hyde_query(query)
        multi_task = generate_multi_queries(query, n=2)
        hyde, multi = await asyncio.gather(hyde_task, multi_task)
        return list(dict.fromkeys([query, hyde] + multi))  # deduplicate, preserve order
    return [query]
