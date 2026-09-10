"""Unit tests for AnalysisService.

Two properties carry the weight here: that a failure in the pipeline never
reaches the database (AGENTS.md section 8.5), and that a foreign analysis 404s
without disclosing the visit or patient behind it (ADR-002).
"""

from datetime import datetime, timezone
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.models.analysis import FindingCategory
from app.models.user import User, UserRole
from app.models.visit import Visit, VisitStatus
from app.schemas.analysis import (
    DISCLAIMER,
    SIMULATED_PIPELINE_NOTE,
    AnalysisResult,
    DiagnosisCandidate,
    TrendBasisRef,
)
from app.schemas.evidence import EvidenceRef
from app.services.analysis_service import AnalysisService
from app.utils.exceptions import AIError, EntityNotFoundError


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


def _visit(patient_id=None) -> Visit:
    visit = Visit(
        id=uuid4(),
        patient_id=patient_id or uuid4(),
        visit_date=NOW,
        chief_complaint="tremor",
        vitals={},
        status=VisitStatus.SUBMITTED,
    )
    visit.symptoms = []
    return visit


def _evidence() -> EvidenceRef:
    return EvidenceRef(
        source="Simulated Source",
        citation="Illustrative reference (simulated corpus), 2024.",
        relevant_passage="A passage.",
    )


def _candidate(**overrides) -> DiagnosisCandidate:
    payload = {
        "name": "Condition A",
        "category": "differential_diagnosis",
        "confidence": 0.5,
        "supporting_findings": ["a finding"],
        "contradicting_findings": [],
        "explanation": "an explanation",
        "trend_basis": [],
        "evidence": [_evidence()],
    }
    payload.update(overrides)
    return DiagnosisCandidate(**payload)


def _result(visit, candidates=None) -> AnalysisResult:
    return AnalysisResult(
        visit_id=visit.id,
        patient_id=visit.patient_id,
        model_name="neuroone-mock-reasoner-v1",
        provider_mode="simulated",
        pipeline_note=SIMULATED_PIPELINE_NOTE,
        disclaimer=DISCLAIMER,
        generated_at=NOW,
        candidates=candidates or [_candidate()],
    )


def _service():
    repository = Mock()
    visit_service = Mock()
    patient_service = Mock()
    orchestrator = Mock()
    service = AnalysisService(
        repository, visit_service, patient_service, orchestrator
    )
    return service, repository, visit_service, patient_service, orchestrator


def _wire_happy_path(visit_service, patient_service, orchestrator, visit):
    visit_service.get_visit.return_value = visit
    visit_service.get_patient_history.return_value = ([], 0)
    patient_service.get_patient.return_value = None
    orchestrator.run.return_value = _result(visit)


def _deny_visit(visit_service):
    visit_service.get_visit.side_effect = EntityNotFoundError("Visit", uuid4())


# --------------------------------------------------------------------------
# Ordering -- AGENTS.md 8.5
# --------------------------------------------------------------------------


def test_a_pipeline_failure_never_reaches_the_database() -> None:
    service, repository, visit_service, patient_service, orchestrator = _service()
    visit = _visit()
    _wire_happy_path(visit_service, patient_service, orchestrator, visit)
    orchestrator.run.side_effect = AIError("model down", error_code="ai_error")

    with pytest.raises(AIError):
        service.analyze_visit(Mock(), visit.id, _user())

    repository.create_with_status.assert_not_called()
    assert visit.status == VisitStatus.SUBMITTED


def test_a_retrieval_failure_leaves_the_visit_status_unchanged() -> None:
    service, repository, visit_service, patient_service, orchestrator = _service()
    visit = _visit()
    _wire_happy_path(visit_service, patient_service, orchestrator, visit)
    orchestrator.run.side_effect = AIError("corpus down", error_code="rag_error")

    with pytest.raises(AIError) as exc_info:
        service.analyze_visit(Mock(), visit.id, _user())

    assert exc_info.value.error_code == "rag_error"
    repository.create_with_status.assert_not_called()
    assert visit.status == VisitStatus.SUBMITTED


