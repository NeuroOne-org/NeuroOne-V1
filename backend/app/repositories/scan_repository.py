"""Scan persistence operations."""
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.scan import Scan
from app.repositories.base_repository import BaseRepository


class ScanRepository(BaseRepository[Scan]):
    """Provide scan-specific queries in addition to common CRUD."""

    def __init__(self):
        super().__init__(model=Scan)

    def get_by_visit(self, db: Session, visit_id: UUID) -> Scan | None:
        """Return the active scan attached to a visit, if any."""

        statement = select(Scan).where(
            Scan.visit_id == visit_id,
            Scan.is_deleted.is_(False),
        )
        return db.scalar(statement)


__all__ = ["ScanRepository"]
