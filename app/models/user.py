"""User model."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import List

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    roles: Mapped[str] = mapped_column(String(500), default="user", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    def get_roles(self) -> List[str]:
        return [r.strip() for r in self.roles.split(",") if r.strip()]

    def set_roles(self, roles: List[str]) -> None:
        self.roles = ",".join(roles)