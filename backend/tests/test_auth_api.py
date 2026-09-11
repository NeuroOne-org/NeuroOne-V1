"""Integration-style contract tests for authentication endpoints."""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi.testclient import TestClient
from jose import jwt

from app.api.dependencies import (
    get_auth_service,
    get_current_active_user,
    get_db,
    get_user_service,
    require_admin,
)
from app.core.security import create_access_token
from main import app
from app.core.config import settings
from app.models.user import User, UserRole
from app.schemas.auth import Token
from app.schemas.user import UserResponse
from app.utils.exceptions import InvalidCredentialsError, UserAlreadyExistsError


def _user(role: UserRole = UserRole.CLINICIAN) -> User:
    now = datetime.now(timezone.utc)
    return User(
        id=uuid4(),
        username=f"user-{uuid4().hex[:8]}",
        email=f"{uuid4().hex[:8]}@example.com",
        first_name="Test",
        last_name="Clinician",
        hashed_password="not-returned",
        role=role,
        is_active=True,
        is_verified=True,
        is_deleted=False,
        created_at=now,
        updated_at=now,
    )


def _db_override():
    yield object()


def _client() -> TestClient:
    app.dependency_overrides[get_db] = _db_override
    return TestClient(app, raise_server_exceptions=False)


def teardown_function() -> None:
    app.dependency_overrides.clear()


def test_login_success_and_invalid_credentials_share_safe_contract() -> None:
    class AuthStub:
        def login(self, db, username, password):
            if password != "correct-password":
                raise InvalidCredentialsError("Invalid username/email or password.")
            return Token(access_token="signed-token")

    app.dependency_overrides[get_auth_service] = lambda: AuthStub()
    client = _client()

    success = client.post(
        "/api/v1/auth/login",
        json={"username": "clinician", "password": "correct-password"},
    )
    failure = client.post(
        "/api/v1/auth/login",
        json={"username": "unknown", "password": "wrong-password"},
    )

    assert success.status_code == 200
    assert success.json() == {"access_token": "signed-token", "token_type": "bearer"}
    assert failure.status_code == 401
    assert failure.json() == {
        "message": "Invalid username/email or password.",
        "error_code": "authentication_error",
        "details": None,
    }


def test_me_requires_authentication_and_returns_current_user() -> None:
    current_user = _user()
    client = _client()

    missing = client.get("/api/v1/auth/me")
    app.dependency_overrides[get_current_active_user] = lambda: current_user
    success = client.get("/api/v1/auth/me")

    assert missing.status_code == 401
    assert missing.json()["error_code"] == "authentication_error"
    assert success.status_code == 200
    assert success.json()["id"] == str(current_user.id)
    assert success.json()["email"] == current_user.email
    assert success.json()["role"] == "clinician"


def test_admin_can_create_user_without_returning_password() -> None:
    admin = _user(UserRole.ADMIN)
    created = _user(UserRole.CLINICIAN)

    class AuthStub:
        def provision_user(self, db, payload, *, requested_by):
            assert requested_by is admin
            return UserResponse.model_validate(created)

    app.dependency_overrides[require_admin] = lambda: admin
    app.dependency_overrides[get_auth_service] = lambda: AuthStub()
    client = _client()
    response = client.post(
        "/api/v1/admin/users",
        json={
            "username": "new-clinician",
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "Clinician",
            "password": "very-safe-password",
            "role": "clinician",
        },
    )

    assert response.status_code == 201
    assert response.json()["role"] == "clinician"
    assert "password" not in response.json()
    assert "hashed_password" not in response.json()


def test_duplicate_user_is_conflict() -> None:
    class AuthStub:
        def provision_user(self, db, payload, *, requested_by):
            raise UserAlreadyExistsError("A user with this email already exists.")

    app.dependency_overrides[require_admin] = lambda: _user(UserRole.ADMIN)
    app.dependency_overrides[get_auth_service] = lambda: AuthStub()
    client = _client()
    response = client.post(
        "/api/v1/admin/users",
        json={
            "username": "duplicate",
            "email": "duplicate@example.com",
            "first_name": "Dupe",
            "last_name": "User",
            "password": "very-safe-password",
        },
    )

    assert response.status_code == 409
    assert response.json()["error_code"] == "conflict"


def test_public_registration_route_does_not_exist() -> None:
    response = _client().post("/api/v1/auth/register", json={})

    assert response.status_code == 404


def test_clinician_cannot_create_users() -> None:
    app.dependency_overrides[get_current_active_user] = lambda: _user(
        UserRole.CLINICIAN
    )
    client = _client()
    response = client.post(
        "/api/v1/admin/users",
        json={
            "username": "forbidden-create",
            "email": "forbidden@example.com",
            "first_name": "No",
            "last_name": "Access",
            "password": "very-safe-password",
        },
    )

    assert response.status_code == 403
    assert response.json()["error_code"] == "authorization_error"


def test_invalid_token_returns_controlled_401() -> None:
    response = _client().get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer definitely-not-a-token"},
    )

    assert response.status_code == 401
    assert response.json()["error_code"] == "authentication_error"


def test_expired_token_returns_controlled_401() -> None:
    expired_token = jwt.encode(
        {
            "sub": str(uuid4()),
            "username": "expired",
            "role": "clinician",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    response = _client().get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )

    assert response.status_code == 401
    assert response.json()["error_code"] == "authentication_error"


def test_forgot_password_always_returns_the_same_generic_message() -> None:
    class AuthStub:
        def __init__(self):
            self.calls: list[str] = []

        def request_password_reset(self, db, email):
            self.calls.append(email)

    stub = AuthStub()
    app.dependency_overrides[get_auth_service] = lambda: stub
    client = _client()

    known = client.post(
        "/api/v1/auth/forgot-password",
        json={"email": "known@example.com"},
    )
    unknown = client.post(
        "/api/v1/auth/forgot-password",
        json={"email": "unknown@example.com"},
    )

    assert known.status_code == 200
    assert unknown.status_code == 200
    assert known.json() == unknown.json()
    assert stub.calls == ["known@example.com", "unknown@example.com"]


def test_reset_password_success_and_invalid_otp() -> None:
    from app.utils.exceptions import InvalidOtpError

    class AuthStub:
        def reset_password(self, db, email, otp, new_password):
            if otp != "123456":
                raise InvalidOtpError("Invalid or expired verification code.")

    app.dependency_overrides[get_auth_service] = lambda: AuthStub()
    client = _client()

    success = client.post(
        "/api/v1/auth/reset-password",
        json={
            "email": "known@example.com",
            "otp": "123456",
            "new_password": "brand-new-password",
        },
    )
    failure = client.post(
        "/api/v1/auth/reset-password",
        json={
            "email": "known@example.com",
            "otp": "000000",
            "new_password": "brand-new-password",
        },
    )

    assert success.status_code == 200
    assert failure.status_code == 422
    assert failure.json()["error_code"] == "invalid_otp"


def test_valid_token_loads_current_user_from_service() -> None:
    current_user = _user()

    class UserServiceStub:
        def get_user(self, db, user_id):
            assert user_id == current_user.id
            return current_user

    app.dependency_overrides[get_user_service] = lambda: UserServiceStub()
    token = create_access_token(
        {
            "sub": str(current_user.id),
            "username": current_user.username,
            "role": current_user.role.value,
        }
    )
    response = _client().get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(current_user.id)