def test_success_persists_the_analysis_and_advances_the_visit() -> None:
    service, repository, visit_service, patient_service, orchestrator = _service()
    visit = _visit()
    _wire_happy_path(visit_service, patient_service, orchestrator, visit)
    repository.create_with_status.side_effect = lambda db, analysis, v: analysis

    analysis = service.analyze_visit(Mock(), visit.id, _user())

    repository.create_with_status.assert_called_once()
    assert analysis.visit_id == visit.id
    assert analysis.model_name == "neuroone-mock-reasoner-v1"
    assert analysis.provider_mode == "simulated"
    assert analysis.pipeline_note == SIMULATED_PIPELINE_NOTE


# --------------------------------------------------------------------------
# Context assembly
# --------------------------------------------------------------------------


def test_history_is_requested_oldest_first_excluding_the_current_visit() -> None:
    service, repository, visit_service, patient_service, orchestrator = _service()
    visit = _visit()
    _wire_happy_path(visit_service, patient_service, orchestrator, visit)
    repository.create_with_status.side_effect = lambda db, analysis, v: analysis

    service.analyze_visit(Mock(), visit.id, _user(), history_limit=7)

    kwargs = visit_service.get_patient_history.call_args.kwargs
    assert kwargs["limit"] == 7
    assert kwargs["newest_first"] is False
    assert kwargs["exclude_visit_id"] == visit.id


def test_the_context_snapshot_is_persisted_with_the_analysis() -> None:
    service, repository, visit_service, patient_service, orchestrator = _service()
    visit = _visit()
    _wire_happy_path(visit_service, patient_service, orchestrator, visit)
    repository.create_with_status.side_effect = lambda db, analysis, v: analysis

    analysis = service.analyze_visit(Mock(), visit.id, _user())

    assert analysis.context_snapshot["visit_id"] == str(visit.id)
    assert analysis.context_snapshot["patient_id"] == str(visit.patient_id)


def test_the_requesting_clinician_is_recorded() -> None:
    service, repository, visit_service, patient_service, orchestrator = _service()
    visit = _visit()
    clinician = _user()
    _wire_happy_path(visit_service, patient_service, orchestrator, visit)
    repository.create_with_status.side_effect = lambda db, analysis, v: analysis

    analysis = service.analyze_visit(Mock(), visit.id, clinician)

    assert analysis.requested_by_id == clinician.id


# --------------------------------------------------------------------------
# Candidate -> finding mapping
# --------------------------------------------------------------------------


def test_candidates_are_persisted_in_rank_order_with_their_citations() -> None:
    service, repository, visit_service, patient_service, orchestrator = _service()
    visit = _visit()
    _wire_happy_path(visit_service, patient_service, orchestrator, visit)
    orchestrator.run.return_value = _result(
        visit,
        [
            _candidate(name="First", confidence=0.8),
            _candidate(name="Second", confidence=0.4),
        ],
    )
    repository.create_with_status.side_effect = lambda db, analysis, v: analysis

    analysis = service.analyze_visit(Mock(), visit.id, _user())

    assert [f.rank for f in analysis.findings] == [0, 1]
    assert [f.condition_name for f in analysis.findings] == ["First", "Second"]
    assert all(f.evidence for f in analysis.findings)


def test_an_early_watch_candidate_persists_its_trend_basis_as_json() -> None:
    service, repository, visit_service, patient_service, orchestrator = _service()
    visit = _visit()
    reference = TrendBasisRef(
        visit_id=uuid4(),
        symptom_id=uuid4(),
        symptom_name="memory loss",
        visit_date=NOW,
        severity=4,
        observation="memory loss severity 2 -> 4 across 3 visits",
    )
    _wire_happy_path(visit_service, patient_service, orchestrator, visit)
    orchestrator.run.return_value = _result(
        visit,
        [
            _candidate(
                category="early_watch", confidence=0.3, trend_basis=[reference]
            )
        ],
    )
    repository.create_with_status.side_effect = lambda db, analysis, v: analysis

    finding = service.analyze_visit(Mock(), visit.id, _user()).findings[0]

    assert finding.category is FindingCategory.EARLY_WATCH
    assert finding.trend_basis[0]["symptom_name"] == "memory loss"
    # JSON mode, so the UUIDs are serializable strings rather than UUID objects.
    assert finding.trend_basis[0]["visit_id"] == str(reference.visit_id)


