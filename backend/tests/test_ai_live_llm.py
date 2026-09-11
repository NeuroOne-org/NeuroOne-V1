"""Tests for the live reasoning provider (AI-02 slice 1, ADR-005).

A live model is untrusted output, so most of what matters here is containment
rather than the happy path: what happens to a fabricated citation, an
over-confident likelihood, an early_watch flag with nothing behind it, and a
provider that returns prose instead of JSON.

The suite makes no network calls. There was no HTTP-mocking convention in this
repository before this file, so it uses ``httpx.MockTransport`` injected
through the client's optional ``client`` parameter.
"""

import json
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import httpx
import pytest
from pydantic import ValidationError

from app.ai.orchestrator import (
    HYBRID_PIPELINE_NOTE,
    AnalysisOrchestrator,
)
from app.ai.providers import build_providers
from app.ai.providers.live_llm import LiveLLMClient
from app.ai.providers.mock_llm import MockLLMClient
from app.ai.providers.mock_retriever import MockEvidenceRetriever
from app.ai.trends import detect_trends
from app.core.config import Settings
from app.schemas.analysis import (
    MAX_CONFIDENCE,
    SIMULATED_PIPELINE_NOTE,
    ReasoningRequest,
)
from app.schemas.clinical_context import (
    ClinicalContext,
    ContextSymptom,
    ContextVisit,
)
from app.schemas.evidence import RetrievalQuery
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


def _rising_tremor_context() -> ClinicalContext:
    """The canonical demo case: tremor 3 -> 5 -> 8 across three visits."""
    prior = [
        _visit(("tremor", 3), days_offset=0),
        _visit(("tremor", 5), days_offset=30),
    ]
    return _context(prior, _visit(("tremor", 8), days_offset=60))


def _evidence(context):
    """Real retrieved documents, so cited ids are ones retrieval returned."""
    symptom_names = sorted(
        {s.symptom_name for v in context.all_visits for s in v.symptoms}
    )
    return MockEvidenceRetriever().retrieve(
        RetrievalQuery(
            symptom_names=symptom_names,
            chief_complaint=context.current_visit.chief_complaint,
        )
    )


def _settings(**overrides) -> Settings:
    defaults = {
        "AI_PROVIDER": "live-llm",
        "AI_LLM_BASE_URL": "https://llm.test/v1",
        "AI_LLM_MODEL": "test-model-v1",
        "AI_LLM_API_KEY": "test-key",
    }
    return Settings(**{**defaults, **overrides})


def _llm(handler, **overrides) -> LiveLLMClient:
    return LiveLLMClient(
        _settings(**overrides),
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )


def _returning(content, requests=None) -> LiveLLMClient:
    """A client whose model always answers with ``content``."""

    def handler(request: httpx.Request) -> httpx.Response:
        if requests is not None:
            requests.append(request)
        return httpx.Response(
            200, json={"choices": [{"message": {"content": content}}]}
        )

    return _llm(handler)


def _candidates(**overrides) -> str:
    """One well-formed candidate payload, JSON-encoded as a model would."""
    candidate = {
        "name": "Parkinson's disease",
        "category": "differential_diagnosis",
        "confidence": 0.55,
        "explanation": "Resting tremor with a progressive course.",
        "supporting_findings": ["tremor recorded at severity 8"],
        "contradicting_findings": [],
        "evidence_document_ids": [],
        "trend_symptom_names": [],
    }
    candidate.update(overrides)
    return json.dumps({"candidates": [candidate]})


def _analyze(llm, context):
    return llm.generate_analysis(
        ReasoningRequest(context=context, evidence=_evidence(context))
    )


# --------------------------------------------------------------------------
# Happy path


def test_a_well_formed_response_maps_onto_the_contract():
    context = _context()
    document_id = _evidence(context)[0].document_id
    result = _analyze(
        _returning(_candidates(evidence_document_ids=[document_id])), context
    )

    assert result.provider_mode == "live"
    assert result.model_name == "test-model-v1"
    assert len(result.candidates) == 1

    candidate = result.candidates[0]
    assert candidate.name == "Parkinson's disease"
    assert candidate.category == "differential_diagnosis"
    assert candidate.confidence == 0.55
    assert [item.document_id for item in candidate.evidence] == [document_id]


