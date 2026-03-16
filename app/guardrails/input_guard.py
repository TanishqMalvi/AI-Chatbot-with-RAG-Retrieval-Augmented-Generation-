"""
Input guardrails.

Blueprint §9:
- PII redaction (Presidio).
- Prompt-injection detection (heuristic + optional LLM check).
"""

from __future__ import annotations

import re

import structlog

from app.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()

# ---------------------------------------------------------------------------
# PII redaction using Microsoft Presidio
# ---------------------------------------------------------------------------

_presidio_analyzer = None
_presidio_anonymizer = None


def _get_presidio():
    """Lazy-load Presidio to avoid import overhead on startup."""
    global _presidio_analyzer, _presidio_anonymizer
    if _presidio_analyzer is None:
        try:
            from presidio_analyzer import AnalyzerEngine  # type: ignore
            from presidio_anonymizer import AnonymizerEngine  # type: ignore

            _presidio_analyzer = AnalyzerEngine()
            _presidio_anonymizer = AnonymizerEngine()
        except Exception as exc:
            logger.warning("presidio_not_available", error=str(exc))
    return _presidio_analyzer, _presidio_anonymizer


def redact_pii(text: str) -> tuple[str, list[str]]:
    """
    Redact PII from input text using Presidio.

    Returns (redacted_text, list_of_detected_entity_types).
    Falls back to regex-based redaction if Presidio is unavailable.
    """
    if not settings.enable_pii_redaction:
        return text, []

    analyzer, anonymizer = _get_presidio()
    if analyzer and anonymizer:
        try:
            results = analyzer.analyze(text=text, language="en")
            entity_types = list({r.entity_type for r in results})
            if results:
                anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
                return anonymized.text, entity_types
            return text, []
        except Exception as exc:
            logger.warning("presidio_redaction_failed", error=str(exc))

    # Regex fallback
    return _regex_redact(text)


def _regex_redact(text: str) -> tuple[str, list[str]]:
    """Minimal regex-based PII redaction as Presidio fallback."""
    detected: list[str] = []
    # SSN
    if re.search(r"\b\d{3}-\d{2}-\d{4}\b", text):
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "<SSN>", text)
        detected.append("US_SSN")
    # Credit card (16 digits)
    if re.search(r"\b(?:\d[ -]?){15,16}\d\b", text):
        text = re.sub(r"\b(?:\d[ -]?){15,16}\d\b", "<CREDIT_CARD>", text)
        detected.append("CREDIT_CARD")
    # Email
    if re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text):
        text = re.sub(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", "<EMAIL>", text)
        detected.append("EMAIL_ADDRESS")
    # Phone (US)
    if re.search(r"\b(\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", text):
        text = re.sub(
            r"\b(\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
            "<PHONE>",
            text,
        )
        detected.append("PHONE_NUMBER")
    return text, detected


# ---------------------------------------------------------------------------
# Prompt injection detection
# ---------------------------------------------------------------------------

_INJECTION_PATTERNS = [
    r"ignore\s+(previous|all|above|prior)\s+(instructions?|rules?|prompts?)",
    r"you\s+are\s+now\s+(a|an|the)\s+\w+",
    r"disregard\s+(your|all|the|these)\s+(instructions?|rules?|constraints?)",
    r"jailbreak",
    r"dan\s+mode",
    r"pretend\s+(you\s+are|to\s+be)",
    r"act\s+as\s+(if\s+you\s+(are|were)|a|an)",
    r"reveal\s+(your\s+)?(system\s+)?prompt",
    r"what\s+are\s+your\s+instructions",
    r"repeat\s+the\s+(text|words?)\s+above",
    r"output\s+your\s+(system\s+)?prompt",
]
_INJECTION_RE = re.compile(
    "|".join(_INJECTION_PATTERNS),
    re.IGNORECASE | re.DOTALL,
)


def detect_prompt_injection(text: str) -> bool:
    """
    Return True if the input appears to contain a prompt injection attempt.

    Uses pattern matching (fast). For production, complement with an LLM-based
    classifier (microsoft/prompt-guard or a small fine-tuned model).
    """
    if not settings.enable_prompt_injection_check:
        return False
    return bool(_INJECTION_RE.search(text))


def sanitize_input(text: str) -> tuple[str, list[str], bool]:
    """
    Full input sanitization pipeline.

    Returns (sanitized_text, detected_pii_types, is_injection_attempt).
    """
    redacted, pii_types = redact_pii(text)
    is_injection = detect_prompt_injection(text)  # check before redaction
    return redacted, pii_types, is_injection
