"""
Document loaders for PDF, TXT, and Markdown files.

Blueprint §5: Support PDFs with layout-aware processing (pdfplumber).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger(__name__)


def _clean_text(text: str) -> str:
    """Normalize whitespace and remove control characters."""
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    text = re.sub(r"\r\n|\r", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_txt(file_path: Path) -> str:
    """Load plain-text file."""
    return _clean_text(file_path.read_text(encoding="utf-8", errors="replace"))


def load_markdown(file_path: Path) -> str:
    """Load Markdown file (kept as-is; chunker handles heading boundaries)."""
    return _clean_text(file_path.read_text(encoding="utf-8", errors="replace"))


def load_pdf(file_path: Path) -> str:
    """
    Load PDF using pdfplumber for layout-aware text extraction.

    Falls back to raw text extraction if pdfplumber fails.
    Blueprint §5: pdfplumber + layoutparser.
    """
    try:
        import pdfplumber  # type: ignore[import]

        pages: list[str] = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text(x_tolerance=2, y_tolerance=2)
                if text:
                    pages.append(text)
        return _clean_text("\n\n".join(pages))
    except Exception as exc:
        logger.warning("pdf_load_fallback", path=str(file_path), error=str(exc))
        # Fallback: raw bytes decode attempt
        return _clean_text(file_path.read_bytes().decode("utf-8", errors="replace"))


LOADER_MAP: dict[str, Any] = {
    ".txt": load_txt,
    ".md": load_markdown,
    ".pdf": load_pdf,
}


def load_document(file_path: Path) -> str:
    """Dispatch to the correct loader based on file extension."""
    suffix = file_path.suffix.lower()
    loader = LOADER_MAP.get(suffix)
    if loader is None:
        raise ValueError(f"Unsupported file type: {suffix}. Supported: {list(LOADER_MAP)}")
    logger.info("loading_document", path=str(file_path), type=suffix)
    return loader(file_path)
