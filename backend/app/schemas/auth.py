from uuid import UUID

from pydantic import BaseModel, Field

from app.models.user import UserRole


class LoginRequest(BaseModel):
    """Credentials submitted to obtain an access token."""

    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=128)


class OtpVerifyRequest(BaseModel):
    """Username/email plus the 6-digit code emailed to the user."""

    username: str = Field(min_length=1, max_length=50)
    otp: str = Field(min_length=6, max_length=6)


class OtpRequiredResponse(BaseModel):
    """Returned by /login on success, before the JWT is issued."""

    otp_required: bool = True
    message: str = "Verification code sent to your email."


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


__all__ = [
    "LoginRequest",
    "OtpVerifyRequest",
    "OtpRequiredResponse",
    "Token",
    "TokenPayload",
]
