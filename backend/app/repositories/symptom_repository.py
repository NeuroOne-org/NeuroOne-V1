"""Symptom persistence operations."""
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.symptom import Symptom
from app.repositories.base_repository import BaseRepository


class SymptomRepository(BaseRepository[Symptom]):
    """Provide symptom-specific queries in addition to common CRUD operations."""

    def __init__(self):
        super().__init__(model=Symptom)

    def _visit_statement(self, visit_id: UUID):
        return select(Symptom).where(
            Symptom.visit_id == visit_id,
            Symptom.is_deleted.is_(False),
        )

    def get_by_visit(
        self,
        db: Session,
        visit_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Symptom]:
        """Return a visit's active symptoms in recording order."""
        statement = (
            self._visit_statement(visit_id)
            .order_by(Symptom.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(statement).all())

    def count_by_visit(self, db: Session, visit_id: UUID) -> int:
        """Count a visit's active symptoms."""
        statement = self._visit_statement(visit_id)
        count_statement = select(func.count()).select_from(statement.subquery())
        return db.scalar(count_statement) or 0
