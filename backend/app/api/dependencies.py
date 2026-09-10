"""Reusable FastAPI dependencies for database and access control."""

from collections.abc import Callable, Generator
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models import User
from app.models.user import UserRole
from app.repositories.patient_repository import PatientRepository
from app.repositories.symptom_repository import SymptomRepository
from app.repositories.user_repository import UserRepository
from app.repositories.visit_repository import VisitRepository
from app.services.auth_service import AuthService
from app.services.patient_service import PatientService
from app.services.user_service import UserService
from app.services.visit_service import VisitService
from app.utils.exceptions import AuthenticationError, AuthorizationError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

_user_service = UserService(UserRepository())
_patient_service = PatientService(PatientRepository(), UserRepository())
_visit_service = VisitService(
    VisitRepository(),
    SymptomRepository(),
    _patient_service,
)


def get_db() -> Generator[Session, None, None]:
    """Provide a database session and always close it after the request."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service() -> UserService:
    """Provide the configured user service."""

    return _user_service


def get_patient_service() -> PatientService:
    """Provide the configured patient service."""

    return _patient_service


def get_visit_service() -> VisitService:
    """Provide the configured visit service."""

    return _visit_service


def get_auth_service(
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> AuthService:
    """Provide the configured authentication service."""

    return AuthService(user_service)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    """Validate the bearer token and return its associated user."""

    payload = auth_service.verify_access_token(token)
    user = user_service.get_user(db, payload.sub)

    if user is None or user.is_deleted:
        raise AuthenticationError("Authenticated user no longer exists.")

    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Return the current user only when the account is active."""

    if not current_user.is_active:
        raise AuthenticationError("User account is inactive.")

    return current_user


def require_roles(*allowed_roles: UserRole) -> Callable[..., User]:
    """Create a dependency that permits only the supplied user roles."""

    allowed = frozenset(allowed_roles)

    def role_dependency(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        if current_user.role not in allowed:
            raise AuthorizationError(
                "You do not have permission to perform this action."
            )

        return current_user

    return role_dependency


get_current_admin = require_roles(UserRole.ADMIN)
get_current_clinician = require_roles(UserRole.CLINICIAN)


def require_admin(
    current_user: Annotated[User, Depends(get_current_admin)],
) -> User:
    """Require the current user to have the administrator role."""

    return current_user


def require_clinician(
    current_user: Annotated[User, Depends(get_current_clinician)],
) -> User:
    """Require the current user to have the clinician role."""

    return current_user


__all__ = [
    "get_auth_service",
    "get_current_active_user",
    "get_current_admin",
    "get_current_clinician",
    "get_current_user",
    "get_db",
    "get_patient_service",
    "get_user_service",
    "get_visit_service",
    "oauth2_scheme",
    "require_admin",
    "require_clinician",
    "require_roles",
]
