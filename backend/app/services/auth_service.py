from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security
from app.models import User
from app.schemas.auth import Token, TokenPayload
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.utils.exceptions import (
    AuthenticationError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)


class AuthService:
    """Business logic for authentication operations."""

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register(
        self,
        db: Session,
        user_data: UserCreate,
    ) -> UserResponse:
        """Register a new user."""

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
    ) -> Token:
        """Authenticate a user and issue an access token directly (no OTP step)."""

        user = self.verify_credentials(db, username_or_email, password)
        return Token(access_token=self.create_access_token(user))

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