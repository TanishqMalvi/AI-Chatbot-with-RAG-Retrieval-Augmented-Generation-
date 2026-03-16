"""
Semantic text chunker.

Blueprint §5:
- Split by semantic boundaries (headings, paragraphs).
- 200–400 tokens per chunk, 20–40 token overlap.
- Keep source IDs and ACL metadata.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

# Approximate token count: ~0.75 tokens per word (rough heuristic for English)
WORDS_PER_TOKEN = 0.75
TARGET_TOKEN_MIN = 200
TARGET_TOKEN_MAX = 400
OVERLAP_TOKENS = 30


def _word_count(text: str) -> int:
    return len(text.split())


def _token_estimate(text: str) -> int:
    return int(_word_count(text) / WORDS_PER_TOKEN)


@dataclass
class Chunk:
    """A single document chunk ready for embedding."""

    chunk_id: str
    chunk_text: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.chunk_id:
            self.chunk_id = str(uuid.uuid4())


def split_into_semantic_sections(text: str) -> list[str]:
    """
    Split text at Markdown headings and double-newline paragraph boundaries.

    Keeps heading text attached to its section.
    """
    # Split on Markdown headings or double newlines
    heading_pattern = re.compile(r"(?=^#{1,6}\s)", re.MULTILINE)
    sections = heading_pattern.split(text)

    # Also split oversized paragraphs at double newlines
    refined: list[str] = []
    for section in sections:
        if _token_estimate(section) > TARGET_TOKEN_MAX * 2:
            refined.extend(re.split(r"\n{2,}", section))
        else:
            refined.append(section)

    return [s.strip() for s in refined if s.strip()]


def chunk_text(
    text: str,
    doc_id: str,
    metadata: dict[str, Any] | None = None,
) -> list[Chunk]:
    """
    Chunk document text into semantically bounded pieces with overlap.

    Parameters
    ----------
    text:     Full document text (already loaded & cleaned).
    doc_id:   Stable document identifier (filename / DB row ID).
    metadata: Document-level metadata merged into every chunk.
              Must include 'access_tags' and optionally 'pii_flags'.
    """
    meta = metadata or {}
    sections = split_into_semantic_sections(text)

    chunks: list[Chunk] = []
    buffer: list[str] = []
    buffer_tokens: int = 0

    def _flush_buffer(overlap_section: str | None = None) -> None:
        if not buffer:
            return
        combined = " ".join(buffer)
        chunk_meta = {
            "doc_id": doc_id,
            "section": buffer[0][:80],  # first ~80 chars as section label
            "author": meta.get("author", "unknown"),
            "created_at": meta.get("created_at", datetime.now(UTC).isoformat()),
            "access_tags": meta.get("access_tags", ["all-employees"]),
            "pii_flags": meta.get("pii_flags", []),
            "chunk_index": len(chunks),
        }
        chunks.append(
            Chunk(
                chunk_id=f"{doc_id}_{len(chunks)}",
                chunk_text=combined,
                metadata=chunk_meta,
            )
        )
        buffer.clear()
        # Add overlap from last section
        if overlap_section:
            words = overlap_section.split()
            overlap_word_count = int(OVERLAP_TOKENS / WORDS_PER_TOKEN)
            overlap_text = " ".join(words[-overlap_word_count:])
            buffer.append(overlap_text)

    for section in sections:
        section_tokens = _token_estimate(section)

        if section_tokens > TARGET_TOKEN_MAX:
            # Section too large → flush current buffer then split section itself
            _flush_buffer()
            words = section.split()
            target_words = int(TARGET_TOKEN_MAX / WORDS_PER_TOKEN)
            overlap_words = int(OVERLAP_TOKENS / WORDS_PER_TOKEN)
            start = 0
            while start < len(words):
                end = min(start + target_words, len(words))
                sub_text = " ".join(words[start:end])
                chunk_meta = {
                    "doc_id": doc_id,
                    "section": section[:80],
                    "author": meta.get("author", "unknown"),
                    "created_at": meta.get(
                        "created_at", datetime.now(UTC).isoformat()
                    ),
                    "access_tags": meta.get("access_tags", ["all-employees"]),
                    "pii_flags": meta.get("pii_flags", []),
                    "chunk_index": len(chunks),
                }
                chunks.append(
                    Chunk(
                        chunk_id=f"{doc_id}_{len(chunks)}",
                        chunk_text=sub_text,
                        metadata=chunk_meta,
                    )
                )
                start += target_words - overlap_words
            continue

        if buffer_tokens + section_tokens > TARGET_TOKEN_MAX and buffer:
            _flush_buffer(overlap_section=buffer[-1] if buffer else None)

        buffer.append(section)
        buffer_tokens = _token_estimate(" ".join(buffer))

    _flush_buffer()

    logger.info(
        "chunking_complete",
        doc_id=doc_id,
        num_chunks=len(chunks),
        avg_tokens=sum(_token_estimate(c.chunk_text) for c in chunks) // max(len(chunks), 1),
    )
    return chunks
