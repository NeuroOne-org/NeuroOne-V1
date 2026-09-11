"""Unit tests for ScanService (ADR-006).

Mirrors test_report_service.py's shape: authorization delegates wholly to
VisitService, and a conflict (a visit that already has a scan) must not
leave an orphaned file in storage.
"""

from datetime import datetime, timezone
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.models.user import User, UserRole
from app.models.visit import Visit, VisitStatus
from app.services.scan_service import ScanService
from app.utils.exceptions import (
    ConflictError,
    EntityNotFoundError,
    ValidationApplicationError,
)


NOW = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)


def _user(role: UserRole = UserRole.CLINICIAN) -> User:
    return User(
        id=uuid4(),
        username=f"user-{uuid4().hex[:8]}",
        email=f"{uuid4().hex[:8]}@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hash",
        role=role,
        is_active=True,
        is_verified=True,
        is_deleted=False,
    )


def _visit(**overrides) -> Visit:
    payload = {
        "id": uuid4(),
        "patient_id": uuid4(),
        "visit_date": NOW,
        "chief_complaint": "progressive tremor",
        "vitals": {},
        "status": VisitStatus.DRAFT,
    }
    payload.update(overrides)
    return Visit(**payload)


def _service():
    repository = Mock()
    visit_service = Mock()
    storage = Mock()
    storage.save.return_value = "visit-id/generated-key-scan.dcm"
    service = ScanService(repository, visit_service, storage, max_size_bytes=1024)
    return service, repository, visit_service, storage


def _deny_visit(visit_service):
    visit_service.get_visit.side_effect = EntityNotFoundError("Visit", uuid4())


# --------------------------------------------------------------------------
# Upload
# --------------------------------------------------------------------------


def test_uploading_persists_a_checksum_of_the_actual_bytes() -> None:
    service, repository, visit_service, storage = _service()
    visit = _visit()
    visit_service.get_visit.return_value = visit
    repository.create.side_effect = lambda db, obj: obj

    scan = service.upload_scan(
        Mock(),
        visit.id,
        _user(),
        filename="scan.dcm",
        content_type="application/dicom",
        content=b"scan-bytes",
    )

    import hashlib

    assert scan.checksum == hashlib.sha256(b"scan-bytes").hexdigest()
    assert scan.size_bytes == len(b"scan-bytes")
    assert scan.visit_id == visit.id


def test_uploading_saves_to_storage_before_persisting() -> None:
    service, repository, visit_service, storage = _service()
    visit = _visit()
    visit_service.get_visit.return_value = visit
    repository.create.side_effect = lambda db, obj: obj

    service.upload_scan(
        Mock(),
        visit.id,
        _user(),
        filename="scan.dcm",
        content_type="application/dicom",
        content=b"scan-bytes",
    )

    storage.save.assert_called_once_with(visit.id, "scan.dcm", b"scan-bytes")


def test_uploading_records_the_uploading_clinician() -> None:
    service, repository, visit_service, storage = _service()
    visit = _visit()
    clinician = _user()
    visit_service.get_visit.return_value = visit
    repository.create.side_effect = lambda db, obj: obj

    scan = service.upload_scan(
        Mock(),
        visit.id,
        clinician,
        filename="scan.dcm",
        content_type="application/dicom",
        content=b"x",
    )

    assert scan.uploaded_by_id == clinician.id


def test_uploading_to_another_clinicians_visit_is_denied() -> None:
    service, repository, visit_service, storage = _service()
    _deny_visit(visit_service)

    with pytest.raises(EntityNotFoundError):
        service.upload_scan(
            Mock(),
            uuid4(),
            _user(),
            filename="scan.dcm",
            content_type="application/dicom",
            content=b"x",
        )

    storage.save.assert_not_called()
    repository.create.assert_not_called()


def test_an_empty_file_is_rejected() -> None:
    service, repository, visit_service, storage = _service()
    visit = _visit()
    visit_service.get_visit.return_value = visit

    with pytest.raises(ValidationApplicationError):
        service.upload_scan(
            Mock(),
            visit.id,
            _user(),
            filename="scan.dcm",
            content_type="application/dicom",
            content=b"",
        )

    storage.save.assert_not_called()


def test_an_oversized_file_is_rejected() -> None:
    service, repository, visit_service, storage = _service()
    visit = _visit()
    visit_service.get_visit.return_value = visit

    with pytest.raises(ValidationApplicationError):
        service.upload_scan(
            Mock(),
            visit.id,
            _user(),
            filename="scan.dcm",
            content_type="application/dicom",
            content=b"x" * 2048,
        )

    storage.save.assert_not_called()


def test_a_second_scan_on_the_same_visit_is_a_conflict_and_cleans_up_storage() -> None:
    """ADR-006 decision 2: one scan per visit."""
    service, repository, visit_service, storage = _service()
    visit = _visit()
    visit_service.get_visit.return_value = visit
    repository.create.side_effect = ConflictError("duplicate")

    with pytest.raises(ConflictError):
        service.upload_scan(
            Mock(),
            visit.id,
            _user(),
            filename="scan.dcm",
            content_type="application/dicom",
            content=b"x",
        )

    storage.delete.assert_called_once_with(storage.save.return_value)


# --------------------------------------------------------------------------
# Retrieval
# --------------------------------------------------------------------------


def test_get_scan_returns_the_visits_scan() -> None:
    service, repository, visit_service, storage = _service()
    visit = _visit()
    scan = Mock()
    visit_service.get_visit.return_value = visit
    repository.get_by_visit.return_value = scan

    assert service.get_scan(Mock(), visit.id, _user()) is scan


def test_get_scan_on_a_scanless_visit_is_a_missing_scan() -> None:
    service, repository, visit_service, storage = _service()
    visit = _visit()
    visit_service.get_visit.return_value = visit
    repository.get_by_visit.return_value = None

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.get_scan(Mock(), visit.id, _user())

    assert exc_info.value.entity == "Scan"


def test_get_scan_on_another_clinicians_visit_is_denied() -> None:
    service, repository, visit_service, storage = _service()
    _deny_visit(visit_service)

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.get_scan(Mock(), uuid4(), _user())

    assert exc_info.value.entity == "Visit"
    repository.get_by_visit.assert_not_called()
