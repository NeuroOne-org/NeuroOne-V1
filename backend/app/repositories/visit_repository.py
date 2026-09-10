"""Clinical case / visit persistence operations."""
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.symptom import Symptom
from app.models.visit import Visit, VisitStatus
from app.repositories.base_repository import BaseRepository


class VisitRepository(BaseRepository[Visit]):
    """Provide visit-specific queries in addition to common CRUD operations."""

    def __init__(self):
        super().__init__(model=Visit)

    def _with_symptoms(self, statement):
        """Eager-load each visit's live symptoms in one extra query.

        selectinload rather than joinedload: the relationship is one-to-many,
        so joining would fan out rows and break LIMIT. This keeps every visit
        query at exactly two SELECTs regardless of how many visits come back.

        The loader criteria filters soft-deleted symptoms inside the eager
        query -- a plain relationship load would return is_deleted=True rows.
        """
        return statement.options(
            selectinload(Visit.symptoms.and_(Symptom.is_deleted.is_(False)))
        )

    def _patient_statement(
        self,
        patient_id: UUID,
        status: VisitStatus | None = None,
    ):
        statement = select(Visit).where(
            Visit.patient_id == patient_id,
            Visit.is_deleted.is_(False),
        )
        if status is not None:
            statement = statement.where(Visit.status == status)
        return statement

    def get_with_symptoms(self, db: Session, visit_id: UUID) -> Visit | None:
        """Return an active visit with its live symptoms loaded."""
        statement = self._with_symptoms(
            select(Visit).where(
                Visit.id == visit_id,
                Visit.is_deleted.is_(False),
            )
        )
        return db.scalar(statement)

    def get_by_patient(
        self,
        db: Session,
        patient_id: UUID,
        skip: int = 0,
        limit: int = 100,
        status: VisitStatus | None = None,
    ) -> list[Visit]:
        """Return a patient's active visits, newest first."""
        statement = (
            self._with_symptoms(self._patient_statement(patient_id, status))
            .order_by(Visit.visit_date.desc(), Visit.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(statement).unique().all())

    def count_by_patient(
        self,
        db: Session,
        patient_id: UUID,
        status: VisitStatus | None = None,
    ) -> int:
        """Count a patient's active visits."""
        statement = self._patient_statement(patient_id, status)
        count_statement = select(func.count()).select_from(statement.subquery())
        return db.scalar(count_statement) or 0

    def get_history(
        self,
        db: Session,
        patient_id: UUID,
        *,
        limit: int = 10,
        newest_first: bool = True,
        exclude_visit_id: UUID | None = None,
    ) -> list[Visit]:
        """Return a patient's visit history ordered for trend comparison.

        This is the cross-visit retrieval CASE-01 exists to provide: it returns
        raw ordered history with symptoms attached and computes no trends --
        interpretation belongs to the AI layer.
        """
        order = (
            (Visit.visit_date.desc(), Visit.created_at.desc())
            if newest_first
            else (Visit.visit_date.asc(), Visit.created_at.asc())
        )

        statement = self._patient_statement(patient_id)
        if exclude_visit_id is not None:
            statement = statement.where(Visit.id != exclude_visit_id)

        statement = (
            self._with_symptoms(statement).order_by(*order).limit(limit)
        )
        return list(db.scalars(statement).unique().all())
