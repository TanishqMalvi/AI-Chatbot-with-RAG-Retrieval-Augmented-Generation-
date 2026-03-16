"""JWT authentication and authorization helpers."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import structlog
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from app.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()

bearer_scheme = HTTPBearer()


# ---------------------------------------------------------------------------
# Token models
# ---------------------------------------------------------------------------


class TokenPayload(BaseModel):
    sub: str  # user ID
    roles: list[str] = []  # e.g. ["hr-team", "engineering"]
    exp: datetime | None = None


class UserContext(BaseModel):
    user_id: str
    roles: list[str]


# ---------------------------------------------------------------------------
# Token creation (used by /token demo endpoint)
# ---------------------------------------------------------------------------


def create_access_token(
    subject: str,
    roles: list[str],
    expires_delta: timedelta | None = None,
) -> str:
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.jwt_access_token_expire_minutes)
    )
    payload: dict[str, Any] = {
        "sub": subject,
        "roles": roles,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


# ---------------------------------------------------------------------------
# Token validation dependency
# ---------------------------------------------------------------------------


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> UserContext:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        user_id: str = payload.get("sub", "")
        roles: list[str] = payload.get("roles", [])
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject",
            )
        return UserContext(user_id=user_id, roles=roles)
    except JWTError as exc:
        logger.warning("jwt_validation_failed", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc
