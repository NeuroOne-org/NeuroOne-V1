"""Tests for the ORM -> ClinicalContext normalize stage.

The PHI-minimization assertion is the load-bearing one: AGENTS.md section 12
requires controlled exposure of patient data, and the context is the payload
that would be handed to an external model in AI-02.
"""

from datetime import date, datetime, timedelta, timezone
from uuid import uuid4

from app.ai.context import build_clinical_context
from app.models.patient import Patient
from app.models.symptom import Symptom
from app.models.visit import Visit, VisitStatus


BASE_DATE = datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc)


def _symptom(name="tremor", severity=5, *, deleted=False):
    symptom = Symptom(
        id=uuid4(),
        visit_id=uuid4(),
        symptom_name=name,
        severity=severity,
        duration_days=30,
        onset="gradual",
    )
    symptom.is_deleted = deleted
    return symptom


def _visit(patient_id=None, *, days_offset=0, complaint="tremor", symptoms=()):
    visit = Visit(
        id=uuid4(),
        patient_id=patient_id or uuid4(),
        visit_date=BASE_DATE + timedelta(days=days_offset),
        chief_complaint=complaint,
        history="six months",
        vitals={"heart_rate": 72},
        notes="a note",
        status=VisitStatus.DRAFT,
    )
    visit.symptoms = list(symptoms)
    return visit


def _patient(**overrides):
    payload = {
        "id": uuid4(),
        "doctor_id": uuid4(),
        "first_name": "Ada",
        "last_name": "Lovelace",
        "gender": "F",
        "dob": date(1990, 6, 15),
        "email": "ada@example.com",
        "address": "12 Analytical Way",
        "blood_group": "O+",
        "allergies": [],
        "emergency_contact": "5559876543",
    }
    payload.update(overrides)
    return Patient(**payload)


def test_current_visit_is_mapped_field_for_field() -> None:
    patient_id = uuid4()
    visit = _visit(patient_id, symptoms=[_symptom("tremor", 6)])

    context = build_clinical_context(visit)

    assert context.patient_id == patient_id
    assert context.visit_id == visit.id
    assert context.current_visit.chief_complaint == "tremor"
    assert context.current_visit.history == "six months"
    assert context.current_visit.vitals == {"heart_rate": 72}
    assert context.current_visit.notes == "a note"
    assert context.current_visit.symptoms[0].symptom_name == "tremor"
    assert context.current_visit.symptoms[0].duration_days == 30
    assert context.current_visit.symptoms[0].onset == "gradual"


def test_prior_visits_stay_oldest_first_and_exclude_the_current_one() -> None:
    patient_id = uuid4()
    older = _visit(patient_id, days_offset=0, complaint="first")
    newer = _visit(patient_id, days_offset=30, complaint="second")
    current = _visit(patient_id, days_offset=60, complaint="current")

    context = build_clinical_context(current, [older, newer])

    assert [v.chief_complaint for v in context.prior_visits] == [
        "first",
        "second",
    ]
    assert context.current_visit.chief_complaint == "current"
    assert current.id not in {v.id for v in context.prior_visits}


def test_all_visits_puts_the_current_visit_last() -> None:
    patient_id = uuid4()
    prior = _visit(patient_id, days_offset=0, complaint="prior")
    current = _visit(patient_id, days_offset=30, complaint="current")

    context = build_clinical_context(current, [prior])

    assert [v.chief_complaint for v in context.all_visits] == [
        "prior",
        "current",
    ]


def test_trends_span_prior_visits_and_the_current_one() -> None:
    """The current severity is part of the trajectory, not outside it."""
    patient_id = uuid4()
    visits = [
        _visit(patient_id, days_offset=0, symptoms=[_symptom("tremor", 3)]),
        _visit(patient_id, days_offset=30, symptoms=[_symptom("tremor", 5)]),
    ]
    current = _visit(
        patient_id, days_offset=60, symptoms=[_symptom("tremor", 8)]
    )

    context = build_clinical_context(current, visits)

    assert len(context.trends) == 1
    trend = context.trends[0]
    assert trend.direction == "worsening"
    assert trend.visit_span == 3
    assert (trend.first_severity, trend.latest_severity) == (3, 8)


def test_soft_deleted_symptoms_are_excluded() -> None:
    visit = _visit(
        symptoms=[_symptom("tremor", 6), _symptom("aphasia", 4, deleted=True)]
    )

    context = build_clinical_context(visit)

    names = [s.symptom_name for s in context.current_visit.symptoms]
    assert names == ["tremor"]


def test_age_is_derived_in_whole_years() -> None:
    visit = _visit()
    patient = _patient(dob=date(1990, 6, 15))

    context = build_clinical_context(
        visit, patient=patient, today=date(2026, 6, 14)
    )
    assert context.patient_age_years == 35

    context = build_clinical_context(
        visit, patient=patient, today=date(2026, 6, 15)
    )
    assert context.patient_age_years == 36


def test_sex_is_the_single_stored_character() -> None:
    context = build_clinical_context(_visit(), patient=_patient(gender="F"))

    assert context.patient_sex == "F"


def test_context_is_usable_without_a_patient() -> None:
    context = build_clinical_context(_visit())

    assert context.patient_age_years is None
    assert context.patient_sex is None


def test_serialized_context_carries_no_direct_identifiers() -> None:
    """AGENTS.md 12: the payload an external model would receive.

    Name, email, address, phone and date of birth must not appear.
    """
    patient = _patient(
        first_name="Ada",
        last_name="Lovelace",
        email="ada@example.com",
        address="12 Analytical Way",
        dob=date(1990, 6, 15),
    )
    visit = _visit(symptoms=[_symptom()])

    payload = build_clinical_context(visit, patient=patient).model_dump_json()

    for identifier in (
        "Ada",
        "Lovelace",
        "ada@example.com",
        "Analytical Way",
        "1990-06-15",
        "5559876543",
    ):
        assert identifier not in payload, identifier


def test_missing_vitals_normalize_to_an_empty_mapping() -> None:
    visit = _visit()
    visit.vitals = None

    assert build_clinical_context(visit).current_visit.vitals == {}
