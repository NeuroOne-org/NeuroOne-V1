"""Analysis persistence operations."""
from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from app.models.analysis import Analysis, AnalysisFinding
from app.models.visit import Visit, VisitStatus
from app.repositories.base_repository import BaseRepository
from app.utils.exceptions import ConflictError, DatabaseError


class AnalysisRepository(BaseRepository[Analysis]):
    """Provide analysis-specific queries in addition to common CRUD."""

    def __init__(self):
        super().__init__(model=Analysis)

    def _with_graph(self, statement):
        """Eager-load findings and their citations in two extra queries.

        Every read path goes through here, so no response can lazy-load a
        finding or a citation per row.
        """
        return statement.options(
            selectinload(
                Analysis.findings.and_(AnalysisFinding.is_deleted.is_(False))
            ).selectinload(AnalysisFinding.evidence)
        )

    def _visit_statement(self, visit_id: UUID):
        return select(Analysis).where(
            Analysis.visit_id == visit_id,
            Analysis.is_deleted.is_(False),
        )

    def create_with_status(
        self,
        db: Session,
        analysis: Analysis,
        visit: Visit,
        status: VisitStatus = VisitStatus.ANALYZED,
    ) -> Analysis:
        """Persist an analysis and advance the visit status in one transaction.

        Both halves commit together, so it is never possible to observe an
        ANALYZED visit with no analysis, nor an analysis on a visit that still
        reads as unanalyzed.

        This is the only place VisitStatus.ANALYZED is written -- the visits
        API rejects it (AGENTS.md section 8.1).
        """
        try:
            db.add(analysis)
            visit.status = status
            db.commit()
            db.refresh(analysis)
            return analysis
        except IntegrityError as exc:
            db.rollback()
            raise ConflictError("Analysis conflicts with existing data.") from exc
        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseError("Unable to persist analysis.") from exc

    def get_with_graph(self, db: Session, analysis_id: UUID) -> Analysis | None:
        """Return an active analysis with its findings and citations loaded."""
        statement = self._with_graph(
            select(Analysis).where(
                Analysis.id == analysis_id,
                Analysis.is_deleted.is_(False),
            )
        )
        return db.scalar(statement)

    def get_by_visit(
        self,
        db: Session,
        visit_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Analysis]:
        """Return a visit's analyses, newest first."""
        statement = (
            self._with_graph(self._visit_statement(visit_id))
            .order_by(Analysis.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(statement).unique().all())

    def count_by_visit(self, db: Session, visit_id: UUID) -> int:
        """Count a visit's active analyses."""
        statement = self._visit_statement(visit_id)
        count_statement = select(func.count()).select_from(statement.subquery())
        return db.scalar(count_statement) or 0

    def get_latest_by_visit(self, db: Session, visit_id: UUID) -> Analysis | None:
        """Return the most recent analysis for a visit, if any."""
        statement = (
            self._with_graph(self._visit_statement(visit_id))
            .order_by(Analysis.created_at.desc())
            .limit(1)
        )
        return db.scalars(statement).unique().first()

    def get_latest_by_patient_ids(
        self,
        db: Session,
        patient_ids: Sequence[UUID],
    ) -> dict[UUID, Analysis]:
        """Return each patient's most recent analysis, across all their visits.

        The triage queue (ADR-006) ranks by a patient's latest analysis, not
        their latest visit -- a visit with no analysis yet has nothing to
        rank the patient by.
        """
        if not patient_ids:
            return {}

        latest = (
            select(
                Visit.patient_id.label("patient_id"),
                func.max(Analysis.created_at).label("latest_created_at"),
            )
            .join(Visit, Visit.id == Analysis.visit_id)
            .where(
                Visit.patient_id.in_(patient_ids),
                Analysis.is_deleted.is_(False),
                Visit.is_deleted.is_(False),
            )
            .group_by(Visit.patient_id)
            .subquery()
        )

        statement = self._with_graph(
            select(Analysis, Visit.patient_id)
            .join(Visit, Visit.id == Analysis.visit_id)
            .join(
                latest,
                (Visit.patient_id == latest.c.patient_id)
                & (Analysis.created_at == latest.c.latest_created_at),
            )
        )

        return {
            patient_id: analysis
            for analysis, patient_id in db.execute(statement).unique().all()
        }
