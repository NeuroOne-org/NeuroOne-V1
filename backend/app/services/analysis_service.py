"""Business logic for AI analysis of a clinical case.

The ordering in ``analyze_visit`` is the safety mechanism, not an accident.
Every read and every provider call happens before the first write, so an AI or
retrieval failure has nothing to roll back and cannot leave a clinical record
partly modified (AGENTS.md section 8.5, ADR-003).
"""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.ai.context import build_clinical_context
from app.ai.orchestrator import AnalysisOrchestrator
from app.models.analysis import (
    Analysis,
    AnalysisEvidence,
    AnalysisFinding,
    FindingCategory,
)
from app.models.user import User, UserRole
from app.repositories.analysis_repository import AnalysisRepository
from app.schemas.analysis import AnalysisResult, DiagnosisCandidate
from app.services.base_service import BaseService
from app.services.patient_service import PatientService
from app.services.visit_service import VisitService
from app.utils.exceptions import AuthorizationError, EntityNotFoundError


class AnalysisService(BaseService[AnalysisRepository]):
    """Coordinates the AI pipeline and persists its output.

    Authorization is delegated wholly to VisitService and PatientService, so
    the ADR-002 ownership rule stays in one place.
    """

    def __init__(
        self,
        repository: AnalysisRepository,
        visit_service: VisitService,
        patient_service: PatientService,
        orchestrator: AnalysisOrchestrator,
    ):
        super().__init__(repository)
        self.visit_service = visit_service
        self.patient_service = patient_service
        self.orchestrator = orchestrator

    # -- mapping ---------------------------------------------------------

    def _to_finding(
        self,
        candidate: DiagnosisCandidate,
        rank: int,
    ) -> AnalysisFinding:
        return AnalysisFinding(
            rank=rank,
            condition_name=candidate.name,
            category=FindingCategory(candidate.category),
            confidence=candidate.confidence,
            supporting_findings=list(candidate.supporting_findings),
            contradicting_findings=list(candidate.contradicting_findings),
            explanation=candidate.explanation,
            trend_basis=[
                reference.model_dump(mode="json")
                for reference in candidate.trend_basis
            ],
            evidence=[
                AnalysisEvidence(
                    rank=index,
                    source=evidence.source,
                    citation=evidence.citation,
                    relevant_passage=evidence.relevant_passage,
                    document_id=evidence.document_id,
                    chunk_id=evidence.chunk_id,
                    source_url=evidence.source_url,
                    source_tier=evidence.source_tier,
                    published_year=evidence.published_year,
                    relevance_score=evidence.relevance_score,
                )
                for index, evidence in enumerate(candidate.evidence)
            ],
        )

    def _to_analysis(
        self,
        result: AnalysisResult,
        current_user: User,
        context_snapshot: dict,
    ) -> Analysis:
        return Analysis(
            visit_id=result.visit_id,
            requested_by_id=current_user.id,
            model_name=result.model_name,
            provider_mode=result.provider_mode,
            pipeline_note=result.pipeline_note,
            disclaimer=result.disclaimer,
            generated_at=result.generated_at,
            context_snapshot=context_snapshot,
            findings=[
                self._to_finding(candidate, rank)
                for rank, candidate in enumerate(result.candidates)
            ],
        )

    # -- use cases -------------------------------------------------------

    def analyze_visit(
        self,
        db: Session,
        visit_id: UUID,
        current_user: User,
        *,
        history_limit: int = 10,
    ) -> Analysis:
        """Run the AI pipeline for a visit and persist the result.

        Ownership violations read as a missing visit (ADR-002), inherited from
        ``VisitService.get_visit``.
        """

        # 1-3. Reads only. These also authorize.
        visit = self.visit_service.get_visit(db, visit_id, current_user)
        patient = self.patient_service.get_patient(
            db, visit.patient_id, current_user
        )
        prior_visits, _ = self.visit_service.get_patient_history(
            db,
            visit.patient_id,
            current_user,
            limit=history_limit,
            newest_first=False,
            exclude_visit_id=visit_id,
        )

        # 4. Pure.
        context = build_clinical_context(visit, prior_visits, patient=patient)

        # 5. Every provider and contract failure raises AIError here, before
        #    anything has been written.
        result = self.orchestrator.run(context)

        # 6. One transaction: the analysis graph and the visit status together.
        analysis = self._to_analysis(
            result, current_user, context.model_dump(mode="json")
        )
        return self.repository.create_with_status(db, analysis, visit)

    def get_analysis(
        self,
        db: Session,
        analysis_id: UUID,
        current_user: User,
    ) -> Analysis:
        """Retrieve one analysis by ID.

        The caller named only the analysis, so a visit-level authorization
        failure is re-labelled -- otherwise the parent visit's UUID would leak
        to someone with no claim to the record. This is the ADR-002 masking
        pattern applied one level deeper.
        """

        analysis = self.repository.get_with_graph(db, analysis_id)
        if analysis is None:
            raise EntityNotFoundError("Analysis", analysis_id)

        try:
            self.visit_service.get_visit(db, analysis.visit_id, current_user)
        except EntityNotFoundError as exc:
            raise EntityNotFoundError("Analysis", analysis_id) from exc

        return analysis

    def list_visit_analyses(
        self,
        db: Session,
        visit_id: UUID,
        current_user: User,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Analysis], int]:
        """List a visit's analyses, newest first."""

        self.visit_service.get_visit(db, visit_id, current_user)
        items = self.repository.get_by_visit(db, visit_id, skip, limit)
        total = self.repository.count_by_visit(db, visit_id)
        return items, total

    def sign_off_analysis(
        self,
        db: Session,
        analysis_id: UUID,
        current_user: User,
    ) -> Analysis:
        """Record clinician sign-off, gating report generation (ADR-006).

        Idempotent rather than one-shot: re-signing updates who and when
        rather than raising, since there is no separate amendment flow yet
        through which a clinician would need to revoke a prior sign-off.

        Only a clinician may sign. The route already enforces this; it is
        repeated here because ownership alone is not enough -- administrators
        pass every ownership check, and their sign-off would unlock a report
        no clinician reviewed.
        """

        if current_user.role is not UserRole.CLINICIAN:
            raise AuthorizationError("Only a clinician can sign off an analysis.")

        analysis = self.get_analysis(db, analysis_id, current_user)
        analysis.reviewed_by_id = current_user.id
        analysis.reviewed_at = datetime.now(timezone.utc)
        return self.repository.update(db, analysis)

    def get_latest_for_visit(
        self,
        db: Session,
        visit_id: UUID,
        current_user: User,
    ) -> Analysis:
        """Return the most recent analysis for a visit."""

        self.visit_service.get_visit(db, visit_id, current_user)

        analysis = self.repository.get_latest_by_visit(db, visit_id)
        if analysis is None:
            raise EntityNotFoundError("Analysis")

        return analysis