def test_candidates_are_ranked_by_descending_confidence():
    context = _context()
    document_id = _evidence(context)[0].document_id
    payload = json.dumps(
        {
            "candidates": [
                {
                    "name": "Essential tremor",
                    "category": "differential_diagnosis",
                    "confidence": 0.3,
                    "explanation": "Bilateral action tremor.",
                    "supporting_findings": ["tremor"],
                    "evidence_document_ids": [document_id],
                    "trend_symptom_names": [],
                    "contradicting_findings": [],
                },
                {
                    "name": "Parkinson's disease",
                    "category": "differential_diagnosis",
                    "confidence": 0.7,
                    "explanation": "Resting tremor.",
                    "supporting_findings": ["tremor"],
                    "evidence_document_ids": [document_id],
                    "trend_symptom_names": [],
                    "contradicting_findings": [],
                },
            ]
        }
    )

    result = _analyze(_returning(payload), context)

    assert [c.name for c in result.candidates] == [
        "Parkinson's disease",
        "Essential tremor",
    ]


def test_max_candidates_trims_the_returned_list():
    context = _context()
    document_id = _evidence(context)[0].document_id
    payload = json.dumps(
        {
            "candidates": [
                {
                    "name": f"Condition {index}",
                    "category": "differential_diagnosis",
                    "confidence": 0.5,
                    "explanation": "Considered.",
                    "supporting_findings": ["tremor"],
                    "evidence_document_ids": [document_id],
                    "trend_symptom_names": [],
                    "contradicting_findings": [],
                }
                for index in range(5)
            ]
        }
    )

    result = _returning(payload).generate_analysis(
        ReasoningRequest(
            context=context, evidence=_evidence(context), max_candidates=2
        )
    )

    assert len(result.candidates) == 2


# --------------------------------------------------------------------------
# Citation containment (AGENTS.md section 8.4.4, section 18)


def test_a_hallucinated_document_id_is_dropped():
    """A provider selects evidence by id; it does not get to invent one."""
    context = _context()
    document_id = _evidence(context)[0].document_id
    result = _analyze(
        _returning(
            _candidates(
                evidence_document_ids=[document_id, "doc-does-not-exist"]
            )
        ),
        context,
    )

    assert [item.document_id for item in result.candidates[0].evidence] == [
        document_id
    ]


def test_a_candidate_citing_only_unretrieved_evidence_is_skipped():
    """An uncited ranked condition is the untraceable output section 18 forbids."""
    result = _analyze(
        _returning(_candidates(evidence_document_ids=["doc-invented-01"])),
        _context(),
    )

    assert result.candidates == []


def test_a_candidate_citing_nothing_is_skipped():
    result = _analyze(_returning(_candidates()), _context())

    assert result.candidates == []


def test_repeated_citations_are_deduplicated():
    context = _context()
    document_id = _evidence(context)[0].document_id
    result = _analyze(
        _returning(
            _candidates(evidence_document_ids=[document_id, document_id])
        ),
        context,
    )

    assert len(result.candidates[0].evidence) == 1


def test_cited_evidence_keeps_the_retrieved_metadata():
    """Source metadata is preserved, not taken from the model (section 8.4.4)."""
    context = _context()
    retrieved = _evidence(context)[0]
    result = _analyze(
        _returning(
            _candidates(evidence_document_ids=[retrieved.document_id])
        ),
        context,
    )

    assert result.candidates[0].evidence[0] == retrieved


# --------------------------------------------------------------------------
# Trend containment (AGENTS.md section 8.2)


def test_trend_basis_ids_come_from_the_context_not_the_model():
    """The model names a symptom; the system resolves the ids (ADR-005)."""
    context = _rising_tremor_context()
    document_id = _evidence(context)[0].document_id
    result = _analyze(
        _returning(
            _candidates(
                category="early_watch",
                confidence=0.3,
                evidence_document_ids=[document_id],
                trend_symptom_names=["Tremor"],
            )
        ),
        context,
    )

    candidate = result.candidates[0]
    assert candidate.category == "early_watch"
    assert candidate.trend_basis

    context_visit_ids = {visit.id for visit in context.all_visits}
    context_symptom_ids = {
        symptom.id for visit in context.all_visits for symptom in visit.symptoms
    }
    for ref in candidate.trend_basis:
        assert ref.visit_id in context_visit_ids
        assert ref.symptom_id in context_symptom_ids


