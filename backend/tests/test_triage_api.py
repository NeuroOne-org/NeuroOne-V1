"""Contract tests for the triage endpoint (ADR-006)."""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.dependencies import get_current_active_user, get_db, get_triage_service
from app.models.user import User, UserRole
from app.schemas.triage import TriageEntry
from main import app


def _user(role: UserRole = UserRole.CLINICIAN) -> User:
    now = datetime.now(timezone.utc)
    return User(
        id=uuid4(),
        username=f"user-{uuid4().hex[:8]}",
        email=f"{uuid4().hex[:8]}@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="not-returned",
        role=role,
        is_active=True,
        is_verified=True,
        is_deleted=False,
        created_at=now,
        updated_at=now,
    )


def _entry(**overrides) -> TriageEntry:
    payload = {
        "patient_id": uuid4(),
        "patient_first_name": "Ada",
        "patient_last_name": "Lovelace",
        "has_open_early_watch": False,
        "has_worsening_trend": False,
        "awaiting_sign_off": False,
    }
    payload.update(overrides)
    return TriageEntry(**payload)


def _db_override():
    yield object()


def _client(current_user: User, service_stub) -> TestClient:
    app.dependency_overrides[get_db] = _db_override
    app.dependency_overrides[get_current_active_user] = lambda: current_user
    app.dependency_overrides[get_triage_service] = lambda: service_stub
    return TestClient(app, raise_server_exceptions=False)


def teardown_function() -> None:
    app.dependency_overrides.clear()


def test_the_queue_returns_the_pagination_envelope() -> None:
    clinician = _user()

    class ServiceStub:
        def list_queue(self, db, current_user, skip, limit):
            assert current_user is clinician
            assert skip == 20
            assert limit == 20
            return [_entry()], 41

    response = _client(clinician, ServiceStub()).get(
        "/api/v1/triage", params={"page": 2, "page_size": 20}
    )

    assert response.status_code == 200
    assert response.json()["pagination"] == {
        "page": 2,
        "page_size": 20,
        "total_records": 41,
        "total_pages": 3,
    }


def test_an_entry_carries_no_field_that_frames_output_as_a_measurement() -> None:
    """FR-04: no stat tile, no aggregate confidence number."""
    clinician = _user()
    entry = _entry(has_open_early_watch=True)

    class ServiceStub:
        def list_queue(self, db, current_user, skip, limit):
            return [entry], 1

    response = _client(clinician, ServiceStub()).get("/api/v1/triage")

    body = response.json()["items"][0]
    assert body["has_open_early_watch"] is True
    for forbidden in ("confidence", "certainty", "average", "score"):
        assert forbidden not in body


def test_default_pagination_is_page_one() -> None:
    clinician = _user()
    seen = []

    class ServiceStub:
        def list_queue(self, db, current_user, skip, limit):
            seen.append((skip, limit))
            return [], 0

    response = _client(clinician, ServiceStub()).get("/api/v1/triage")

    assert response.status_code == 200
    assert seen == [(0, 20)]
