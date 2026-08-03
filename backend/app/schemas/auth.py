"""Authentication request and response schemas."""

from uuid import UUID

from pydantic import BaseModel, Field

from app.models.user import UserRole


class LoginRequest(BaseModel):
    """Credentials submitted to obtain an access token."""

    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=128)


class Token(BaseModel):
    """Bearer token returned after successful authentication."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Claims read from a validated access token."""

    sub: UUID
    username: str
    role: UserRole
    exp: int | None = None


__all__ = ["LoginRequest", "Token", "TokenPayload"]
