"""Unit tests for TriageService (ADR-006 decision 7).

The ranking order is the load-bearing property here: early_watch, then
worsening trend, then awaiting sign-off, in exactly that order -- and a page
boundary must never split what is otherwise one sorted queue.
"""

from datetime import date, datetime, timezone
from unittest.mock import Mock
from uuid import uuid4

from app.models.analysis import Analysis, AnalysisFinding, FindingCategory
from app.models.patient import Patient
from app.models.user import User, UserRole
from app.services.triage_service import IMAGING_TREND_SYMPTOM_NAME, TriageService


NOW = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)


def _user(role: UserRole = UserRole.CLINICIAN) -> User:
    return User(
        id=uuid4(),
        username=f"user-{uuid4().hex[:8]}",
        email=f"{uuid4().hex[:8]}@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hash",
        role=role,
        is_active=True,
        is_verified=True,
        is_deleted=False,
    )


def _patient(**overrides) -> Patient:
    payload = {
        "id": uuid4(),
        "doctor_id": uuid4(),
        "first_name": "Ada",
        "last_name": "Lovelace",
        "gender": "F",
        "dob": date(1963, 6, 15),
        "email": f"{uuid4().hex[:8]}@example.com",
        "address": "12 Analytical Way",
        "blood_group": "O+",
        "allergies": [],
        "emergency_contact": "5559876543",
    }
    payload.update(overrides)
    return Patient(**payload)


def _finding(category=FindingCategory.DIFFERENTIAL_DIAGNOSIS, trend_basis=()) -> AnalysisFinding:
    finding = AnalysisFinding(
        rank=0,
        condition_name="Condition A",
        category=category,
        confidence=0.5,
        supporting_findings=["a finding"],
        contradicting_findings=[],
        explanation="an explanation",
        trend_basis=list(trend_basis),
    )
    finding.is_deleted = False
    return finding


def _analysis(visit_id=None, *, findings=None, snapshot=None, reviewed=True) -> Analysis:
    analysis = Analysis(
        id=uuid4(),
        visit_id=visit_id or uuid4(),
        requested_by_id=uuid4(),
        model_name="neuroone-mock-reasoner-v1",
        provider_mode="simulated",
        pipeline_note="pipeline complete, evidence retrieval simulated",
        disclaimer="Decision support only.",
        generated_at=NOW,
        context_snapshot=snapshot if snapshot is not None else {},
        reviewed_by_id=uuid4() if reviewed else None,
        reviewed_at=NOW if reviewed else None,
    )
    analysis.findings = list(findings) if findings is not None else [_finding()]
    return analysis


def _service():
    patient_service = Mock()
    analysis_repository = Mock()
    service = TriageService(patient_service, analysis_repository)
    return service, patient_service, analysis_repository


# --------------------------------------------------------------------------
# Ranking order (ADR-006 decision 7)
# --------------------------------------------------------------------------


def test_early_watch_outranks_worsening_trend_and_sign_off() -> None:
    service, patient_service, analysis_repository = _service()
    early_watch_patient = _patient(first_name="EarlyWatch")
    trend_patient = _patient(first_name="Trend")
    sign_off_patient = _patient(first_name="SignOff")
    patient_service.list_all_patients.return_value = [
        sign_off_patient,
        trend_patient,
        early_watch_patient,
    ]
    analysis_repository.get_latest_by_patient_ids.return_value = {
        early_watch_patient.id: _analysis(
            findings=[_finding(category=FindingCategory.EARLY_WATCH, trend_basis=[{}])]
        ),
        trend_patient.id: _analysis(
            snapshot={"trends": [{"direction": "worsening"}]}
        ),
        sign_off_patient.id: _analysis(reviewed=False),
    }

    entries, total = service.list_queue(Mock(), _user())

    assert total == 3
    assert [e.patient_first_name for e in entries] == [
        "EarlyWatch",
        "Trend",
        "SignOff",
    ]


def test_a_patient_with_no_analysis_sorts_last() -> None:
    service, patient_service, analysis_repository = _service()
    unanalyzed = _patient(first_name="Unanalyzed")
    flagged = _patient(first_name="Flagged")
    patient_service.list_all_patients.return_value = [unanalyzed, flagged]
    analysis_repository.get_latest_by_patient_ids.return_value = {
        flagged.id: _analysis(
            findings=[_finding(category=FindingCategory.EARLY_WATCH, trend_basis=[{}])]
        )
    }

    entries, _ = service.list_queue(Mock(), _user())

    assert [e.patient_first_name for e in entries] == ["Flagged", "Unanalyzed"]
    unanalyzed_entry = entries[1]
    assert unanalyzed_entry.has_open_early_watch is False
    assert unanalyzed_entry.has_worsening_trend is False
    assert unanalyzed_entry.awaiting_sign_off is False
    assert unanalyzed_entry.latest_analysis_id is None


def test_a_worsening_imaging_trend_is_recognized_via_trend_basis() -> None:
    """ADR-006: the scan-derived trend has no column of its own -- it is read
    back from the staged candidate's trend_basis (app.ai.trends)."""
    service, patient_service, analysis_repository = _service()
    patient = _patient()
    patient_service.list_all_patients.return_value = [patient]
    analysis_repository.get_latest_by_patient_ids.return_value = {
        patient.id: _analysis(
            findings=[
                _finding(
                    trend_basis=[{"symptom_name": IMAGING_TREND_SYMPTOM_NAME}]
                )
            ]
        )
    }

    entries, _ = service.list_queue(Mock(), _user())

    assert entries[0].has_worsening_trend is True


def test_pagination_slices_the_already_sorted_queue() -> None:
    service, patient_service, analysis_repository = _service()
    patients = [_patient(first_name=f"P{i}") for i in range(5)]
    patient_service.list_all_patients.return_value = patients
    analysis_repository.get_latest_by_patient_ids.return_value = {}

    page, total = service.list_queue(Mock(), _user(), skip=2, limit=2)

    assert total == 5
    assert len(page) == 2


def test_a_reviewed_analysis_is_not_awaiting_sign_off() -> None:
    service, patient_service, analysis_repository = _service()
    patient = _patient()
    patient_service.list_all_patients.return_value = [patient]
    analysis_repository.get_latest_by_patient_ids.return_value = {
        patient.id: _analysis(reviewed=True)
    }

    entries, _ = service.list_queue(Mock(), _user())

    assert entries[0].awaiting_sign_off is False
