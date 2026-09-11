"""Unit tests for ReportService.

Two properties carry the weight, mirroring test_analysis_service.py: that a
rendering failure never reaches the database (ADR-004's render-before-persist
ordering), and that a foreign report 404s without disclosing the analysis
behind it (ADR-002, applied two levels deeper).
"""

from datetime import date, datetime, timezone
from unittest.mock import Mock, patch
from uuid import uuid4

import pytest

from app.models.analysis import (
    Analysis,
    AnalysisEvidence,
    AnalysisFinding,
    FindingCategory,
)
from app.models.patient import Patient
from app.models.report import Report
from app.models.symptom import Symptom
from app.models.user import User, UserRole
from app.models.visit import Visit, VisitStatus
from app.schemas.analysis import DISCLAIMER, SIMULATED_PIPELINE_NOTE
from app.services.report_service import ReportService
from app.utils.exceptions import (
    AnalysisNotReviewedError,
    EntityNotFoundError,
    InternalServerError,
)


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


def _symptom(**overrides) -> Symptom:
    payload = {
        "id": uuid4(),
        "visit_id": uuid4(),
        "symptom_name": "resting tremor",
        "severity": 8,
        "duration_days": 180,
        "onset": "gradual",
        "observation": "worse at night",
    }
    payload.update(overrides)
    symptom = Symptom(**payload)
    symptom.is_deleted = False
    return symptom


def _visit(patient_id=None, *, symptoms=None) -> Visit:
    visit = Visit(
        id=uuid4(),
        patient_id=patient_id or uuid4(),
        visit_date=NOW,
        chief_complaint="intermittent hand tremor",
        history="six months",
        vitals={},
        notes=None,
        status=VisitStatus.ANALYZED,
    )
    visit.symptoms = symptoms if symptoms is not None else [_symptom()]
    return visit


def _evidence(**overrides) -> AnalysisEvidence:
    payload = {
        "rank": 0,
        "source": "Journal of Neurology",
        "citation": "Doe J et al. Early motor signs. J Neurol. 2024;271(3):112-120.",
        "relevant_passage": "Progressive resting tremor is an early motor sign.",
        "document_id": "doc-1",
        "chunk_id": "doc-1#c1",
        "source_tier": "guideline",
        "published_year": 2024,
        "relevance_score": 1.0,
    }
    payload.update(overrides)
    return AnalysisEvidence(**payload)


def _finding(**overrides) -> AnalysisFinding:
    payload = {
        "rank": 0,
        "condition_name": "Parkinsonian syndrome",
        "category": FindingCategory.DIFFERENTIAL_DIAGNOSIS,
        "confidence": 0.55,
        "supporting_findings": ["resting tremor severity 8"],
        "contradicting_findings": [],
        "explanation": "Motor findings are consistent with early parkinsonism.",
        "trend_basis": [],
    }
    payload.update(overrides)
    finding = AnalysisFinding(**payload)
    finding.evidence = [_evidence()]
    return finding


def _analysis(
    visit_id=None,
    *,
    findings=None,
    reviewed_by_id=...,
    reviewed_at=...,
) -> Analysis:
    # Reviewed by default: most tests here exercise report generation, not
    # the sign-off gate (ADR-006 decision 6), which has its own tests below.
    analysis = Analysis(
        id=uuid4(),
        visit_id=visit_id or uuid4(),
        requested_by_id=uuid4(),
        model_name="neuroone-mock-reasoner-v1",
        provider_mode="simulated",
        pipeline_note=SIMULATED_PIPELINE_NOTE,
        disclaimer=DISCLAIMER,
        generated_at=NOW,
        context_snapshot={},
        reviewed_by_id=uuid4() if reviewed_by_id is ... else reviewed_by_id,
        reviewed_at=NOW if reviewed_at is ... else reviewed_at,
    )
    analysis.findings = findings if findings is not None else [_finding()]
    return analysis


def _service():
    repository = Mock()
    analysis_service = Mock()
    visit_service = Mock()
    patient_service = Mock()
    service = ReportService(
        repository, analysis_service, visit_service, patient_service
    )
    return service, repository, analysis_service, visit_service, patient_service


def _wire_happy_path(analysis_service, visit_service, patient_service):
    patient = _patient()
    visit = _visit(patient.id)
    analysis = _analysis(visit.id)
    analysis_service.get_analysis.return_value = analysis
    visit_service.get_visit.return_value = visit
    patient_service.get_patient.return_value = patient
    return analysis, visit, patient


# --------------------------------------------------------------------------
# Generation -- render before persist (ADR-004)
# --------------------------------------------------------------------------


