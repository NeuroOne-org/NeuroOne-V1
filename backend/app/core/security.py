"""Password hashing and JSON Web Token helpers."""

from datetime import datetime, timedelta, timezone
from typing import Any

from passlib.context import CryptContext
from jose import jwt

from app.core.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt_sha256", "bcrypt"],
    deprecated=["bcrypt"],
)


def hash_password(password: str) -> str:
    """Hash a plaintext password using the configured password context."""

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored hash."""

    try:
        return pwd_context.verify(plain_password, hashed_password)
    except (TypeError, ValueError):
        return False


def create_access_token(claims: dict[str, Any]) -> str:
    """Create a signed access token from the supplied claims."""

    payload = claims.copy()
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    payload["exp"] = expires_at

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a signed access token."""

    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
