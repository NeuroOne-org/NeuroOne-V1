"""CorpusEvidenceRetriever against a fake CorpusSearch (ADR-007, AI-02b-5).

Fast suite only: no database. `CorpusRepository` and the real Postgres
search are exercised by the Postgres-marked suite instead.
"""

import pytest

from app.ai.providers.base import CorpusHit, CorpusSearch, CorpusSearchTerms
from app.ai.providers.corpus_retriever import CorpusEvidenceRetriever
from app.schemas.evidence import RetrievalQuery


def _hit(**overrides) -> CorpusHit:
    defaults = dict(
        document_id="nice-ng97-2018",
        chunk_id="nice-ng97-2018#c1",
        source="NICE",
        citation="NICE. Dementia. NG97. 2018.",
        relevant_passage="Progressive memory loss is a core feature.",
        source_url="https://example.org/ng97",
        source_tier="guideline",
        published_year=2018,
        keywords=("dementia", "memory loss"),
        rank=0.5,
    )
    defaults.update(overrides)
    return CorpusHit(**defaults)


class _FakeSearch:
    """Records the terms/limit it was called with and returns fixed hits."""

    def __init__(self, hits: list[CorpusHit], *, error: Exception | None = None):
        self._hits = hits
        self._error = error
        self.calls: list[tuple[CorpusSearchTerms, int]] = []

    def search(self, terms: CorpusSearchTerms, *, limit: int) -> list[CorpusHit]:
        self.calls.append((terms, limit))
        if self._error is not None:
            raise self._error
        return list(self._hits)


def _query(**overrides) -> RetrievalQuery:
    defaults = dict(
        condition_names=["Dementia"],
        symptom_names=["Memory loss"],
        chief_complaint="progressive memory loss over six months",
        max_results=12,
    )
    defaults.update(overrides)
    return RetrievalQuery(**defaults)


def test_corpus_search_is_a_runtime_checkable_protocol():
    assert isinstance(_FakeSearch([]), CorpusSearch)


def test_terms_are_built_from_all_three_query_fields():
    search = _FakeSearch([_hit()])
    retriever = CorpusEvidenceRetriever(search, corpus_version="curated-v1")

    retriever.retrieve(_query())

    terms, limit = search.calls[0]
    assert terms.conditions == ("Dementia",)
    assert terms.symptoms == ("Memory loss",)
    assert terms.complaint_terms == (
        "progressive",
        "memory",
        "loss",
        "over",
        "six",
        "months",
    )
    assert limit == 12


def test_complaint_is_capped_at_twenty_tokens():
    search = _FakeSearch([_hit()])
    retriever = CorpusEvidenceRetriever(search, corpus_version="curated-v1")

    long_complaint = " ".join(f"word{i}" for i in range(30))
    retriever.retrieve(_query(chief_complaint=long_complaint))

    terms, _ = search.calls[0]
    assert len(terms.complaint_terms) == 20
    assert terms.complaint_terms[0] == "word0"


def test_out_of_policy_hit_is_dropped():
    search = _FakeSearch([_hit(source_tier="primary_study")])
    retriever = CorpusEvidenceRetriever(search, corpus_version="curated-v1")

    assert retriever.retrieve(_query()) == []


def test_scores_are_normalized_with_top_at_one():
    search = _FakeSearch(
        [
            _hit(document_id="doc-a", chunk_id="doc-a#c1", rank=0.5, source_tier="guideline"),
            _hit(
                document_id="doc-b",
                chunk_id="doc-b#c1",
                rank=0.1,
                source_tier="systematic_review",
            ),
        ]
    )
    retriever = CorpusEvidenceRetriever(search, corpus_version="curated-v1")

    documents = retriever.retrieve(_query())

    assert documents[0].relevance_score == 1.0
    assert 0.0 < documents[1].relevance_score < 1.0


def test_ties_are_ordered_by_document_id_then_chunk_id():
    search = _FakeSearch(
        [
            _hit(document_id="doc-b", chunk_id="doc-b#c1", rank=0.5),
            _hit(document_id="doc-a", chunk_id="doc-a#c2", rank=0.5),
            _hit(document_id="doc-a", chunk_id="doc-a#c1", rank=0.5),
        ]
    )
    retriever = CorpusEvidenceRetriever(search, corpus_version="curated-v1")

    documents = retriever.retrieve(_query())

    assert [d.chunk_id for d in documents] == [
        "doc-a#c1",
        "doc-a#c2",
        "doc-b#c1",
    ]


def test_output_is_identical_across_repeated_runs():
    search = _FakeSearch(
        [
            _hit(document_id="doc-a", chunk_id="doc-a#c1", rank=0.4),
            _hit(document_id="doc-b", chunk_id="doc-b#c1", rank=0.6),
        ]
    )
    retriever = CorpusEvidenceRetriever(search, corpus_version="curated-v1")

    first = retriever.retrieve(_query())
    second = retriever.retrieve(_query())

    assert first == second


def test_max_results_is_honoured_even_if_search_over_returns():
    hits = [
        _hit(document_id=f"doc-{i}", chunk_id=f"doc-{i}#c1", rank=float(i))
        for i in range(5)
    ]
    search = _FakeSearch(hits)
    retriever = CorpusEvidenceRetriever(search, corpus_version="curated-v1")

    documents = retriever.retrieve(_query(max_results=2))

    assert len(documents) == 2


def test_search_exception_propagates():
    search = _FakeSearch([], error=RuntimeError("db unreachable"))
    retriever = CorpusEvidenceRetriever(search, corpus_version="curated-v1")

    with pytest.raises(RuntimeError):
        retriever.retrieve(_query())


def test_keywords_round_trip_to_a_tuple():
    search = _FakeSearch([_hit(keywords=("dementia", "memory loss"))])
    retriever = CorpusEvidenceRetriever(search, corpus_version="curated-v1")

    documents = retriever.retrieve(_query())

    assert documents[0].keywords == ("dementia", "memory loss")
    assert isinstance(documents[0].keywords, tuple)


def test_empty_hits_is_a_legitimate_empty_result():
    search = _FakeSearch([])
    retriever = CorpusEvidenceRetriever(search, corpus_version="curated-v1")

    assert retriever.retrieve(_query()) == []


def test_name_and_provenance_carry_the_corpus_version():
    retriever = CorpusEvidenceRetriever(_FakeSearch([]), corpus_version="curated-v1")

    assert retriever.name == "curated-corpus-curated-v1"
    assert retriever.provenance == "live"
    assert retriever.corpus_version == "curated-v1"