def test_early_watch_without_a_resolvable_trend_is_downgraded():
    """The ADR-003 invariant holds by construction, not by raising."""
    context = _rising_tremor_context()
    document_id = _evidence(context)[0].document_id
    result = _analyze(
        _returning(
            _candidates(
                category="early_watch",
                evidence_document_ids=[document_id],
                trend_symptom_names=["a symptom nobody recorded"],
            )
        ),
        context,
    )

    candidate = result.candidates[0]
    assert candidate.category == "differential_diagnosis"
    assert candidate.trend_basis == []


def test_a_non_worsening_trend_does_not_support_an_early_watch():
    context = _context(
        [_visit(("tremor", 8), days_offset=0)],
        _visit(("tremor", 3), days_offset=30),
    )
    document_id = _evidence(context)[0].document_id
    result = _analyze(
        _returning(
            _candidates(
                category="early_watch",
                evidence_document_ids=[document_id],
                trend_symptom_names=["tremor"],
            )
        ),
        context,
    )

    assert result.candidates[0].category == "differential_diagnosis"


def test_a_confidently_ranked_condition_is_not_an_early_watch():
    """early_watch is a low-confidence watch, not a confident finding.

    A real model flagged early_watch at 0.78 with a genuine trend behind it,
    which contradicts ADR-003 decision 4 and disagreed with the rule the mock
    applies. The category is derived, so the two providers cannot drift.
    """
    context = _rising_tremor_context()
    document_id = _evidence(context)[0].document_id
    result = _analyze(
        _returning(
            _candidates(
                category="early_watch",
                confidence=0.78,
                evidence_document_ids=[document_id],
                trend_symptom_names=["tremor"],
            )
        ),
        context,
    )

    candidate = result.candidates[0]
    assert candidate.category == "differential_diagnosis"
    # The trace survives the category decision -- trend_basis is a trace, not
    # a category marker (ADR-003 decision 4).
    assert candidate.trend_basis


def test_a_low_confidence_trend_is_an_early_watch_whatever_the_model_said():
    context = _rising_tremor_context()
    document_id = _evidence(context)[0].document_id
    result = _analyze(
        _returning(
            _candidates(
                category="differential_diagnosis",
                confidence=0.2,
                evidence_document_ids=[document_id],
                trend_symptom_names=["tremor"],
            )
        ),
        context,
    )

    assert result.candidates[0].category == "early_watch"


def test_both_providers_agree_on_what_an_early_watch_means():
    """The seam exists so a category cannot mean two things (ADR-005)."""
    context = _rising_tremor_context()
    evidence = _evidence(context)
    request = ReasoningRequest(context=context, evidence=evidence)

    mock_flags = {
        candidate.category == "early_watch"
        for candidate in MockLLMClient().generate_analysis(request).candidates
        if candidate.confidence < 0.4 and candidate.trend_basis
    }

    live = _returning(
        _candidates(
            category="differential_diagnosis",
            confidence=0.2,
            evidence_document_ids=[evidence[0].document_id],
            trend_symptom_names=["tremor"],
        )
    ).generate_analysis(request)

    assert mock_flags in ({True}, set())
    assert live.candidates[0].category == "early_watch"


def test_an_unrecognized_category_falls_back_to_the_non_flagging_one():
    context = _context()
    document_id = _evidence(context)[0].document_id
    result = _analyze(
        _returning(
            _candidates(
                category="definitely_this_one",
                evidence_document_ids=[document_id],
            )
        ),
        context,
    )

    assert result.candidates[0].category == "differential_diagnosis"


# --------------------------------------------------------------------------
# Certainty ceiling (AGENTS.md section 8.2)


def test_confidence_above_the_ceiling_is_clamped():
    """Section 8.2 forbids expressing certainty; a real model will try."""
    context = _context()
    document_id = _evidence(context)[0].document_id
    result = _analyze(
        _returning(
            _candidates(
                confidence=0.98, evidence_document_ids=[document_id]
            )
        ),
        context,
    )

    assert result.candidates[0].confidence == MAX_CONFIDENCE


