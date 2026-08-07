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
    LoginRequest,
    OtpRequiredResponse,
    OtpVerifyRequest,
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
    """Creates a new staff user (doctor/admin/receptionist)."""
    return auth_service.register(db, payload)


@router.post("/login", response_model=OtpRequiredResponse)
def login(
    credentials: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> OtpRequiredResponse:
    """
    Verifies username/email + password. On success, emails a 6-digit
    code and returns a confirmation (no token yet) — call /verify-otp
    with that code to receive the actual JWT.
    """
    user = auth_service.verify_credentials(
        db,
        credentials.username,
        credentials.password,
    )
    generate_and_send_otp(identity=user.username, to_email=user.email)
    return OtpRequiredResponse()


@router.post("/verify-otp", response_model=Token)
def verify_login_otp(
    payload: OtpVerifyRequest,
    db: Annotated[Session, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Token:
    """
    Exchanges a valid, unexpired OTP for a real access token.
    """
    if not verify_otp(identity=payload.username, submitted_code=payload.otp):
        raise InvalidCredentialsError("Invalid or expired verification code.")

    user = auth_service.user_service.get_user_by_username(db, payload.username)
    if user is None:
        raise InvalidCredentialsError("Invalid or expired verification code.")

    return Token(access_token=auth_service.create_access_token(user))


@router.get("/me", response_model=UserResponse)
def read_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserResponse:
    """Returns the identity tied to the bearer token."""
    return current_user