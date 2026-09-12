from fastapi import BackgroundTasks
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.models import User
from app.models.user import UserRole
from app.schemas.auth import LoginResponse, Token, TokenPayload
from app.schemas.user import UserCreate, UserResponse
from app.services import otp_service
from app.services.user_service import UserService
from app.utils.exceptions import (
    AuthenticationError,
    AuthorizationError,
    InvalidCredentialsError,
    InvalidOtpError,
    UserAlreadyExistsError,
)


class AuthService:
    """Business logic for authentication operations."""

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def provision_user(
        self,
        db: Session,
        user_data: UserCreate,
        *,
        requested_by: User,
    ) -> UserResponse:
        """Provision a staff user after enforcing the ADMIN boundary."""

        if requested_by.role is not UserRole.ADMIN:
            raise AuthorizationError(
                "You do not have permission to perform this action."
            )

        return self._create_user(db, user_data)

    def bootstrap_admin(self, db: Session, user_data: UserCreate) -> UserResponse:
        """Create the first administrator, and only when none exists."""

        if user_data.role is not UserRole.ADMIN:
            raise ValueError("Bootstrap account must have the ADMIN role.")
        existing_admin = self.user_service.repository.get_first_by_role(
            db,
            UserRole.ADMIN,
        )
        if existing_admin is not None:
            raise UserAlreadyExistsError("An administrator already exists.")
        return self._create_user(db, user_data)

    def _create_user(
        self,
        db: Session,
        user_data: UserCreate,
    ) -> UserResponse:
        """Create a user after uniqueness checks and password hashing."""

        if self.user_service.get_user_by_email(db, str(user_data.email)):
            raise UserAlreadyExistsError("A user with this email already exists.")

        if self.user_service.get_user_by_username(db, user_data.username):
            raise UserAlreadyExistsError(
                "A user with this username already exists."
            )

        hashed_password = self.hash_password(user_data.password)
        user = self.user_service.create_user(
            db,
            user_data,
            hashed_password=hashed_password,
        )

        return UserResponse.model_validate(user)

    def verify_credentials(
        self,
        db: Session,
        username_or_email: str,
        password: str,
    ) -> User:
        """
        Validates username/email + password and returns the User, without
        issuing a token. Used by the OTP flow.
        """

        if "@" in username_or_email:
            user = self.user_service.get_user_by_email(db, username_or_email)
        else:
            user = self.user_service.get_user_by_username(
                db,
                username_or_email,
            )

        if user is None or not self.verify_password(
            password,
            user.hashed_password,
        ):
            raise InvalidCredentialsError("Invalid username/email or password.")

        if not user.is_active:
            raise InvalidCredentialsError("Invalid username/email or password.")

        return user

    def login(
        self,
        db: Session,
        username_or_email: str,
        password: str,
    ) -> LoginResponse:
        """Authenticate a user and, per AUTH_REQUIRE_OTP, either issue a
        token directly or send a login OTP and report that one is required.

        The OTP send happens synchronously and lets delivery failures raise:
        unlike forgot-password/request-otp, the caller has already proven
        they know the password, so there is no account-existence to protect
        by hiding the failure.
        """

        user = self.verify_credentials(db, username_or_email, password)

        if not settings.AUTH_REQUIRE_OTP:
            return LoginResponse(access_token=self.create_access_token(user))

        otp_service.generate_and_send_otp(
            identity=user.email,
            to_email=user.email,
            purpose="login",
        )
        return LoginResponse(otp_required=True)

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """Verify a plaintext password against a stored hash."""

        return security.verify_password(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        """Hash a plaintext password."""

        return security.hash_password(password)

    def create_access_token(self, user: User) -> str:
        """Create an access token for a user."""

        return security.create_access_token(
            {
                "sub": str(user.id),
                "username": user.username,
                "role": user.role.value,
            }
        )

    def verify_access_token(self, token: str) -> TokenPayload:
        """Validate an access token and return its payload."""

        try:
            payload = security.decode_access_token(token)
            return TokenPayload.model_validate(payload)
        except (JWTError, ValidationError, ValueError, TypeError) as exc:
            raise AuthenticationError("Invalid or expired access token.") from exc

    def request_password_reset(
        self,
        db: Session,
        email: str,
        background_tasks: BackgroundTasks,
    ) -> None:
        """
        Schedule a reset-code email if the address belongs to an active
        account. Always returns immediately either way — the lookup is the
        only work done inline, and delivery (including any SMTP failure)
        happens after the response is sent, so neither response latency nor
        a delivery error can reveal whether the address is registered.
        """

        user = self.user_service.get_user_by_email(db, email)
        if user is None or not user.is_active:
            return

        background_tasks.add_task(
            otp_service.send_otp_background,
            identity=email,
            to_email=email,
            purpose="password_reset",
        )

    def request_otp_login(
        self,
        db: Session,
        email: str,
        background_tasks: BackgroundTasks,
    ) -> None:
        """
        Schedule a login-code email if the address belongs to an active
        account. Always returns immediately either way, for the same
        reason as request_password_reset.
        """

        user = self.user_service.get_user_by_email(db, email)
        if user is None or not user.is_active:
            return

        background_tasks.add_task(
            otp_service.send_otp_background,
            identity=email,
            to_email=email,
            purpose="login",
        )

    def verify_otp_login(
        self,
        db: Session,
        email: str,
        otp: str,
        password: str,
    ) -> Token:
        """
        Verify credentials and OTP together, then issue an access token.
        Accepts only a code issued for purpose="login" -- a password-reset
        code cannot be replayed here.
        """

        if not otp_service.verify_otp(identity=email, submitted_code=otp, purpose="login"):
            raise InvalidOtpError("Invalid or expired verification code.")

        user = self.verify_credentials(db, email, password)
        return Token(access_token=self.create_access_token(user))

    def reset_password(
        self,
        db: Session,
        email: str,
        otp: str,
        new_password: str,
    ) -> None:
        """Validate the reset code and set a new password.

        Accepts only a code issued for purpose="password_reset" -- a login
        code cannot be replayed here.
        """

        if not otp_service.verify_otp(
            identity=email, submitted_code=otp, purpose="password_reset"
        ):
            raise InvalidOtpError("Invalid or expired verification code.")

        user = self.user_service.get_user_by_email(db, email)
        if user is None or not user.is_active:
            raise InvalidOtpError("Invalid or expired verification code.")

        self.user_service.set_password(db, user, self.hash_password(new_password))
