"""Authentication endpoints."""

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_auth_service, get_current_active_user, get_db
from app.core.session import clear_session_cookie, set_session_cookie
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    LoginResponse,
    RequestOtpRequest,
    RequestOtpResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
    Token,
    VerifyOtpRequest,
)
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.utils import rate_limit

router = APIRouter()

# Every attempt counts toward these limits, successful or not (see
# rate_limit.enforce). Login is keyed on both the target account and the
# source IP, so neither a distributed attack on one account nor one IP
# spraying many accounts is bounded only by the other dimension. The
# OTP-sending endpoints are keyed on the recipient address only, since each
# hit sends a real email; verify/reset are keyed on the account and layer on
# top of the existing per-code guess limit (otp_service.MAX_VERIFY_ATTEMPTS).
_LOGIN_LIMIT = 10
_LOGIN_WINDOW_SECONDS = 15 * 60
_OTP_REQUEST_LIMIT = 3
_OTP_REQUEST_WINDOW_SECONDS = 10 * 60
_OTP_VERIFY_LIMIT = 8
_OTP_VERIFY_WINDOW_SECONDS = 15 * 60


@router.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest,
    request: Request,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> LoginResponse:
    """Verify username/email and password.

    Returns a signed JWT directly when AUTH_REQUIRE_OTP is false. Otherwise
    a code is sent to the account's email and the response carries
    otp_required=true instead -- the client continues at /auth/verify-otp
    with that code and the same password.

    A token is also set as the HttpOnly session cookie, which is what the
    browser app authenticates with; the copy in the body is for API clients.
    """

    rate_limit.enforce(
        f"login:ip:{rate_limit.client_ip(request)}",
        limit=_LOGIN_LIMIT,
        window_seconds=_LOGIN_WINDOW_SECONDS,
        message="Too many sign-in attempts from this location. Try again later.",
    )
    rate_limit.enforce(
        f"login:account:{credentials.username.lower()}",
        limit=_LOGIN_LIMIT,
        window_seconds=_LOGIN_WINDOW_SECONDS,
        message="Too many sign-in attempts for this account. Try again later.",
    )

    result = auth_service.login(db, credentials.username, credentials.password)
    if result.access_token is not None:
        set_session_cookie(response, result.access_token)
    return result


@router.get("/me", response_model=UserResponse)
def read_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserResponse:
    """Return the identity associated with the session cookie or bearer token."""

    return current_user


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(
    payload: ForgotPasswordRequest,
    db: Annotated[Session, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    background_tasks: BackgroundTasks,
) -> ForgotPasswordResponse:
    """Email a reset code if the address belongs to an active account.

    Always returns the same generic message, immediately, so neither this
    endpoint's response nor its timing can be used to enumerate registered
    accounts -- delivery is scheduled to run after the response is sent.
    """

    rate_limit.enforce(
        f"otp-request:password_reset:{payload.email.lower()}",
        limit=_OTP_REQUEST_LIMIT,
        window_seconds=_OTP_REQUEST_WINDOW_SECONDS,
        message="Too many reset codes requested for this address. Try again later.",
    )

    auth_service.request_password_reset(db, payload.email, background_tasks)
    return ForgotPasswordResponse()


@router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(
    payload: ResetPasswordRequest,
    db: Annotated[Session, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> ResetPasswordResponse:
    """Exchange a valid, unexpired reset code for a new password."""

    rate_limit.enforce(
        f"otp-verify:password_reset:{payload.email.lower()}",
        limit=_OTP_VERIFY_LIMIT,
        window_seconds=_OTP_VERIFY_WINDOW_SECONDS,
        message="Too many attempts for this account. Try again later.",
    )

    auth_service.reset_password(db, payload.email, payload.otp, payload.new_password)
    return ResetPasswordResponse()


@router.post("/request-otp", response_model=RequestOtpResponse)
def request_otp_login(
    payload: RequestOtpRequest,
    db: Annotated[Session, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    background_tasks: BackgroundTasks,
) -> RequestOtpResponse:
    """Email an OTP if the address belongs to an active account.

    Always returns the same generic message, immediately, so neither this
    endpoint's response nor its timing can be used to enumerate registered
    accounts -- delivery is scheduled to run after the response is sent.
    """

    rate_limit.enforce(
        f"otp-request:login:{payload.email.lower()}",
        limit=_OTP_REQUEST_LIMIT,
        window_seconds=_OTP_REQUEST_WINDOW_SECONDS,
        message="Too many codes requested for this address. Try again later.",
    )

    auth_service.request_otp_login(db, payload.email, background_tasks)
    return RequestOtpResponse()


@router.post("/verify-otp", response_model=Token)
def verify_otp_login(
    payload: VerifyOtpRequest,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Token:
    """Verify credentials and OTP together, then issue an access token.

    As with /auth/login, the token is also set as the session cookie.
    """

    rate_limit.enforce(
        f"otp-verify:login:{payload.email.lower()}",
        limit=_OTP_VERIFY_LIMIT,
        window_seconds=_OTP_VERIFY_WINDOW_SECONDS,
        message="Too many attempts for this account. Try again later.",
    )

    token = auth_service.verify_otp_login(db, payload.email, payload.otp, payload.password)
    set_session_cookie(response, token.access_token)
    return token


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response) -> None:
    """Clear the session cookie.

    Needs no authentication, so a cookie the server has already rejected can
    always be cleared. It does not revoke the token itself: a copy taken
    elsewhere stays valid until it expires or the password is changed.
    """

    clear_session_cookie(response)