def test_a_negative_confidence_is_clamped_to_zero():
    context = _context()
    document_id = _evidence(context)[0].document_id
    result = _analyze(
        _returning(
            _candidates(confidence=-2, evidence_document_ids=[document_id])
        ),
        context,
    )

    assert result.candidates[0].confidence == 0.0


def test_no_live_candidate_expresses_certainty():
    context = _context()
    document_id = _evidence(context)[0].document_id
    result = _analyze(
        _returning(
            _candidates(confidence=1.0, evidence_document_ids=[document_id])
        ),
        context,
    )

    assert all(c.confidence < 1.0 for c in result.candidates)


# --------------------------------------------------------------------------
# Structural failures fail hard (ADR-005)


def test_an_invented_payload_field_is_a_contract_failure():
    """Section 8.2: an invented field is a failure, not a field to ignore."""
    context = _context()
    document_id = _evidence(context)[0].document_id
    payload = _candidates(
        evidence_document_ids=[document_id], trend_basis=[{"visit_id": str(uuid4())}]
    )

    with pytest.raises(ValidationError):
        _analyze(_returning(payload), context)


def test_malformed_json_is_a_contract_failure():
    with pytest.raises(ValidationError):
        _analyze(_returning("I think it might be Parkinson's."), _context())


def test_a_response_missing_candidates_yields_no_candidates():
    result = _analyze(_returning(json.dumps({"candidates": []})), _context())

    assert result.candidates == []


def test_an_unrecognized_completion_envelope_raises():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"unexpected": "shape"})

    with pytest.raises(ValueError, match="chat-completions envelope"):
        _analyze(_llm(handler), _context())


# --------------------------------------------------------------------------
# Transport behaviour


def test_a_transport_failure_propagates_to_the_orchestrator():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("timed out")

    with pytest.raises(httpx.TimeoutException):
        _analyze(_llm(handler), _context())


def test_a_transient_rate_limit_is_retried_once():
    """A free tier rate-limits under load (ADR-005)."""
    context = _context()
    document_id = _evidence(context)[0].document_id
    attempts = []

    def handler(request: httpx.Request) -> httpx.Response:
        attempts.append(request)
        if len(attempts) == 1:
            return httpx.Response(429, json={"error": "slow down"})
        return httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "message": {
                            "content": _candidates(
                                evidence_document_ids=[document_id]
                            )
                        }
                    }
                ]
            },
        )

    result = _analyze(_llm(handler), context)

    assert len(attempts) == 2
    assert len(result.candidates) == 1


def test_a_persistent_rate_limit_raises():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, json={"error": "slow down"})

    with pytest.raises(httpx.HTTPStatusError):
        _analyze(_llm(handler), _context())


def test_a_client_error_is_not_retried():
    attempts = []

    def handler(request: httpx.Request) -> httpx.Response:
        attempts.append(request)
        return httpx.Response(401, json={"error": "bad key"})

    with pytest.raises(httpx.HTTPStatusError):
        _analyze(_llm(handler), _context())

    assert len(attempts) == 1


# --------------------------------------------------------------------------
# The prompt


def test_the_case_is_sent_as_json_data_rather_than_prose():
    """Clinician free text is untrusted input, so it travels as a JSON value."""
    context = _context()
    requests = []
    _analyze(_returning(_candidates(), requests), context)

    body = json.loads(requests[0].content)
    case = json.loads(body["messages"][1]["content"])

    assert case["CURRENT_VISIT"]["chief_complaint"] == (
        "intermittent hand tremor"
    )
    assert case["MAX_CANDIDATES"] == 5


def test_the_prompt_offers_only_retrieved_document_ids():
    context = _context()
    requests = []
    _analyze(_returning(_candidates(), requests), context)

    case = json.loads(
        json.loads(requests[0].content)["messages"][1]["content"]
    )
    offered = {item["document_id"] for item in case["EVIDENCE"]}

    assert offered == {item.document_id for item in _evidence(context)}


def test_the_prompt_carries_no_identifiers_for_the_model_to_echo():
    """No UUID reaches the model, so none can come back (ADR-005)."""
    context = _rising_tremor_context()
    requests = []
    _analyze(_returning(_candidates(), requests), context)

    body = requests[0].content.decode()

    assert str(context.visit_id) not in body
    assert str(context.patient_id) not in body
    for visit in context.all_visits:
        assert str(visit.id) not in body
        for symptom in visit.symptoms:
            assert str(symptom.id) not in body


