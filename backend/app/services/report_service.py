"""Business logic for generating and retrieving clinical report PDFs.

ADR-004: authorization has no column of its own on ``reports``. Every read
here re-derives ownership through ``AnalysisService`` -- exactly the chain
``ADR-002``/``ADR-003`` already established one level up -- rather than
re-implementing it.
"""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.models.patient import Patient
from app.models.report import Report
from app.models.user import User
from app.models.visit import Visit
from app.reports.renderer import render
from app.repositories.report_repository import ReportRepository
from app.schemas.analysis import likelihood_band_for
from app.schemas.clinical_context import ClinicalContext
from app.schemas.report import (
    ReportEvidenceSnapshot,
    ReportFindingSnapshot,
    ReportPatientSnapshot,
    ReportSnapshot,
    ReportSymptomSnapshot,
    ReportVisitSnapshot,
)
from app.services.analysis_service import AnalysisService
from app.services.base_service import BaseService
from app.services.patient_service import PatientService
from app.services.visit_service import VisitService
from app.utils.exceptions import (
    AnalysisNotReviewedError,
    EntityNotFoundError,
    InternalServerError,
)


def _render_or_fail(snapshot: ReportSnapshot) -> bytes:
    try:
        return render(snapshot)
    except Exception as exc:  # renderer failure, not a contract failure
        raise InternalServerError(
            "Report rendering failed. The clinical record was not modified.",
            error_code="report_render_error",
        ) from exc


class ReportService(BaseService[ReportRepository]):
    """Builds report snapshots, renders them, and persists the metadata."""

    def __init__(
        self,
        repository: ReportRepository,
        analysis_service: AnalysisService,
        visit_service: VisitService,
        patient_service: PatientService,
    ):
        super().__init__(repository)
        self.analysis_service = analysis_service
        self.visit_service = visit_service
        self.patient_service = patient_service

    # -- mapping ---------------------------------------------------------

    def _build_snapshot(
        self, analysis: Analysis, visit: Visit, patient: Patient
    ) -> ReportSnapshot:
        """The clinical case comes from the analysis's own context snapshot
        (HB-12), so edits made after the analysis never reach its report.
        Only the name is read live: it identifies the patient, and the AI
        context deliberately never carries it.
        """

        full_name = patient.first_name
        if patient.last_name:
            full_name = f"{patient.first_name} {patient.last_name}"

        context = ClinicalContext.model_validate(analysis.context_snapshot)
        case = context.current_visit

        return ReportSnapshot(
            analysis_id=analysis.id,
            visit_id=visit.id,
            patient=ReportPatientSnapshot(
                full_name=full_name,
                age_years=context.patient_age_years,
                gender=context.patient_sex,
            ),
            visit=ReportVisitSnapshot(
                visit_date=case.visit_date,
                chief_complaint=case.chief_complaint,
                history=case.history,
                notes=case.notes,
                symptoms=[
                    ReportSymptomSnapshot(
                        symptom_name=symptom.symptom_name,
                        severity=symptom.severity,
                        duration_days=symptom.duration_days,
                        onset=symptom.onset,
                        observation=symptom.observation,
                    )
                    for symptom in case.symptoms
                ],
            ),
            model_name=analysis.model_name,
            provider_mode=analysis.provider_mode,
            pipeline_note=analysis.pipeline_note,
            disclaimer=analysis.disclaimer,
            generated_at=analysis.generated_at,
            reviewed_by_name=(
                f"{analysis.reviewed_by.first_name} {analysis.reviewed_by.last_name}"
            ),
            reviewed_at=analysis.reviewed_at,
            findings=[
                ReportFindingSnapshot(
                    rank=finding.rank,
                    condition_name=finding.condition_name,
                    category=finding.category.value,
                    likelihood_band=likelihood_band_for(finding.confidence),
                    supporting_findings=list(finding.supporting_findings),
                    contradicting_findings=list(finding.contradicting_findings),
                    explanation=finding.explanation,
                    trend_basis=list(finding.trend_basis),
                    evidence=[
                        ReportEvidenceSnapshot(
                            source=evidence.source,
                            citation=evidence.citation,
                            relevant_passage=evidence.relevant_passage,
                            source_url=evidence.source_url,
                            source_tier=evidence.source_tier,
                            published_year=evidence.published_year,
                        )
                        for evidence in finding.evidence
                    ],
                )
                for finding in analysis.findings
            ],
        )

    # -- use cases -------------------------------------------------------

    def generate_report(
        self,
        db: Session,
        analysis_id: UUID,
        current_user: User,
    ) -> Report:
        """Build, render, and persist a new report for an analysis.

        Render-before-persist (ADR-004): rendering is proved to succeed
        before any row is constructed, so a rendering failure leaves nothing
        to roll back.

        Sign-off gates this (ADR-006 decision 6): no PDF is produced until a
        clinician has reviewed the analysis, which is what makes "a
        clinician reviewed it" structural rather than a disclaimer.
        """

        analysis = self.analysis_service.get_analysis(db, analysis_id, current_user)
        if analysis.reviewed_at is None:
            raise AnalysisNotReviewedError(
                "This analysis has not been signed off by a clinician yet. "
                "A report can only be generated after sign-off."
            )

        visit = self.visit_service.get_visit(db, analysis.visit_id, current_user)
        patient = self.patient_service.get_patient(
            db, visit.patient_id, current_user
        )

        snapshot = self._build_snapshot(analysis, visit, patient)
        _render_or_fail(snapshot)

        report_id = uuid4()
        report = Report(
            id=report_id,
            analysis_id=analysis.id,
            generated_by_id=current_user.id,
            generated_at=datetime.now(timezone.utc),
            filename=f"neuroone-report-{report_id}.pdf",
            snapshot=snapshot.model_dump(mode="json"),
        )
        return self.repository.create(db, report)

    def get_report(
        self,
        db: Session,
        report_id: UUID,
        current_user: User,
    ) -> Report:
        """Retrieve one report by ID.

        The caller named only the report, so an authorization failure is
        re-labelled -- otherwise the parent analysis's UUID would leak to
        someone with no claim to the record (the ADR-002 masking pattern,
        applied one level deeper still).
        """

        report = self.repository.get_by_id(db, report_id)
        if report is None:
            raise EntityNotFoundError("Report", report_id)

        try:
            self.analysis_service.get_analysis(db, report.analysis_id, current_user)
        except EntityNotFoundError as exc:
            raise EntityNotFoundError("Report", report_id) from exc

        return report

    def list_analysis_reports(
        self,
        db: Session,
        analysis_id: UUID,
        current_user: User,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Report], int]:
        """List an analysis's reports, newest first."""

        self.analysis_service.get_analysis(db, analysis_id, current_user)
        items = self.repository.get_by_analysis(db, analysis_id, skip, limit)
        total = self.repository.count_by_analysis(db, analysis_id)
        return items, total

    def get_pdf(
        self,
        db: Session,
        report_id: UUID,
        current_user: User,
    ) -> tuple[bytes, str]:
        """Re-render a report's PDF bytes from its immutable snapshot."""

        report = self.get_report(db, report_id, current_user)
        snapshot = ReportSnapshot.model_validate(report.snapshot)
        return _render_or_fail(snapshot), report.filename


__all__ = ["ReportService"]
