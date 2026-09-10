"""Tests for the mocked retriever and reasoner.

Two properties matter most here. First the corpus invariants: every condition
must be able to cite something, or it would be silently dropped for lacking
evidence. Second determinism: the same context must produce byte-identical
output, which is what AGENTS.md section 8.1 requires of a mock provider.
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.ai.corpus.mock_corpus import DOCUMENTS_BY_ID, MOCK_CONDITIONS, MOCK_DOCUMENTS
from app.ai.providers import build_providers
from app.ai.providers.mock_llm import MockLLMClient
from app.ai.providers.mock_retriever import MockEvidenceRetriever
from app.ai.trends import detect_trends
from app.schemas.analysis import MAX_CONFIDENCE, ReasoningRequest
from app.schemas.clinical_context import (
    ClinicalContext,
    ContextSymptom,
    ContextVisit,
)
from app.schemas.evidence import RetrievalQuery


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


def _analyze(context, retriever=None, llm=None):
    retriever = retriever or MockEvidenceRetriever()
    llm = llm or MockLLMClient()
    symptom_names = sorted(
        {s.symptom_name for v in context.all_visits for s in v.symptoms}
    )
    documents = retriever.retrieve(
        RetrievalQuery(
            symptom_names=symptom_names,
            chief_complaint=context.current_visit.chief_complaint,
        )
    )
    return llm.generate_analysis(
        ReasoningRequest(context=context, evidence=documents)
    )


# --------------------------------------------------------------------------
# Corpus invariants
# --------------------------------------------------------------------------


def test_every_condition_can_cite_at_least_one_real_document() -> None:
    """A condition with no resolvable citation would be silently dropped."""
    for condition in MOCK_CONDITIONS:
        assert condition.document_ids, condition.name
        for document_id in condition.document_ids:
            assert document_id in DOCUMENTS_BY_ID, (condition.name, document_id)


def test_every_document_carries_a_citation_and_a_passage() -> None:
    for document in MOCK_DOCUMENTS:
        assert document.source.strip()
        assert document.citation.strip()
        assert document.relevant_passage.strip()
        assert document.keywords


def test_document_ids_are_unique() -> None:
    ids = [document.document_id for document in MOCK_DOCUMENTS]

    assert len(ids) == len(set(ids))


def test_corpus_is_labelled_as_simulated() -> None:
    """The fixture must not read as real literature."""
    for document in MOCK_DOCUMENTS:
        assert "simulated" in document.citation.lower()


# --------------------------------------------------------------------------
# Retriever
# --------------------------------------------------------------------------


def test_retriever_returns_relevant_documents_most_relevant_first() -> None:
    documents = MockEvidenceRetriever().retrieve(
        RetrievalQuery(symptom_names=["tremor", "bradykinesia"])
    )

    assert documents
    scores = [document.relevance_score for document in documents]
    assert scores == sorted(scores, reverse=True)
    assert scores[0] == 1.0


def test_retriever_returns_nothing_for_an_unmatched_query() -> None:
    """An empty result is a legitimate outcome, not an exception."""
    documents = MockEvidenceRetriever().retrieve(
        RetrievalQuery(symptom_names=["entirely-unrelated-finding"])
    )

    assert documents == []


def test_retriever_honours_max_results() -> None:
    documents = MockEvidenceRetriever().retrieve(
        RetrievalQuery(symptom_names=["tremor", "memory loss", "numbness"], max_results=2)
    )

    assert len(documents) == 2


def test_retriever_is_deterministic() -> None:
    query = RetrievalQuery(symptom_names=["tremor"], chief_complaint="tremor")
    retriever = MockEvidenceRetriever()

    first = retriever.retrieve(query)
    second = retriever.retrieve(query)

    assert [d.model_dump() for d in first] == [d.model_dump() for d in second]


def test_retriever_prioritizes_trusted_tiers_on_equal_matches() -> None:
    """AGENTS.md 8.4: trusted medical sources are prioritized."""
    documents = MockEvidenceRetriever().retrieve(
        RetrievalQuery(symptom_names=["memory loss", "cognitive decline"])
    )
    tiers = [document.source_tier for document in documents]

    assert tiers[0] in {"guideline", "systematic_review"}


# --------------------------------------------------------------------------
# Reasoner
# --------------------------------------------------------------------------


def test_reasoner_ranks_candidates_by_descending_confidence() -> None:
    result = _analyze(_rising_tremor_context())

    confidences = [candidate.confidence for candidate in result.candidates]
    assert confidences == sorted(confidences, reverse=True)
    assert result.provider_mode == "simulated"
    assert result.model_name == "neuroone-mock-reasoner-v1"


def test_every_candidate_carries_at_least_one_citation() -> None:
    result = _analyze(_rising_tremor_context())

    assert result.candidates
    for candidate in result.candidates:
        assert candidate.evidence


def test_no_candidate_expresses_certainty() -> None:
    """AGENTS.md 8.2: confidence is likelihood, never certainty."""
    result = _analyze(_rising_tremor_context())

    for candidate in result.candidates:
        assert candidate.confidence <= MAX_CONFIDENCE


def test_severity_changes_the_ranking() -> None:
    """The property a seeded RNG or a canned fixture would not have."""
    mild = _analyze(_context(current=_visit(("tremor", 2))))
    severe = _analyze(_context(current=_visit(("tremor", 9))))

    mild_top = {c.name: c.confidence for c in mild.candidates}
    severe_top = {c.name: c.confidence for c in severe.candidates}

    shared = set(mild_top) & set(severe_top)
    assert shared
    assert any(severe_top[name] > mild_top[name] for name in shared)


def test_contradicting_findings_lower_confidence_and_are_reported() -> None:
    without = _analyze(_context(current=_visit(("tremor", 6))))
    with_contra = _analyze(
        _context(current=_visit(("tremor", 6), ("bradykinesia", 6)))
    )

    essential_without = next(
        c for c in without.candidates if c.name == "Essential tremor"
    )
    essential_with = next(
        c for c in with_contra.candidates if c.name == "Essential tremor"
    )

    assert essential_with.confidence < essential_without.confidence
    assert essential_with.contradicting_findings


def test_unmatched_presentation_yields_an_empty_differential() -> None:
    context = _context(
        current=_visit(("entirely-unrelated-finding", 5), complaint="unrelated")
    )

    assert _analyze(context).candidates == []


def test_reasoner_is_deterministic() -> None:
    """AGENTS.md 8.1: schema-valid deterministic results."""
    context = _rising_tremor_context()

    first = _analyze(context)
    second = _analyze(context)

    assert first.model_dump_json() == second.model_dump_json()


def test_registry_builds_the_mock_pair() -> None:
    retriever, llm = build_providers()

    assert retriever.provenance == "simulated"
    assert llm.provenance == "simulated"
