"""Triage queue: a clinician's panel ranked by what needs attention (ADR-006).

No stat tiles -- the ranked queue is itself the answer to "what needs
attention", and an aggregate confidence average across patients would be
both clinically meaningless and a step back toward the framing FR-04 warns
against.
"""

from sqlalchemy.orm import Session

from app.models.analysis import Analysis, FindingCategory
from app.models.patient import Patient
from app.models.user import User
from app.repositories.analysis_repository import AnalysisRepository
from app.schemas.triage import TriageEntry
from app.services.patient_service import PatientService


# The symptom_name app.ai.trends.stage_trend_basis_ref writes onto a staged
# candidate's trend_basis when the imaging-derived stage worsened across
# visits. There is no separate persisted column for "imaging trend" (ADR-006
# feeds it into trend_basis, not a new field), so this is how the triage
# queue recognizes it after the fact.
IMAGING_TREND_SYMPTOM_NAME = "MRI-derived stage"


def _has_open_early_watch(analysis: Analysis | None) -> bool:
    if analysis is None:
        return False
    return any(
        finding.category == FindingCategory.EARLY_WATCH
        for finding in analysis.findings
    )


def _has_worsening_trend(analysis: Analysis | None) -> bool:
    """A worsening trend from either signal (ADR-006: detect_trends extended).

    A symptom trend is recorded in the persisted context_snapshot. The
    imaging trend is not stored on its own, but a worsening one leaves a
    trace in the staged finding's trend_basis.
    """
    if analysis is None:
        return False

    symptom_trends = analysis.context_snapshot.get("trends") or []
    if any(trend.get("direction") == "worsening" for trend in symptom_trends):
        return True

    return any(
        reference.get("symptom_name") == IMAGING_TREND_SYMPTOM_NAME
        for finding in analysis.findings
        for reference in finding.trend_basis
    )


def _awaiting_sign_off(analysis: Analysis | None) -> bool:
    return analysis is not None and analysis.reviewed_at is None


class TriageService:
    """Ranks a clinician's patient panel by what needs attention."""

    def __init__(
        self,
        patient_service: PatientService,
        analysis_repository: AnalysisRepository,
    ):
        self.patient_service = patient_service
        self.analysis_repository = analysis_repository

    def _to_entry(self, patient: Patient, analysis: Analysis | None) -> TriageEntry:
        return TriageEntry(
            patient_id=patient.id,
            patient_first_name=patient.first_name,
            patient_last_name=patient.last_name,
            has_open_early_watch=_has_open_early_watch(analysis),
            has_worsening_trend=_has_worsening_trend(analysis),
            awaiting_sign_off=_awaiting_sign_off(analysis),
            latest_visit_id=analysis.visit_id if analysis else None,
            latest_analysis_id=analysis.id if analysis else None,
            latest_analysis_generated_at=analysis.generated_at if analysis else None,
        )

    def _priority(self, entry: TriageEntry) -> tuple[bool, bool, bool]:
        # False sorts before True in Python, so each flag is negated: an
        # entry needing attention on that dimension sorts first, in exactly
        # the order ADR-006 decision 7 states -- early_watch, then
        # worsening trend, then awaiting sign-off.
        return (
            not entry.has_open_early_watch,
            not entry.has_worsening_trend,
            not entry.awaiting_sign_off,
        )

    def list_queue(
        self,
        db: Session,
        current_user: User,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[TriageEntry], int]:
        """Return the caller's panel, ranked, then paginated.

        Ranking runs over the whole panel before paging: a page boundary
        must never split what is otherwise one sorted queue.
        """

        patients = self.patient_service.list_all_patients(db, current_user)
        latest_by_patient = self.analysis_repository.get_latest_by_patient_ids(
            db, [patient.id for patient in patients]
        )

        entries = [
            self._to_entry(patient, latest_by_patient.get(patient.id))
            for patient in patients
        ]
        entries.sort(key=self._priority)

        return entries[skip : skip + limit], len(entries)


__all__ = ["IMAGING_TREND_SYMPTOM_NAME", "TriageService"]
