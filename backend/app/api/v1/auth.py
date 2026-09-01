"""Authentication endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_auth_service,
    get_current_active_user,
    get_db,
)
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    OtpRequiredResponse,
    OtpVerifyRequest,
    ResetPasswordRequest,
    Token,
)
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.services.otp_service import generate_and_send_otp, verify_otp
from app.utils.exceptions import InvalidCredentialsError

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: UserCreate,
    db: Annotated[Session, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserResponse:
    return auth_service.register(db, payload)


@router.post("/login", response_model=OtpRequiredResponse)
def login(
    credentials: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> OtpRequiredResponse:
    user = auth_service.verify_credentials(
        db,
        credentials.username,
        credentials.password,
    )
    # Store the OTP under whatever identity the client submitted at login
    # (credentials.username — e.g. the email typed into the form), not the
    # resolved user.username. The frontend only ever knows the value it
    # typed in, and will send that same value back to /verify-otp — so the
    # storage key and the lookup key must match, or verification always
    # fails with "Invalid or expired verification code."
    generate_and_send_otp(identity=credentials.username, to_email=user.email)
    return OtpRequiredResponse()


@router.post("/verify-otp", response_model=Token)
def verify_login_otp(
    payload: OtpVerifyRequest,
    db: Annotated[Session, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Token:
    if not verify_otp(identity=payload.username, submitted_code=payload.otp):
        raise InvalidCredentialsError("Invalid or expired verification code.")

    # payload.username is whatever the client submitted (may be an email or
    # a real username) — resolve to a user record by trying username first,
    # then falling back to email, so this works regardless of which one the
    # person logged in with.
    user = auth_service.user_service.get_user_by_username(db, payload.username)
    if user is None:
        user = auth_service.user_service.get_user_by_email(db, payload.username)
    if user is None:
        raise InvalidCredentialsError("Invalid or expired verification code.")

    return Token(access_token=auth_service.create_access_token(user))


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(
    payload: ForgotPasswordRequest,
    db: Annotated[Session, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> ForgotPasswordResponse:
    user = auth_service.user_service.get_user_by_email(db, payload.email)
    if user is not None and user.is_active:
        generate_and_send_otp(identity=payload.email, to_email=payload.email)

    return ForgotPasswordResponse()


@router.post("/reset-password", response_model=Token)
def reset_password(
    payload: ResetPasswordRequest,
    db: Annotated[Session, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Token:
    if not verify_otp(identity=payload.email, submitted_code=payload.otp):
        raise InvalidCredentialsError("Invalid or expired reset code.")

    user = auth_service.user_service.get_user_by_email(db, payload.email)
    if user is None:
        raise InvalidCredentialsError("Invalid or expired reset code.")

    new_hash = auth_service.hash_password(payload.new_password)
    auth_service.user_service.set_password(db, user, new_hash)

    return Token(access_token=auth_service.create_access_token(user))


@router.get("/me", response_model=UserResponse)
def read_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserResponse:
    return current_user