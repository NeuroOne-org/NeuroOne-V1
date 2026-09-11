"""Contract tests for the scan endpoints (ADR-006)."""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.dependencies import get_current_active_user, get_db, get_scan_service
from app.models.scan import Scan
from app.models.user import User, UserRole
from app.utils.exceptions import ConflictError, EntityNotFoundError
from main import app


NOW = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)


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


def _scan(visit_id=None, uploaded_by_id=None) -> Scan:
    now = datetime.now(timezone.utc)
    return Scan(
        id=uuid4(),
        visit_id=visit_id or uuid4(),
        uploaded_by_id=uploaded_by_id or uuid4(),
        storage_key="irrelevant/key.dcm",
        original_filename="scan.dcm",
        content_type="application/dicom",
        size_bytes=10,
        checksum="a" * 64,
        dimensions={},
        uploaded_at=NOW,
        created_at=now,
        updated_at=now,
    )


def _db_override():
    yield object()


def _client(current_user: User, service_stub) -> TestClient:
    app.dependency_overrides[get_db] = _db_override
    app.dependency_overrides[get_current_active_user] = lambda: current_user
    app.dependency_overrides[get_scan_service] = lambda: service_stub
    return TestClient(app, raise_server_exceptions=False)


def teardown_function() -> None:
    app.dependency_overrides.clear()


# --------------------------------------------------------------------------
# Upload
# --------------------------------------------------------------------------


def test_uploading_a_scan_returns_201_with_metadata() -> None:
    clinician = _user()
    visit_id = uuid4()
    created = _scan(visit_id, clinician.id)

    class ServiceStub:
        def upload_scan(self, db, vid, current_user, *, filename, content_type, content):
            assert vid == visit_id
            assert current_user is clinician
            assert filename == "scan.dcm"
            assert content == b"scan-bytes"
            return created

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/visits/{visit_id}/scan",
        files={"file": ("scan.dcm", b"scan-bytes", "application/dicom")},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["visit_id"] == str(visit_id)
    assert body["uploaded_by_id"] == str(clinician.id)
    assert "storage_key" not in body


def test_uploading_to_another_clinicians_visit_is_404() -> None:
    clinician = _user()

    class ServiceStub:
        def upload_scan(self, db, vid, current_user, *, filename, content_type, content):
            raise EntityNotFoundError("Visit", vid)

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/visits/{uuid4()}/scan",
        files={"file": ("scan.dcm", b"x", "application/dicom")},
    )

    assert response.status_code == 404


def test_uploading_a_second_scan_to_the_same_visit_is_409() -> None:
    clinician = _user()

    class ServiceStub:
        def upload_scan(self, db, vid, current_user, *, filename, content_type, content):
            raise ConflictError("This visit already has a scan attached.")

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/visits/{uuid4()}/scan",
        files={"file": ("scan.dcm", b"x", "application/dicom")},
    )

    assert response.status_code == 409


# --------------------------------------------------------------------------
# Retrieval
# --------------------------------------------------------------------------


def test_getting_a_visits_scan_succeeds() -> None:
    clinician = _user()
    scan = _scan()

    class ServiceStub:
        def get_scan(self, db, visit_id, current_user):
            return scan

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/visits/{scan.visit_id}/scan"
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(scan.id)


def test_getting_a_scan_on_a_scanless_visit_is_404() -> None:
    clinician = _user()

    class ServiceStub:
        def get_scan(self, db, visit_id, current_user):
            raise EntityNotFoundError("Scan", visit_id)

    response = _client(clinician, ServiceStub()).get(f"/api/v1/visits/{uuid4()}/scan")

    assert response.status_code == 404
