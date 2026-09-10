"""Normalize Input + Build Clinical Context (TRD section 8, stages 1-2).

This is the only module in ``app/ai/`` that touches ORM objects, and it reads
already-loaded attributes rather than querying -- that reading *is* the
normalize stage. Everything downstream of ``build_clinical_context`` operates on
schemas alone, which is what lets the whole pipeline be tested without a
database.

PHI minimization (AGENTS.md section 12): the context deliberately carries no
name, email, phone, address, or date of birth. Age is reduced to whole years.
"""

from collections.abc import Sequence
from datetime import date

from app.ai.trends import detect_trends
from app.models.patient import Patient
from app.models.visit import Visit
from app.schemas.clinical_context import (
    ClinicalContext,
    ContextSymptom,
    ContextVisit,
)


def _age_years(dob: date | None, *, today: date | None = None) -> int | None:
    """Whole years, so a date of birth never reaches the reasoning layer."""

    if dob is None:
        return None

    reference = today or date.today()
    years = reference.year - dob.year
    if (reference.month, reference.day) < (dob.month, dob.day):
        years -= 1
    return max(years, 0)


def _to_context_visit(visit: Visit) -> ContextVisit:
    """Map a Visit and its live symptoms into the AI-facing shape."""

    return ContextVisit(
        id=visit.id,
        visit_date=visit.visit_date,
        chief_complaint=visit.chief_complaint,
        history=visit.history,
        vitals=visit.vitals or {},
        notes=visit.notes,
        symptoms=[
            ContextSymptom(
                id=symptom.id,
                symptom_name=symptom.symptom_name,
                severity=symptom.severity,
                duration_days=symptom.duration_days,
                onset=symptom.onset,
            )
            for symptom in visit.symptoms
            if not symptom.is_deleted
        ],
    )


def build_clinical_context(
    current_visit: Visit,
    prior_visits: Sequence[Visit] = (),
    *,
    patient: Patient | None = None,
    today: date | None = None,
) -> ClinicalContext:
    """Assemble the context the AI pipeline reasons over.

    ``prior_visits`` must be oldest-first and must not include the current
    visit -- ``VisitService.get_patient_history(newest_first=False,
    exclude_visit_id=...)`` returns exactly that.

    Trend detection runs across prior visits *and* the current one, because a
    symptom's latest severity is part of its trajectory.
    """

    context_current = _to_context_visit(current_visit)
    context_prior = [_to_context_visit(visit) for visit in prior_visits]

    return ClinicalContext(
        patient_id=current_visit.patient_id,
        visit_id=current_visit.id,
        current_visit=context_current,
        prior_visits=context_prior,
        trends=detect_trends([*context_prior, context_current]),
        patient_age_years=_age_years(
            getattr(patient, "dob", None), today=today
        ),
        patient_sex=getattr(patient, "gender", None),
    )


__all__ = ["build_clinical_context"]
