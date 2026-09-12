from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=128)


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    message: str = "If an account exists for that email, a reset code has been sent."


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)
    new_password: str = Field(min_length=8, max_length=128)


class ResetPasswordResponse(BaseModel):
    message: str = "Password has been reset. You can log in with your new password."


class RequestOtpRequest(BaseModel):
    email: EmailStr


class RequestOtpResponse(BaseModel):
    message: str = "If an account exists for that email, a verification code has been sent."


class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)
    password: str = Field(min_length=1, max_length=128)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    """/auth/login's response.

    Either a token (AUTH_REQUIRE_OTP=false, or OTP already satisfied), or
    otp_required=true with no token -- meaning the password was correct, a
    code has been sent to the account's email, and the client must continue
    at /auth/verify-otp with that code and the same password.
    """

    access_token: str | None = None
    token_type: str = "bearer"
    otp_required: bool = False


class TokenPayload(BaseModel):
    sub: UUID
    username: str
    role: UserRole
    exp: int | None = None


__all__ = [
    "LoginRequest",
    "ForgotPasswordRequest",
    "ForgotPasswordResponse",
    "ResetPasswordRequest",
    "ResetPasswordResponse",
    "RequestOtpRequest",
    "RequestOtpResponse",
    "VerifyOtpRequest",
    "Token",
    "LoginResponse",
    "TokenPayload",
]
