"""Report persistence operations."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.report import Report
from app.repositories.base_repository import BaseRepository


class ReportRepository(BaseRepository[Report]):
    """Provide report-specific queries in addition to common CRUD."""

    def __init__(self):
        super().__init__(model=Report)

    def _analysis_statement(self, analysis_id: UUID):
        return select(Report).where(
            Report.analysis_id == analysis_id,
            Report.is_deleted.is_(False),
        )

    def get_by_analysis(
        self,
        db: Session,
        analysis_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Report]:
        """Return an analysis's reports, newest first."""

        statement = (
            self._analysis_statement(analysis_id)
            .order_by(Report.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(statement).all())

    def count_by_analysis(self, db: Session, analysis_id: UUID) -> int:
        """Count an analysis's active reports."""

        statement = self._analysis_statement(analysis_id)
        count_statement = select(func.count()).select_from(statement.subquery())
        return db.scalar(count_statement) or 0


__all__ = ["ReportRepository"]