# --------------------------------------------------------------------------
# Authorization -- ADR-002, one level deeper
# --------------------------------------------------------------------------


def test_analysis_on_another_clinicians_visit_is_refused_before_any_work() -> None:
    service, repository, visit_service, _, orchestrator = _service()
    _deny_visit(visit_service)

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.analyze_visit(Mock(), uuid4(), _user())

    assert exc_info.value.entity == "Visit"
    orchestrator.run.assert_not_called()
    repository.create_with_status.assert_not_called()


def test_a_foreign_analysis_reads_as_a_missing_analysis() -> None:
    """The masked 404 must not disclose the visit or the patient behind it."""
    service, repository, visit_service, _, _ = _service()
    visit = _visit()
    analysis = Mock()
    analysis.visit_id = visit.id
    repository.get_with_graph.return_value = analysis
    _deny_visit(visit_service)

    analysis_id = uuid4()
    with pytest.raises(EntityNotFoundError) as exc_info:
        service.get_analysis(Mock(), analysis_id, _user())

    assert exc_info.value.entity == "Analysis"
    assert exc_info.value.identifier == analysis_id
    assert str(visit.id) not in exc_info.value.message
    assert str(visit.patient_id) not in exc_info.value.message


def test_a_missing_analysis_and_a_foreign_one_raise_the_same_shape() -> None:
    service, repository, visit_service, _, _ = _service()
    visit = _visit()

    foreign = Mock()
    foreign.visit_id = visit.id
    repository.get_with_graph.return_value = foreign
    _deny_visit(visit_service)
    foreign_id = uuid4()
    with pytest.raises(EntityNotFoundError) as denied:
        service.get_analysis(Mock(), foreign_id, _user())

    repository.get_with_graph.return_value = None
    missing_id = uuid4()
    with pytest.raises(EntityNotFoundError) as missing:
        service.get_analysis(Mock(), missing_id, _user())

    assert denied.value.entity == missing.value.entity == "Analysis"
    assert denied.value.error_code == missing.value.error_code
    assert denied.value.message.replace(
        str(foreign_id), ""
    ) == missing.value.message.replace(str(missing_id), "")


def test_owned_analysis_is_returned() -> None:
    service, repository, visit_service, _, _ = _service()
    visit = _visit()
    analysis = Mock()
    analysis.visit_id = visit.id
    repository.get_with_graph.return_value = analysis
    visit_service.get_visit.return_value = visit

    assert service.get_analysis(Mock(), uuid4(), _user()) is analysis


def test_listing_a_foreign_visits_analyses_is_refused() -> None:
    service, repository, visit_service, _, _ = _service()
    _deny_visit(visit_service)

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.list_visit_analyses(Mock(), uuid4(), _user())

    assert exc_info.value.entity == "Visit"
    repository.get_by_visit.assert_not_called()


def test_listing_returns_items_and_total() -> None:
    service, repository, visit_service, _, _ = _service()
    visit = _visit()
    visit_service.get_visit.return_value = visit
    repository.get_by_visit.return_value = [Mock()]
    repository.count_by_visit.return_value = 3

    items, total = service.list_visit_analyses(Mock(), visit.id, _user())

    assert len(items) == 1
    assert total == 3


def test_latest_raises_when_a_visit_has_no_analysis_yet() -> None:
    service, repository, visit_service, _, _ = _service()
    visit_service.get_visit.return_value = _visit()
    repository.get_latest_by_visit.return_value = None

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.get_latest_for_visit(Mock(), uuid4(), _user())

    assert exc_info.value.entity == "Analysis"


def test_latest_on_a_foreign_visit_is_refused() -> None:
    service, repository, visit_service, _, _ = _service()
    _deny_visit(visit_service)

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.get_latest_for_visit(Mock(), uuid4(), _user())

    assert exc_info.value.entity == "Visit"
    repository.get_latest_by_visit.assert_not_called()