def test_generating_a_report_persists_a_snapshot() -> None:
    service, repository, analysis_service, visit_service, patient_service = (
        _service()
    )
    analysis, visit, patient = _wire_happy_path(
        analysis_service, visit_service, patient_service
    )
    repository.create.side_effect = lambda db, obj: obj

    report = service.generate_report(Mock(), analysis.id, _user())

    repository.create.assert_called_once()
    assert report.analysis_id == analysis.id
    assert report.filename == f"neuroone-report-{report.id}.pdf"
    assert report.snapshot["patient"]["full_name"] == "Ada Lovelace"
    assert report.snapshot["findings"][0]["condition_name"] == "Parkinsonian syndrome"


def test_an_unreviewed_analysis_refuses_report_generation() -> None:
    """ADR-006 decision 6: sign-off gates the report."""
    service, repository, analysis_service, visit_service, patient_service = (
        _service()
    )
    unreviewed = _analysis(reviewed_by_id=None, reviewed_at=None)
    analysis_service.get_analysis.return_value = unreviewed

    with pytest.raises(AnalysisNotReviewedError):
        service.generate_report(Mock(), unreviewed.id, _user())

    repository.create.assert_not_called()
    visit_service.get_visit.assert_not_called()


def test_a_reviewed_analysis_may_generate_a_report() -> None:
    service, repository, analysis_service, visit_service, patient_service = (
        _service()
    )
    analysis, visit, patient = _wire_happy_path(
        analysis_service, visit_service, patient_service
    )
    repository.create.side_effect = lambda db, obj: obj

    report = service.generate_report(Mock(), analysis.id, _user())

    assert report.analysis_id == analysis.id


def test_a_rendering_failure_never_reaches_the_database() -> None:
    service, repository, analysis_service, visit_service, patient_service = (
        _service()
    )
    _wire_happy_path(analysis_service, visit_service, patient_service)

    with patch(
        "app.services.report_service.render",
        side_effect=RuntimeError("layout error"),
    ):
        with pytest.raises(InternalServerError) as exc_info:
            service.generate_report(Mock(), uuid4(), _user())

    assert exc_info.value.error_code == "report_render_error"
    repository.create.assert_not_called()


def test_generation_on_an_unauthorized_analysis_is_refused_before_any_work() -> None:
    service, repository, analysis_service, visit_service, patient_service = (
        _service()
    )
    analysis_service.get_analysis.side_effect = EntityNotFoundError(
        "Analysis", uuid4()
    )

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.generate_report(Mock(), uuid4(), _user())

    assert exc_info.value.entity == "Analysis"
    visit_service.get_visit.assert_not_called()
    repository.create.assert_not_called()


def test_no_early_watch_finding_loses_its_trend_basis_in_the_snapshot() -> None:
    service, repository, analysis_service, visit_service, patient_service = (
        _service()
    )
    trend_basis = [
        {
            "visit_id": str(uuid4()),
            "symptom_name": "memory loss",
            "observation": "memory loss severity 2 -> 4 across 3 visits",
        }
    ]
    finding = _finding(
        category=FindingCategory.EARLY_WATCH,
        confidence=0.3,
        trend_basis=trend_basis,
    )
    patient = _patient()
    visit = _visit(patient.id)
    analysis = _analysis(visit.id, findings=[finding])
    analysis_service.get_analysis.return_value = analysis
    visit_service.get_visit.return_value = visit
    patient_service.get_patient.return_value = patient
    repository.create.side_effect = lambda db, obj: obj

    report = service.generate_report(Mock(), analysis.id, _user())

    assert report.snapshot["findings"][0]["trend_basis"] == trend_basis


# --------------------------------------------------------------------------
# Retrieval -- masked 404s (ADR-002, one level deeper than Analysis)
# --------------------------------------------------------------------------


def test_a_missing_report_404s() -> None:
    service, repository, *_ = _service()
    repository.get_by_id.return_value = None

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.get_report(Mock(), uuid4(), _user())

    assert exc_info.value.entity == "Report"


def test_a_foreign_report_reads_as_a_missing_report() -> None:
    """The masked 404 must not disclose the analysis behind it."""
    service, repository, analysis_service, _, _ = _service()
    report = Report(
        id=uuid4(),
        analysis_id=uuid4(),
        generated_by_id=uuid4(),
        generated_at=NOW,
        filename="neuroone-report-x.pdf",
        snapshot={},
    )
    repository.get_by_id.return_value = report
    analysis_service.get_analysis.side_effect = EntityNotFoundError(
        "Analysis", report.analysis_id
    )

    report_id = uuid4()
    with pytest.raises(EntityNotFoundError) as exc_info:
        service.get_report(Mock(), report_id, _user())

    assert exc_info.value.entity == "Report"
    assert exc_info.value.identifier == report_id
    assert str(report.analysis_id) not in exc_info.value.message


