"""Service-boundary tests for account provisioning and bootstrap."""

import time
from datetime import datetime, timezone
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse
from app.services import otp_service
from app.services.auth_service import AuthService
from app.utils.exceptions import (
    AuthorizationError,
    InvalidCredentialsError,
    InvalidOtpError,
    UserAlreadyExistsError,
)


def teardown_function() -> None:
    otp_service._otp_store.clear()


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


def test_request_password_reset_sends_otp_for_active_user(monkeypatch) -> None:
    user_service = Mock()
    user = User(
        id=uuid4(),
        email="known@example.com",
        is_active=True,
        is_deleted=False,
    )
    user_service.get_user_by_email.return_value = user
    service = AuthService(user_service)
    sent = Mock()
    monkeypatch.setattr(otp_service, "generate_and_send_otp", sent)

    service.request_password_reset(Mock(), "known@example.com")

    sent.assert_called_once_with(
        identity="known@example.com",
        to_email="known@example.com",
    )


def test_request_password_reset_is_silent_for_unknown_or_inactive_email(
    monkeypatch,
) -> None:
    user_service = Mock()
    service = AuthService(user_service)
    sent = Mock()
    monkeypatch.setattr(otp_service, "generate_and_send_otp", sent)

    user_service.get_user_by_email.return_value = None
    service.request_password_reset(Mock(), "unknown@example.com")

    user_service.get_user_by_email.return_value = User(
        id=uuid4(),
        email="inactive@example.com",
        is_active=False,
        is_deleted=False,
    )
    service.request_password_reset(Mock(), "inactive@example.com")

    sent.assert_not_called()


def test_reset_password_updates_hash_on_valid_otp(monkeypatch) -> None:
    user_service = Mock()
    user = User(
        id=uuid4(),
        email="known@example.com",
        is_active=True,
        is_deleted=False,
        hashed_password="old-hash",
    )
    user_service.get_user_by_email.return_value = user
    service = AuthService(user_service)
    monkeypatch.setattr(otp_service, "verify_otp", Mock(return_value=True))

    service.reset_password(Mock(), "known@example.com", "123456", "brand-new-password")

    user_service.set_password.assert_called_once()
    args, _ = user_service.set_password.call_args
    assert args[1] is user
    assert service.verify_password("brand-new-password", args[2])


def test_reset_password_rejects_invalid_otp(monkeypatch) -> None:
    user_service = Mock()
    service = AuthService(user_service)
    monkeypatch.setattr(otp_service, "verify_otp", Mock(return_value=False))

    with pytest.raises(InvalidOtpError):
        service.reset_password(Mock(), "known@example.com", "000000", "brand-new-password")

    user_service.set_password.assert_not_called()


def test_reset_password_rejects_when_user_no_longer_exists(monkeypatch) -> None:
    user_service = Mock()
    user_service.get_user_by_email.return_value = None
    service = AuthService(user_service)
    monkeypatch.setattr(otp_service, "verify_otp", Mock(return_value=True))

    with pytest.raises(InvalidOtpError):
        service.reset_password(Mock(), "known@example.com", "123456", "brand-new-password")


def test_otp_login_wrong_password_does_not_burn_the_code() -> None:
    user_service = Mock()
    service = AuthService(user_service)
    user = User(
        id=uuid4(),
        username="known-user",
        email="known@example.com",
        hashed_password=service.hash_password("correct-password"),
        role=UserRole.CLINICIAN,
        is_active=True,
        is_deleted=False,
    )
    user_service.get_user_by_email.return_value = user
    otp_service._otp_store["known@example.com"] = otp_service._OtpEntry(
        code="123456",
        expires_at=time.time() + otp_service.OTP_TTL_SECONDS,
    )

    with pytest.raises(InvalidCredentialsError):
        service.verify_otp_login(Mock(), "known@example.com", "123456", "wrong-password")
    with pytest.raises(InvalidOtpError):
        service.verify_otp_login(Mock(), "known@example.com", "000000", "correct-password")

    token = service.verify_otp_login(
        Mock(), "known@example.com", "123456", "correct-password"
    )
    assert service.verify_access_token(token.access_token).sub == user.id
