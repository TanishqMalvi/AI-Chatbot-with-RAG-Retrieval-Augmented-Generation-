"""
HealthTech RAG Assistant – FastAPI application entry point.

Pipeline order (blueprint §15):
  ingest → chunk → embed → store → retrieve → rerank → generate → guardrail → respond
"""

from __future__ import annotations

import time
import uuid

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from app.api import auth, chat, health, ingest
from app.config import get_settings
from app.database import init_db

logger = structlog.get_logger(__name__)
settings = get_settings()

# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.app_name,
    description=(
        "Production-grade RAG chatbot for HealthTech enterprise knowledge management. "
        "Supports PDF, TXT, and Markdown documents with JWT-based RBAC and row-level ACLs."
    ),
    version="1.0.0",
    docs_url="/docs" if settings.app_env == "development" else None,
    redoc_url="/redoc" if settings.app_env == "development" else None,
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.app_env == "development" else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Request ID + latency middleware
# ---------------------------------------------------------------------------


@app.middleware("http")
async def request_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start = time.perf_counter()

    response = await call_next(request)

    if isinstance(response, StreamingResponse):
        response.headers["X-Request-ID"] = request_id
        return response

    elapsed_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time-Ms"] = f"{elapsed_ms:.1f}"

    logger.info(
        "request_completed",
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        latency_ms=round(elapsed_ms, 1),
    )
    return response


# ---------------------------------------------------------------------------
# Global exception handler
# ---------------------------------------------------------------------------


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        "unhandled_exception",
        request_id=request_id,
        error=str(exc),
        exc_info=exc,
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "request_id": request_id,
        },
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(ingest.router, prefix="/api/v1", tags=["Ingestion"])


# ---------------------------------------------------------------------------
# Startup: Initialize database and seed admin user
# ---------------------------------------------------------------------------


@app.on_event("startup")
async def startup_event() -> None:
    init_db()
    await seed_admin_user()


async def seed_admin_user() -> None:
    """Create admin user from environment variables if no users exist."""
    from app.auth.jwt_handler import get_user_by_email, hash_password
    from app.config import get_settings
    from app.database import SessionLocal
    from app.models.user import User
    from datetime import UTC, datetime
    import uuid

    settings = get_settings()
    if not settings.admin_email or not settings.admin_password:
        return

    db = SessionLocal()
    try:
        # Check if any users exist
        user_count = db.query(User).count()
        if user_count > 0:
            return

        # Create admin user
        email = settings.admin_email.lower().strip()
        existing = get_user_by_email(db, email)
        if existing:
            return

        user = User(
            id=str(uuid.uuid4()),
            email=email,
            hashed_password=hash_password(settings.admin_password),
            roles="admin,user",
            created_at=datetime.now(UTC),
        )
        db.add(user)
        db.commit()
        logger.info("admin_user_seeded", email=email)
    except Exception as exc:
        logger.error("admin_seeding_failed", error=str(exc))
        db.rollback()
    finally:
        db.close()
