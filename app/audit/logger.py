"""
Audit logging module.

Writes structured audit events to stdout (captured by log aggregator in prod)
and optionally to a rotating file. Every sensitive operation (auth, retrieval,
generation) must call audit_log() to maintain GDPR / HIPAA compliance.
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import UTC, datetime
from typing import Any

import structlog

logger = structlog.get_logger(__name__)


def audit_log(
    event: str,
    user_id: str,
    details: dict[str, Any] | None = None,
    *,
    request_id: str | None = None,
) -> None:
    """Write a structured audit event.

    Parameters
    ----------
    event:      Machine-readable event name (e.g. 'chat_request', 'doc_ingested').
    user_id:    The authenticated user performing the action.
    details:    Arbitrary additional context (avoid raw PII here).
    request_id: Optional correlation ID from the HTTP request.
    """
    entry: dict[str, Any] = {
        "audit_event": event,
        "user_id": user_id,
        "timestamp": datetime.now(UTC).isoformat(),
        "request_id": request_id or str(uuid.uuid4()),
        **(details or {}),
    }

    # Structured JSON to stdout → picked up by Fluentd / CloudWatch / etc.
    logger.info("AUDIT", **entry)

    # Optional file-based audit trail (rotation handled externally)
    audit_file = os.environ.get("AUDIT_LOG_FILE")
    if audit_file:
        with open(audit_file, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
