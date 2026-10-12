"""Adapter binding the `staging_results` table to `StagingStore` (ADR-008).

Opens one short-lived session per call, like `StorageScanImages`, so a
stored stage commits independently of the analysis that produced it: a
failed analysis still keeps the paid staging call it already made. That
touches no clinical record -- a stage is derived from the scan, not part of
the patient's case.
"""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import SessionLocal
from app.models.staging import StagingRecord
from app.schemas.imaging import StagingResult


class SessionStagingStore:
    def __init__(self, session_factory: sessionmaker[Session] = SessionLocal):
        self._session_factory = session_factory

    def get(self, checksum: str, model_name: str) -> StagingResult | None:
        with self._session_factory() as db:
            record = db.scalar(
                select(StagingRecord).where(
                    StagingRecord.checksum == checksum,
                    StagingRecord.model_name == model_name,
                )
            )
            # Re-validated, so a row written under an older contract fails
            # here as a staging error instead of reaching a clinician.
            return StagingResult.model_validate(record.result) if record else None

    def put(self, checksum: str, result: StagingResult) -> None:
        with self._session_factory() as db:
            db.add(
                StagingRecord(
                    checksum=checksum,
                    model_name=result.model_name,
                    result=result.model_dump(mode="json"),
                )
            )
            try:
                db.commit()
            except IntegrityError:
                # A concurrent analysis stored this scan first. Both results
                # came from the same model on the same bytes; keep the first.
                db.rollback()


__all__ = ["SessionStagingStore"]
