"""
Document ingestion API endpoint.

Supports:
- Single file upload (multipart/form-data)
- Directory batch ingestion (internal/admin)
- Webhook-triggered ingestion
"""

from __future__ import annotations

import hashlib
import hmac
import tempfile
from pathlib import Path
from typing import Any

import structlog
from fastapi import APIRouter, Depends, File, Header, HTTPException, Request, UploadFile, status
from pydantic import BaseModel

from app.audit.logger import audit_log
from app.auth.jwt_handler import UserContext, get_current_user
from app.config import get_settings
from app.ingestion.pipeline import ingest_directory, ingest_file

logger = structlog.get_logger(__name__)
settings = get_settings()

router = APIRouter()

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


# ---------------------------------------------------------------------------
# Admin-only role check
# ---------------------------------------------------------------------------


def require_admin(user: UserContext = Depends(get_current_user)) -> UserContext:
    if "admin" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required for document ingestion.",
        )
    return user


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class IngestResponse(BaseModel):
    filename: str
    chunks_ingested: int
    doc_id: str


class BatchIngestResponse(BaseModel):
    results: dict[str, int]
    total_chunks: int


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post("/ingest/file", response_model=IngestResponse)
async def ingest_single_file(
    request: Request,
    file: UploadFile = File(...),
    access_tags: str = "all-employees",
    author: str = "system",
    pii_flags: str = "",
    user: UserContext = Depends(require_admin),
) -> IngestResponse:
    """
    Upload and ingest a single document (PDF, TXT, or Markdown).

    access_tags: comma-separated role tags, e.g. "hr-team,admin"
    pii_flags:   comma-separated PII type flags, e.g. "PHI,PII"
    """
    suffix = Path(file.filename or "upload").suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{suffix}'. Supported: {SUPPORTED_EXTENSIONS}",
        )

    content = await file.read()
    request_id = getattr(request.state, "request_id", "unknown")

    doc_id = hashlib.sha256(content).hexdigest()[:16]

    metadata: dict[str, Any] = {
        "access_tags": [t.strip() for t in access_tags.split(",") if t.strip()],
        "author": author,
        "pii_flags": [f.strip() for f in pii_flags.split(",") if f.strip()],
        "filename": file.filename or "upload",
    }

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        n_chunks = ingest_file(tmp_path, metadata=metadata)
    finally:
        tmp_path.unlink(missing_ok=True)

    audit_log(
        "doc_ingested",
        user_id=user.user_id,
        details={"filename": file.filename, "chunks": n_chunks, "doc_id": doc_id},
        request_id=request_id,
    )

    return IngestResponse(filename=file.filename or "upload", chunks_ingested=n_chunks, doc_id=doc_id)


@router.post("/ingest/directory", response_model=BatchIngestResponse)
async def ingest_data_directory(
    request: Request,
    directory: str = "./data",
    user: UserContext = Depends(require_admin),
) -> BatchIngestResponse:
    """
    Batch-ingest all supported documents from a server-side directory.
    Used for initial data loading and scheduled re-ingestion.
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Directory not found: {directory}",
        )

    results = ingest_directory(dir_path)
    total = sum(v for v in results.values() if v > 0)

    audit_log(
        "batch_ingest",
        user_id=user.user_id,
        details={"directory": directory, "total_chunks": total, "files": len(results)},
        request_id=getattr(request.state, "request_id", "unknown"),
    )

    return BatchIngestResponse(results=results, total_chunks=total)


@router.post("/ingest/webhook", status_code=status.HTTP_202_ACCEPTED)
async def webhook_ingest(
    request: Request,
    x_webhook_signature: str = Header(default=""),
) -> dict[str, str]:
    """
    Webhook endpoint for automated ingestion triggers (e.g., S3 event, CMS publish).

    Validates HMAC-SHA256 signature using INGEST_WEBHOOK_SECRET.
    """
    body = await request.body()

    # Validate HMAC signature
    expected = hmac.new(
        settings.ingest_webhook_secret.encode(),
        body,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(f"sha256={expected}", x_webhook_signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature.",
        )

    # In production: parse body, enqueue background task (Celery/RQ/ARQ)
    logger.info("webhook_ingest_received", body_size=len(body))
    return {"status": "accepted", "message": "Ingestion queued for background processing."}
