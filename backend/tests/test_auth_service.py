"""Service-boundary tests for account provisioning and bootstrap."""

from datetime import datetime, timezone
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.utils.exceptions import (
    AuthorizationError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)


def _payload(role: UserRole = UserRole.CLINICIAN) -> UserCreate:
    return UserCreate(
        username="new-user",
        email="new-user@example.com",
        first_name="New",
        last_name="User",
        password="safe-password",
        role=role,
    )


def _response(role: UserRole) -> UserResponse:
    now = datetime.now(timezone.utc)
    return UserResponse(
        id=uuid4(),
        username="new-user",
        email="new-user@example.com",
        first_name="New",
        last_name="User",
        role=role,
        is_active=True,
        is_verified=False,
        created_at=now,
        updated_at=now,
    )


def test_service_rejects_non_admin_provisioning() -> None:
    service = AuthService(Mock())
    clinician = User(role=UserRole.CLINICIAN)

    with pytest.raises(AuthorizationError):
        service.provision_user(Mock(), _payload(), requested_by=clinician)


def test_bootstrap_creates_only_when_no_admin_exists(monkeypatch) -> None:
    user_service = Mock()
    user_service.repository.get_first_by_role.return_value = None
    service = AuthService(user_service)
    expected = _response(UserRole.ADMIN)
    create = Mock(return_value=expected)
    monkeypatch.setattr(service, "_create_user", create)

    assert service.bootstrap_admin(Mock(), _payload(UserRole.ADMIN)) is expected
    create.assert_called_once()

    user_service.repository.get_first_by_role.return_value = User(
        role=UserRole.ADMIN
    )
    with pytest.raises(UserAlreadyExistsError):
        service.bootstrap_admin(Mock(), _payload(UserRole.ADMIN))


def test_login_validates_real_password_hash_and_hides_user_existence() -> None:
    user_service = Mock()
    service = AuthService(user_service)
    user = User(
        id=uuid4(),
        username="known-user",
        email="known-user@example.com",
        hashed_password=service.hash_password("correct-password"),
        role=UserRole.CLINICIAN,
        is_active=True,
        is_deleted=False,
    )
    user_service.get_user_by_username.return_value = user

    token = service.login(Mock(), "known-user", "correct-password")
    assert service.verify_access_token(token.access_token).sub == user.id

    with pytest.raises(InvalidCredentialsError) as wrong_password:
        service.login(Mock(), "known-user", "wrong-password")

    user_service.get_user_by_username.return_value = None
    with pytest.raises(InvalidCredentialsError) as unknown_user:
        service.login(Mock(), "unknown-user", "wrong-password")

    assert str(wrong_password.value) == str(unknown_user.value)
