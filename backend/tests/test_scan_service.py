"""Unit tests for ScanService (ADR-006).

Mirrors test_report_service.py's shape: authorization delegates wholly to
VisitService, and a conflict (a visit that already has a scan) must not
leave an orphaned file in storage.
"""

import gzip
import io
from datetime import datetime, timezone
from unittest.mock import Mock
from uuid import uuid4

import nibabel
import numpy as np
import pydicom
import pytest
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian

from app.models.user import User, UserRole
from app.models.visit import Visit, VisitStatus
from app.services.scan_service import ScanService
from app.utils.exceptions import (
    ConflictError,
    DatabaseError,
    EntityNotFoundError,
    ValidationApplicationError,
)


NOW = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)


def _dicom(rows: int = 3, columns: int = 4) -> bytes:
    meta = FileMetaDataset()
    meta.TransferSyntaxUID = ExplicitVRLittleEndian
    ds = FileDataset("scan.dcm", {}, file_meta=meta, preamble=bytes(128))
    ds.Rows, ds.Columns = rows, columns
    ds.BitsAllocated, ds.BitsStored, ds.HighBit = 8, 8, 7
    ds.SamplesPerPixel, ds.PixelRepresentation = 1, 0
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelData = bytes(rows * columns)
    out = io.BytesIO()
    pydicom.dcmwrite(out, ds)
    return out.getvalue()


DICOM = _dicom()
NIFTI_GZ = gzip.compress(
    nibabel.Nifti1Image(np.zeros((5, 6, 7), dtype=np.uint8), np.eye(4)).to_bytes()
)


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
        content=DICOM,
    )

    import hashlib

    assert scan.checksum == hashlib.sha256(DICOM).hexdigest()
    assert scan.size_bytes == len(DICOM)
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
        content=DICOM,
    )

    storage.save.assert_called_once_with(visit.id, "scan.dcm", DICOM)


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
        content=DICOM,
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
            content=DICOM,
        )

    storage.delete.assert_called_once_with(storage.save.return_value)


def test_a_non_conflict_database_error_also_cleans_up_storage() -> None:
    """Any persistence failure orphans the file, not just a conflict."""
    service, repository, visit_service, storage = _service()
    visit = _visit()
    visit_service.get_visit.return_value = visit
    repository.create.side_effect = DatabaseError("connection lost")

    with pytest.raises(DatabaseError):
        service.upload_scan(
            Mock(),
            visit.id,
            _user(),
            filename="scan.dcm",
            content_type="application/dicom",
            content=DICOM,
        )

    storage.delete.assert_called_once_with(storage.save.return_value)


def test_an_unsupported_file_type_is_rejected() -> None:
    service, repository, visit_service, storage = _service()
    visit = _visit()
    visit_service.get_visit.return_value = visit

    with pytest.raises(ValidationApplicationError):
        service.upload_scan(
            Mock(),
            visit.id,
            _user(),
            filename="scan.exe",
            content_type="application/octet-stream",
            content=b"x",
        )

    storage.save.assert_not_called()
    repository.create.assert_not_called()


def test_a_double_extension_nifti_file_is_accepted() -> None:
    service, repository, visit_service, storage = _service()
    visit = _visit()
    visit_service.get_visit.return_value = visit
    repository.create.side_effect = lambda db, obj: obj

    scan = service.upload_scan(
        Mock(),
        visit.id,
        _user(),
        filename="brain.nii.gz",
        content_type="application/octet-stream",
        content=NIFTI_GZ,
    )

    assert scan.original_filename == "brain.nii.gz"


def test_uploading_records_the_parsed_dimensions() -> None:
    service, repository, visit_service, storage = _service()
    visit_service.get_visit.return_value = _visit()
    repository.create.side_effect = lambda db, obj: obj

    dicom = service.upload_scan(
        Mock(), uuid4(), _user(),
        filename="scan.dcm", content_type="application/dicom", content=DICOM,
    )
    nifti = service.upload_scan(
        Mock(), uuid4(), _user(),
        filename="brain.nii.gz", content_type="application/gzip", content=NIFTI_GZ,
    )

    # Audit HB-15: these used to be stored as {}.
    assert dicom.dimensions == {"width": 4, "height": 3, "slices": 1}
    assert nifti.dimensions == {"width": 5, "height": 6, "slices": 7}


@pytest.mark.parametrize("filename", ["scan.dcm", "brain.nii", "brain.nii.gz", "scan.png"])
def test_bytes_that_are_not_the_named_format_are_rejected(filename) -> None:
    service, repository, visit_service, storage = _service()
    visit_service.get_visit.return_value = _visit()

    with pytest.raises(ValidationApplicationError, match="could not be read"):
        service.upload_scan(
            Mock(), uuid4(), _user(),
            filename=filename, content_type="application/octet-stream", content=b"x",
        )

    storage.save.assert_not_called()
    repository.create.assert_not_called()


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
