"""Health check endpoint."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="HealthTech-RAG-Assistant",
        version="1.0.0",
    )


@router.get("/", include_in_schema=False)
async def root():
    return {"message": "HealthTech RAG Assistant. See /docs for API reference."}
