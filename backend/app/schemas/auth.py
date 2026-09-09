from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=128)


class OtpVerifyRequest(BaseModel):
    username: str = Field(min_length=1, max_length=255)
    otp: str = Field(min_length=6, max_length=6)


class OtpRequiredResponse(BaseModel):
    otp_required: bool = True
    message: str = "Verification code sent to your email."


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    message: str = "If an account exists for that email, a reset code has been sent."


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)
    new_password: str = Field(min_length=8, max_length=128)


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
    "OtpVerifyRequest",
    "OtpRequiredResponse",
    "ForgotPasswordRequest",
    "ForgotPasswordResponse",
    "ResetPasswordRequest",
    "Token",
    "TokenPayload",
]