def test_the_configured_model_and_endpoint_are_used():
    context = _context()
    requests = []
    _analyze(_returning(_candidates(), requests), context)

    request = requests[0]
    assert str(request.url) == "https://llm.test/v1/chat/completions"
    assert request.headers["Authorization"] == "Bearer test-key"
    assert json.loads(request.content)["model"] == "test-model-v1"


# --------------------------------------------------------------------------
# Logging (AGENTS.md section 12)


def test_no_patient_data_is_logged(caplog):
    """Section 12: never put sensitive patient data in logs."""
    context = _context(
        current=_visit(("tremor", 8), complaint="worsening hand tremor at rest")
    )
    document_id = _evidence(context)[0].document_id

    with caplog.at_level("DEBUG"):
        _analyze(
            _returning(
                _candidates(evidence_document_ids=[document_id])
            ),
            context,
        )

    logged = "\n".join(record.getMessage() for record in caplog.records)

    assert "worsening hand tremor at rest" not in logged
    assert "tremor" not in logged
    assert str(context.patient_id) not in logged
    # The operational facts are still there.
    assert "test-model-v1" in logged


# --------------------------------------------------------------------------
# Honest labelling (AGENTS.md section 8.1, ADR-005)


def test_live_reasoning_over_a_simulated_corpus_is_labelled_hybrid():
    """The retriever is still mocked, so the note must not claim otherwise."""
    context = _rising_tremor_context()
    document_id = _evidence(context)[0].document_id
    orchestrator = AnalysisOrchestrator(
        MockEvidenceRetriever(),
        _returning(_candidates(evidence_document_ids=[document_id])),
    )

    result = orchestrator.run(context)

    assert result.provider_mode == "live"
    assert result.pipeline_note == HYBRID_PIPELINE_NOTE
    assert "simulated" in result.pipeline_note


def test_the_mock_pair_is_still_labelled_simulated():
    result = AnalysisOrchestrator(
        MockEvidenceRetriever(), MockLLMClient()
    ).run(_rising_tremor_context())

    assert result.provider_mode == "simulated"
    assert result.pipeline_note == SIMULATED_PIPELINE_NOTE


def test_a_model_failure_is_a_controlled_ai_error():
    """Section 8.5: the clinical record survives a provider failure."""

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("timed out")

    orchestrator = AnalysisOrchestrator(MockEvidenceRetriever(), _llm(handler))

    with pytest.raises(AIError) as exc:
        orchestrator.run(_context())

    assert exc.value.error_code == "ai_error"


def test_malformed_model_output_is_a_controlled_contract_error():
    orchestrator = AnalysisOrchestrator(
        MockEvidenceRetriever(), _returning("not json at all")
    )

    with pytest.raises(AIError) as exc:
        orchestrator.run(_context())

    assert exc.value.error_code == "ai_contract_error"


def test_an_analysis_with_every_candidate_dropped_raises():
    orchestrator = AnalysisOrchestrator(
        MockEvidenceRetriever(),
        _returning(_candidates(evidence_document_ids=["doc-invented-01"])),
    )

    with pytest.raises(AIError) as exc:
        orchestrator.run(_context())

    assert exc.value.error_code == "ai_no_candidates"


# --------------------------------------------------------------------------
# Provider selection


def test_build_providers_returns_the_live_pair_when_configured():
    retriever, llm, _ = build_providers(_settings())

    assert isinstance(llm, LiveLLMClient)
    assert llm.provenance == "live"
    assert llm.name == "test-model-v1"


def test_the_live_pair_keeps_the_simulated_retriever():
    """AI-02 slice 1 swaps reasoning only (ADR-005)."""
    retriever, _, _ = build_providers(_settings())

    assert isinstance(retriever, MockEvidenceRetriever)
    assert retriever.provenance == "simulated"


def test_build_providers_rejects_a_live_selection_without_a_key():
    with pytest.raises(ValueError, match="AI_LLM_API_KEY"):
        build_providers(_settings(AI_LLM_API_KEY=None))


def test_build_providers_still_defaults_to_the_mock_pair():
    retriever, llm, _ = build_providers(_settings(AI_PROVIDER="mock"))

    assert isinstance(retriever, MockEvidenceRetriever)
    assert isinstance(llm, MockLLMClient)
