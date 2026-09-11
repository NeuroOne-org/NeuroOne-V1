from uuid import UUID

from pydantic import BaseModel, Field

from app.models.user import UserRole


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=128)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: UUID
    username: str
    role: UserRole
    exp: int | None = None


__all__ = [
    "LoginRequest",
    "Token",
    "TokenPayload",
]