def test_an_owned_report_is_returned() -> None:
    service, repository, analysis_service, _, _ = _service()
    report = Report(
        id=uuid4(),
        analysis_id=uuid4(),
        generated_by_id=uuid4(),
        generated_at=NOW,
        filename="neuroone-report-x.pdf",
        snapshot={},
    )
    repository.get_by_id.return_value = report
    analysis_service.get_analysis.return_value = Mock()

    assert service.get_report(Mock(), report.id, _user()) is report


def test_listing_a_foreign_analysiss_reports_is_refused() -> None:
    service, repository, analysis_service, _, _ = _service()
    analysis_service.get_analysis.side_effect = EntityNotFoundError(
        "Analysis", uuid4()
    )

    with pytest.raises(EntityNotFoundError):
        service.list_analysis_reports(Mock(), uuid4(), _user())

    repository.get_by_analysis.assert_not_called()


def test_listing_returns_items_and_total() -> None:
    service, repository, analysis_service, _, _ = _service()
    analysis_service.get_analysis.return_value = Mock()
    repository.get_by_analysis.return_value = [Mock()]
    repository.count_by_analysis.return_value = 2

    items, total = service.list_analysis_reports(Mock(), uuid4(), _user())

    assert len(items) == 1
    assert total == 2


# --------------------------------------------------------------------------
# Download -- re-render from the immutable snapshot
# --------------------------------------------------------------------------


def test_downloading_re_renders_from_the_stored_snapshot() -> None:
    service, repository, analysis_service, _, _ = _service()
    snapshot = {
        "analysis_id": str(uuid4()),
        "visit_id": str(uuid4()),
        "patient": {"full_name": "Ada Lovelace"},
        "visit": {
            "visit_date": NOW.isoformat(),
            "chief_complaint": "tremor",
            "symptoms": [],
        },
        "model_name": "m",
        "provider_mode": "simulated",
        "pipeline_note": "pipeline complete, evidence retrieval simulated",
        "disclaimer": DISCLAIMER,
        "generated_at": NOW.isoformat(),
        "findings": [
            {
                "rank": 0,
                "condition_name": "X",
                "category": "differential_diagnosis",
                "likelihood_band": "moderate",
                "supporting_findings": ["a"],
                "contradicting_findings": [],
                "explanation": "e",
                "trend_basis": [],
                "evidence": [
                    {"source": "s", "citation": "c", "relevant_passage": "p"}
                ],
            }
        ],
    }
    report = Report(
        id=uuid4(),
        analysis_id=uuid4(),
        generated_by_id=uuid4(),
        generated_at=NOW,
        filename="neuroone-report-x.pdf",
        snapshot=snapshot,
    )
    repository.get_by_id.return_value = report
    analysis_service.get_analysis.return_value = Mock()

    pdf_bytes, filename = service.get_pdf(Mock(), report.id, _user())

    assert pdf_bytes.startswith(b"%PDF-")
    assert filename == "neuroone-report-x.pdf"


def test_a_download_rendering_failure_mutates_nothing() -> None:
    service, repository, analysis_service, _, _ = _service()
    snapshot = {
        "analysis_id": str(uuid4()),
        "visit_id": str(uuid4()),
        "patient": {"full_name": "Ada Lovelace"},
        "visit": {
            "visit_date": NOW.isoformat(),
            "chief_complaint": "tremor",
            "symptoms": [],
        },
        "model_name": "m",
        "provider_mode": "simulated",
        "pipeline_note": "pipeline complete, evidence retrieval simulated",
        "disclaimer": DISCLAIMER,
        "generated_at": NOW.isoformat(),
        "findings": [
            {
                "rank": 0,
                "condition_name": "X",
                "category": "differential_diagnosis",
                "likelihood_band": "moderate",
                "supporting_findings": ["a"],
                "contradicting_findings": [],
                "explanation": "e",
                "trend_basis": [],
                "evidence": [
                    {"source": "s", "citation": "c", "relevant_passage": "p"}
                ],
            }
        ],
    }
    report = Report(
        id=uuid4(),
        analysis_id=uuid4(),
        generated_by_id=uuid4(),
        generated_at=NOW,
        filename="neuroone-report-x.pdf",
        snapshot=snapshot,
    )
    repository.get_by_id.return_value = report
    analysis_service.get_analysis.return_value = Mock()

    with patch(
        "app.services.report_service.render",
        side_effect=RuntimeError("layout error"),
    ):
        with pytest.raises(InternalServerError) as exc_info:
            service.get_pdf(Mock(), report.id, _user())

    assert exc_info.value.error_code == "report_render_error"
