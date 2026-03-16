"""Tests for the document ingestion pipeline."""

from __future__ import annotations

from app.ingestion.chunker import Chunk, chunk_text, split_into_semantic_sections
from app.ingestion.loader import _clean_text, load_markdown, load_txt

# ---------------------------------------------------------------------------
# Text cleaning
# ---------------------------------------------------------------------------


def test_clean_text_removes_control_chars():
    raw = "Hello\x00World\x1f!"
    cleaned = _clean_text(raw)
    assert "\x00" not in cleaned
    assert "\x1f" not in cleaned
    assert "Hello" in cleaned


def test_clean_text_normalizes_newlines():
    raw = "Line1\r\nLine2\rLine3"
    cleaned = _clean_text(raw)
    assert "\r" not in cleaned
    assert "Line1\nLine2\nLine3" == cleaned


def test_clean_text_collapses_blank_lines():
    raw = "Para1\n\n\n\n\nPara2"
    cleaned = _clean_text(raw)
    assert "\n\n\n" not in cleaned


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def test_load_txt(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text("Hello HealthTech!\nThis is a test.", encoding="utf-8")
    text = load_txt(p)
    assert "Hello HealthTech" in text


def test_load_markdown(tmp_path):
    p = tmp_path / "test.md"
    content = "# Section 1\n\nSome text here.\n\n## Section 2\n\nMore text."
    p.write_text(content, encoding="utf-8")
    text = load_markdown(p)
    assert "Section 1" in text
    assert "More text" in text


# ---------------------------------------------------------------------------
# Chunker
# ---------------------------------------------------------------------------


def test_split_into_semantic_sections_markdown():
    text = "# Section 1\n\nParagraph one.\n\n## Section 2\n\nParagraph two."
    sections = split_into_semantic_sections(text)
    assert len(sections) >= 2
    assert any("Section 1" in s for s in sections)
    assert any("Section 2" in s for s in sections)


def test_chunk_text_basic():
    text = """# Policy Overview

This is the introduction paragraph with some content.

## Section A

This section discusses the first important topic in our company guidelines and policies.
It contains multiple sentences to ensure we have enough content for chunking purposes.

## Section B

This section covers the second major area of our documentation.
It also contains enough text to be meaningful in the context of retrieval.
"""
    chunks = chunk_text(text, doc_id="test_doc_001")
    assert len(chunks) >= 1
    for chunk in chunks:
        assert isinstance(chunk, Chunk)
        assert chunk.chunk_text.strip()
        assert chunk.metadata["doc_id"] == "test_doc_001"
        assert "access_tags" in chunk.metadata


def test_chunk_text_preserves_metadata():
    text = "Some document text with multiple sections.\n\n## Section\n\nMore content here."
    metadata = {
        "author": "Test Author",
        "access_tags": ["hr-team"],
        "pii_flags": ["PHI"],
    }
    chunks = chunk_text(text, doc_id="meta_test", metadata=metadata)
    assert len(chunks) >= 1
    for chunk in chunks:
        assert chunk.metadata["author"] == "Test Author"
        assert chunk.metadata["access_tags"] == ["hr-team"]
        assert chunk.metadata["pii_flags"] == ["PHI"]


def test_chunk_text_unique_ids():
    text = "\n\n".join([f"Section {i}: " + "word " * 60 for i in range(10)])
    chunks = chunk_text(text, doc_id="unique_id_test")
    ids = [c.chunk_id for c in chunks]
    assert len(ids) == len(set(ids)), "Chunk IDs must be unique"


def test_chunk_text_large_section_split():
    # A single large section should be split into multiple chunks
    long_text = "word " * 2000  # ~2000 words ≈ ~1333 tokens >> 400 token max
    chunks = chunk_text(long_text, doc_id="large_section_test")
    assert len(chunks) > 1, "Large sections should be split into multiple chunks"
