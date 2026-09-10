"""Pipeline tests covering the AI test category (AGENTS.md section 10, TRD 12).

Structured-output validation, citation presence, traceability, malformed model
output, missing evidence, AI failure and RAG failure. The traceability test is
the load-bearing one: an early_watch flag that cannot be resolved back to the
patient's own records is exactly what section 18 forbids.
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from app.ai.orchestrator import AnalysisOrchestrator
from app.ai.providers import build_providers
from app.ai.trends import detect_trends
from app.schemas.analysis import (
    MAX_CONFIDENCE,
    SIMULATED_PIPELINE_NOTE,
    DiagnosisCandidate,
    ReasoningResult,
)
from app.schemas.clinical_context import (
    ClinicalContext,
    ContextSymptom,
    ContextVisit,
)
from app.schemas.evidence import EvidenceRef, RetrievedDocument
from app.utils.exceptions import AIError


BASE_DATE = datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc)


def _visit(*symptoms, days_offset=0, complaint="intermittent hand tremor"):
    return ContextVisit(
        id=uuid4(),
        visit_date=BASE_DATE + timedelta(days=days_offset),
        chief_complaint=complaint,
        symptoms=[
            ContextSymptom(id=uuid4(), symptom_name=name, severity=severity)
            for name, severity in symptoms
        ],
    )


def _context(prior=(), current=None) -> ClinicalContext:
    current = current or _visit(("tremor", 8))
    prior = list(prior)
    return ClinicalContext(
        patient_id=uuid4(),
        visit_id=current.id,
        current_visit=current,
        prior_visits=prior,
        trends=detect_trends([*prior, current]),
    )


def _rising_trend_context() -> ClinicalContext:
    """The canonical demo case.

    The presenting complaint (tremor) worsens loudly and lands in the
    differential; a second signal (memory loss) worsens quietly and should be
    flagged early_watch. That contrast is the point of the feature.
    """
    prior = [
        _visit(("tremor", 3), ("memory loss", 2), days_offset=0),
        _visit(("tremor", 5), ("memory loss", 3), days_offset=30),
    ]
    current = _visit(("tremor", 8), ("memory loss", 4), days_offset=60)
    return _context(prior, current)


def _orchestrator(**kwargs) -> AnalysisOrchestrator:
    retriever, llm = build_providers()
    return AnalysisOrchestrator(retriever, llm, **kwargs)


class _StubRetriever:
    name = "stub-retriever"
    provenance = "simulated"

    def __init__(self, documents=None, error=None):
        self._documents = documents if documents is not None else []
        self._error = error

    def retrieve(self, query):
        if self._error:
            raise self._error
        return list(self._documents)


class _StubLLM:
    name = "stub-llm"
    provenance = "simulated"

    def __init__(self, result=None, error=None):
        self._result = result
        self._error = error

    def generate_analysis(self, request):
        if self._error:
            raise self._error
        return self._result


def _document(document_id="doc-1") -> RetrievedDocument:
    return RetrievedDocument(
        document_id=document_id,
        chunk_id=f"{document_id}#c1",
        source="Simulated Source",
        citation="Illustrative reference (simulated corpus), 2024.",
        relevant_passage="A passage.",
        source_tier="guideline",
        published_year=2024,
        keywords=("tremor",),
        relevance_score=1.0,
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
        "evidence": [EvidenceRef.model_validate(_document())],
    }
    payload.update(overrides)
    return DiagnosisCandidate(**payload)


# --------------------------------------------------------------------------
# Happy path and structured output
# --------------------------------------------------------------------------


def test_pipeline_returns_validated_ranked_output() -> None:
    result = _orchestrator().run(_rising_trend_context())

    assert result.candidates
    confidences = [candidate.confidence for candidate in result.candidates]
    assert confidences == sorted(confidences, reverse=True)
    assert result.provider_mode == "simulated"
    assert result.model_name == "neuroone-mock-reasoner-v1"


def test_mock_sourced_output_is_labelled_as_simulated() -> None:
    """AGENTS.md 8.1: never let simulated evidence read as clinically validated."""
    result = _orchestrator().run(_rising_trend_context())

    assert result.pipeline_note == SIMULATED_PIPELINE_NOTE
    assert "simulated" in result.pipeline_note


def test_result_carries_a_disclaimer_that_denies_a_diagnosis() -> None:
    result = _orchestrator().run(_rising_trend_context())

    assert "not a diagnosis" in result.disclaimer.lower()


def test_every_candidate_carries_at_least_one_citation() -> None:
    """AGENTS.md 8.4.6 / 18: citations traceable."""
    result = _orchestrator().run(_rising_trend_context())

    for candidate in result.candidates:
        assert candidate.evidence
        for evidence in candidate.evidence:
            assert evidence.source.strip()
            assert evidence.citation.strip()
            assert evidence.relevant_passage.strip()


def test_no_candidate_expresses_certainty() -> None:
    result = _orchestrator().run(_rising_trend_context())

    for candidate in result.candidates:
        assert 0.0 <= candidate.confidence <= MAX_CONFIDENCE


def test_candidate_and_evidence_counts_are_capped() -> None:
    result = _orchestrator(max_candidates=2, evidence_per_candidate=1).run(
        _rising_trend_context()
    )

    assert len(result.candidates) <= 2
    for candidate in result.candidates:
        assert len(candidate.evidence) == 1


# --------------------------------------------------------------------------
# The section 8.1 obligation, and traceability
# --------------------------------------------------------------------------


def test_a_multi_visit_trend_produces_an_early_watch_flag() -> None:
    """AGENTS.md 8.1: the mock must simulate at least one multi-visit trend."""
    result = _orchestrator().run(_rising_trend_context())

    early = [c for c in result.candidates if c.category == "early_watch"]

    assert early, "the rising-trend case must surface an early_watch candidate"
    assert all(candidate.trend_basis for candidate in early)


def test_every_early_watch_traces_to_the_patients_own_records() -> None:
    """The traceability requirement of section 18, asserted end to end."""
    context = _rising_trend_context()
    visits_by_id = {visit.id: visit for visit in context.all_visits}

    result = _orchestrator().run(context)
    early = [c for c in result.candidates if c.category == "early_watch"]
    assert early

    for candidate in early:
        for reference in candidate.trend_basis:
            assert reference.visit_id in visits_by_id, "unknown visit referenced"
            visit = visits_by_id[reference.visit_id]
            symptom_ids = {symptom.id for symptom in visit.symptoms}
            assert reference.symptom_id in symptom_ids, (
                "trend_basis symptom does not belong to the referenced visit"
            )
            assert reference.observation.strip()


def test_a_single_visit_produces_no_early_watch() -> None:
    """Without history there is no trend for an early_watch to point at."""
    result = _orchestrator().run(_context(current=_visit(("tremor", 8))))

    assert all(c.category == "differential_diagnosis" for c in result.candidates)


def test_trend_basis_and_evidence_are_not_conflated() -> None:
    """AGENTS.md 8.2: own history vs external literature are distinct."""
    result = _orchestrator().run(_rising_trend_context())

    for candidate in result.candidates:
        for reference in candidate.trend_basis:
            assert hasattr(reference, "visit_id")
            assert not hasattr(reference, "citation")
        for evidence in candidate.evidence:
            assert hasattr(evidence, "citation")
            assert not hasattr(evidence, "visit_id")


# --------------------------------------------------------------------------
# Failure handling -- AGENTS.md 8.5
# --------------------------------------------------------------------------


def test_retrieval_failure_raises_a_controlled_rag_error() -> None:
    orchestrator = AnalysisOrchestrator(
        _StubRetriever(error=RuntimeError("corpus offline")), _StubLLM()
    )

    with pytest.raises(AIError) as exc_info:
        orchestrator.run(_context())

    assert exc_info.value.error_code == "rag_error"
    assert isinstance(exc_info.value.__cause__, RuntimeError)
    assert "not modified" in exc_info.value.message


def test_missing_evidence_raises_a_distinct_error() -> None:
    orchestrator = AnalysisOrchestrator(_StubRetriever([]), _StubLLM())

    with pytest.raises(AIError) as exc_info:
        orchestrator.run(_context())

    assert exc_info.value.error_code == "rag_no_evidence"


def test_model_failure_raises_a_controlled_ai_error() -> None:
    orchestrator = AnalysisOrchestrator(
        _StubRetriever([_document()]),
        _StubLLM(error=RuntimeError("model offline")),
    )

    with pytest.raises(AIError) as exc_info:
        orchestrator.run(_context())

    assert exc_info.value.error_code == "ai_error"
    assert isinstance(exc_info.value.__cause__, RuntimeError)


def test_malformed_model_output_raises_a_contract_error() -> None:
    """A model that violates the contract fails at the seam."""
    from pydantic import ValidationError

    def _explode(_request):
        raise ValidationError.from_exception_data("ReasoningResult", [])

    llm = _StubLLM()
    llm.generate_analysis = _explode

    orchestrator = AnalysisOrchestrator(_StubRetriever([_document()]), llm)

    with pytest.raises(AIError) as exc_info:
        orchestrator.run(_context())

    assert exc_info.value.error_code == "ai_contract_error"


def test_unrecognized_result_type_raises_a_contract_error() -> None:
    orchestrator = AnalysisOrchestrator(
        _StubRetriever([_document()]), _StubLLM(result={"candidates": []})
    )

    with pytest.raises(AIError) as exc_info:
        orchestrator.run(_context())

    assert exc_info.value.error_code == "ai_contract_error"


def test_an_empty_differential_raises_rather_than_persisting_nothing() -> None:
    orchestrator = AnalysisOrchestrator(
        _StubRetriever([_document()]),
        _StubLLM(
            ReasoningResult(
                model_name="stub", provider_mode="simulated", candidates=[]
            )
        ),
    )

    with pytest.raises(AIError) as exc_info:
        orchestrator.run(_context())

    assert exc_info.value.error_code == "ai_no_candidates"


def test_every_failure_message_avoids_leaking_provider_internals() -> None:
    orchestrator = AnalysisOrchestrator(
        _StubRetriever(error=RuntimeError("postgres://secret@host/db")),
        _StubLLM(),
    )

    with pytest.raises(AIError) as exc_info:
        orchestrator.run(_context())

    assert "secret" not in exc_info.value.message


# --------------------------------------------------------------------------
# Determinism
# --------------------------------------------------------------------------


def test_pipeline_is_deterministic_apart_from_its_timestamp() -> None:
    context = _rising_trend_context()
    orchestrator = _orchestrator()

    first = orchestrator.run(context).model_dump(exclude={"generated_at"})
    second = orchestrator.run(context).model_dump(exclude={"generated_at"})

    assert first == second
