"""Authentication endpoints: signup and login."""

from __future__ import annotations

import structlog
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
    create_access_token,
    get_user_by_email,
    hash_password,
    verify_password,
)
from app.config import get_settings
from app.database import get_db
from app.models.user import User

logger = structlog.get_logger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/v1", tags=["Auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(body: SignupRequest, db: Session = Depends(get_db)) -> dict[str, str]:
    """
    Register a new user.

    Creates a user with the given email and password (hashed).
    Default role is "user". Returns success message (no token — user must log in).
    """
    email = body.email.lower().strip()

    # Check if email already exists
    existing = get_user_by_email(db, email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create user
    user_id = str(uuid.uuid4())
    hashed = hash_password(body.password)
    roles = ["user"]  # default role

    user = User(
        id=user_id,
        email=email,
        hashed_password=hashed,
        roles=",".join(roles),
        created_at=datetime.now(UTC),
    )
    db.add(user)
    db.commit()

    logger.info("user_created", user_id=user_id, email=email)
    return {"detail": "Account created successfully. Please log in."}


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """
    Authenticate user and issue JWT.

    Verifies email and password against stored hash.
    Returns 401 with generic message on failure (does not reveal which field was wrong).
    """
    email = body.email.lower().strip()
    user = get_user_by_email(db, email)

    if not user or not verify_password(body.password, user.hashed_password):
        logger.warning("login_failed", email=email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(subject=user.id, roles=user.get_roles())
    logger.info("login_success", user_id=user.id, email=user.email)
    return TokenResponse(access_token=token)


# Keep the old /token endpoint for backward compatibility but mark as deprecated
from pydantic import BaseModel


class TokenRequest(BaseModel):
    user_id: str
    roles: list[str] = ["all-employees"]


@router.post("/token", response_model=TokenResponse, deprecated=True)
async def issue_token(body: TokenRequest) -> TokenResponse:
    """
    Issue a JWT for the given user_id and roles.

    **Deprecated:** For development / testing only. Use /api/v1/login with email/password.
    """
    token = create_access_token(subject=body.user_id, roles=body.roles)
    return TokenResponse(access_token=token)