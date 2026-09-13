"""Business logic for attaching an MRI scan to a visit (ADR-006).

Authorization is delegated wholly to VisitService, the same pattern
AnalysisService and ReportService already use, so the ADR-002 ownership rule
stays in one place.
"""

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.scan import Scan
from app.models.user import User
from app.repositories.scan_repository import ScanRepository
from app.services.base_service import BaseService
from app.services.visit_service import VisitService
from app.storage.scan_storage import ScanStorage
from app.utils.exceptions import (
    ConflictError,
    EntityNotFoundError,
    ValidationApplicationError,
)

# Mirrors the frontend dropzone's accept list (mri-dropzone.tsx) -- the
# browser filter is a UX convenience only, so the server enforces the same
# allow-list since a client can send any extension or content-type it likes.
ALLOWED_SCAN_EXTENSIONS = {".nii", ".nii.gz", ".dcm", ".png", ".jpg", ".jpeg"}


def _scan_extension(filename: str) -> str:
    name = filename.lower()
    if name.endswith(".nii.gz"):
        return ".nii.gz"
    return Path(name).suffix


class ScanService(BaseService[ScanRepository]):
    """Attaches, and retrieves, the one scan a visit may have."""

    def __init__(
        self,
        repository: ScanRepository,
        visit_service: VisitService,
        storage: ScanStorage,
        *,
        max_size_bytes: int,
    ):
        super().__init__(repository)
        self.visit_service = visit_service
        self.storage = storage
        self.max_size_bytes = max_size_bytes

    def upload_scan(
        self,
        db: Session,
        visit_id: UUID,
        current_user: User,
        *,
        filename: str,
        content_type: str,
        content: bytes,
    ) -> Scan:
        """Attach a scan to a visit. One scan per visit (ADR-006 decision 2).

        The scan attaches to the visit, not the patient, so cross-visit
        comparison falls out of the trend machinery that already exists
        rather than needing its own history model.
        """

        visit = self.visit_service.get_visit(db, visit_id, current_user)

        if _scan_extension(filename) not in ALLOWED_SCAN_EXTENSIONS:
            raise ValidationApplicationError(
                "Unsupported scan file type. Accepted types: "
                + ", ".join(sorted(ALLOWED_SCAN_EXTENSIONS))
                + "."
            )
        if not content:
            raise ValidationApplicationError("An MRI scan file must not be empty.")
        if len(content) > self.max_size_bytes:
            raise ValidationApplicationError(
                f"The scan exceeds the {self.max_size_bytes} byte upload limit."
            )

        storage_key = self.storage.save(visit.id, filename, content)
        scan = Scan(
            visit_id=visit.id,
            uploaded_by_id=current_user.id,
            storage_key=storage_key,
            original_filename=filename,
            content_type=content_type,
            size_bytes=len(content),
            checksum=hashlib.sha256(content).hexdigest(),
            dimensions={},
            uploaded_at=datetime.now(timezone.utc),
        )

        try:
            return self.repository.create(db, scan)
        except ConflictError as exc:
            # The row never landed, so the file it referenced is now
            # orphaned -- clean it up rather than leaking storage on every
            # rejected re-upload.
            self.storage.delete(storage_key)
            raise ConflictError(
                "This visit already has a scan attached. A follow-up scan "
                "belongs to a new visit (ADR-006)."
            ) from exc
        except Exception:
            # Any other persistence failure (e.g. a transient DatabaseError)
            # still leaves the row unwritten, so the file must not outlive
            # the record it was meant to back.
            self.storage.delete(storage_key)
            raise

    def get_scan(
        self,
        db: Session,
        visit_id: UUID,
        current_user: User,
    ) -> Scan:
        """Retrieve the scan attached to a visit, if any."""

        self.visit_service.get_visit(db, visit_id, current_user)

        scan = self.repository.get_by_visit(db, visit_id)
        if scan is None:
            raise EntityNotFoundError("Scan", visit_id)

        return scan


__all__ = ["ScanService"]
