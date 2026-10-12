"""Tests for the imaging staging seam (ADR-006).

Mirrors test_ai_mock_providers.py and test_ai_orchestrator.py: determinism of
the mock provider itself, then the orchestrator wiring that folds a stage
estimate into the same cited, ranked candidate shape everything else in the
pipeline produces.
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from app.ai.orchestrator import AnalysisOrchestrator
from app.ai.providers import build_providers
from app.ai.providers.mock_staging import MIN_STAGING_CONFIDENCE, MockImagingStager
from app.ai.trends import detect_stage_trend, detect_trends
from app.schemas.analysis import MAX_CONFIDENCE
from app.schemas.clinical_context import (
    ClinicalContext,
    ContextSymptom,
    ContextVisit,
    ScanSummary,
)
from app.schemas.imaging import STAGE_LABELS, StagingRequest, StagingResult
from app.utils.exceptions import AIError


BASE_DATE = datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc)


def _scan(checksum="a" * 64) -> ScanSummary:
    return ScanSummary(
        checksum=checksum,
        content_type="application/dicom",
        dimensions={"width": 256, "height": 256, "slices": 120},
    )


def _visit_with_scan(
    scan: ScanSummary | None,
    complaint="intermittent hand tremor",
    days_offset=0,
):
    return ContextVisit(
        id=uuid4(),
        visit_date=BASE_DATE + timedelta(days=days_offset),
        chief_complaint=complaint,
        symptoms=[ContextSymptom(id=uuid4(), symptom_name="tremor", severity=6)],
        scan=scan,
    )


def _context(scan: ScanSummary | None, prior=()) -> ClinicalContext:
    current = _visit_with_scan(scan, days_offset=60)
    prior = list(prior)
    return ClinicalContext(
        patient_id=uuid4(),
        visit_id=current.id,
        current_visit=current,
        prior_visits=prior,
        trends=detect_trends([*prior, current]),
    )


# --------------------------------------------------------------------------
# MockImagingStager
# --------------------------------------------------------------------------


def test_staging_is_deterministic_for_the_same_checksum() -> None:
    stager = MockImagingStager()
    request = StagingRequest(
        checksum="b" * 64, content_type="application/dicom", dimensions={}
    )

    first = stager.stage(request)
    second = stager.stage(request)

    assert first == second


def test_different_checksums_can_stage_differently() -> None:
    stager = MockImagingStager()

    results = {
        stager.stage(
            StagingRequest(checksum=f"{i:064x}", content_type="image/png", dimensions={})
        ).stage
        for i in range(10)
    }

    assert len(results) > 1


def test_staging_confidence_never_exceeds_the_certainty_ceiling() -> None:
    """AGENTS.md 8.2's ceiling applies to imaging staging too (ADR-006)."""
    stager = MockImagingStager()

    for i in range(20):
        result = stager.stage(
            StagingRequest(checksum=f"{i:064x}", content_type="image/png", dimensions={})
        )
        assert MIN_STAGING_CONFIDENCE <= result.confidence <= MAX_CONFIDENCE


def test_staging_is_labelled_as_simulated() -> None:
    stager = MockImagingStager()
    result = stager.stage(
        StagingRequest(checksum="c" * 64, content_type="image/png", dimensions={})
    )

    assert result.provenance == "simulated"
    assert result.stage in STAGE_LABELS


def test_contributing_regions_are_capped_and_ordered() -> None:
    stager = MockImagingStager()
    result = stager.stage(
        StagingRequest(checksum="d" * 64, content_type="image/png", dimensions={})
    )

    assert 1 <= len(result.contributing_regions) <= 3
    contributions = [region.contribution for region in result.contributing_regions]
    assert contributions == sorted(contributions, reverse=True)


# --------------------------------------------------------------------------
# Orchestrator integration
# --------------------------------------------------------------------------


def _orchestrator(**kwargs) -> AnalysisOrchestrator:
    retriever, llm, stager = build_providers()
    return AnalysisOrchestrator(retriever, llm, stager, **kwargs)


def test_a_scanned_visit_produces_a_staged_candidate() -> None:
    result = _orchestrator().run(_context(_scan()))

    stage_names = set(STAGE_LABELS.values())
    staged = [c for c in result.candidates if c.name in stage_names]

    assert staged, "a scanned visit must surface a stage estimate candidate"
    for candidate in staged:
        assert candidate.evidence
        assert candidate.category == "differential_diagnosis"


def test_a_symptoms_only_visit_produces_no_staged_candidate() -> None:
    """MRI is optional (ADR-006 decision 1): no scan, no staging step."""
    result = _orchestrator().run(_context(None))

    stage_names = set(STAGE_LABELS.values())
    assert not any(c.name in stage_names for c in result.candidates)


def test_pipeline_note_discloses_imaging_staging_when_a_scan_is_present() -> None:
    result = _orchestrator().run(_context(_scan()))

    assert "imaging staging simulated" in result.pipeline_note


def test_pipeline_note_omits_imaging_staging_without_a_scan() -> None:
    result = _orchestrator().run(_context(None))

    assert "imaging staging" not in result.pipeline_note


def test_a_scan_with_no_configured_stager_raises_a_controlled_error() -> None:
    retriever, llm, _ = build_providers()
    orchestrator = AnalysisOrchestrator(retriever, llm)  # no stager

    with pytest.raises(AIError) as exc_info:
        orchestrator.run(_context(_scan()))

    assert exc_info.value.error_code == "staging_error"


def test_staged_candidate_confidence_never_exceeds_the_certainty_ceiling() -> None:
    result = _orchestrator().run(_context(_scan()))

    for candidate in result.candidates:
        assert candidate.confidence <= MAX_CONFIDENCE


def test_staging_pipeline_is_deterministic() -> None:
    context = _context(_scan())
    orchestrator = _orchestrator()

    first = orchestrator.run(context).model_dump(exclude={"generated_at"})
    second = orchestrator.run(context).model_dump(exclude={"generated_at"})

    assert first == second


# --------------------------------------------------------------------------
# Cross-visit stage trend (ADR-006: detect_trends extended to scan data)
# --------------------------------------------------------------------------


def test_detect_stage_trend_requires_two_distinct_visits() -> None:
    result = StagingResult(
        model_name="x", provenance="simulated", stage="CN", confidence=0.6
    )

    assert detect_stage_trend([(uuid4(), BASE_DATE, result)]) is None


def test_detect_stage_trend_classifies_worsening_direction() -> None:
    cn = StagingResult(
        model_name="x", provenance="simulated", stage="CN", confidence=0.6
    )
    severe = StagingResult(
        model_name="x", provenance="simulated", stage="Severe", confidence=0.8
    )

    trend = detect_stage_trend(
        [
            (uuid4(), BASE_DATE, cn),
            (uuid4(), BASE_DATE + timedelta(days=90), severe),
        ]
    )

    assert trend is not None
    assert trend.direction == "worsening"
    assert trend.first_stage == "CN"
    assert trend.latest_stage == "Severe"


def _checksum_for_stage(target_stage: str, limit: int = 2000) -> str:
    stager = MockImagingStager()
    for i in range(limit):
        checksum = f"{i:064x}"
        request = StagingRequest(
            checksum=checksum, content_type="application/dicom", dimensions={}
        )
        if stager.stage(request).stage == target_stage:
            return checksum

    raise AssertionError(f"no checksum found for stage {target_stage!r}")


def test_a_worsening_imaging_trend_enriches_the_staged_candidates_traceability() -> None:
    prior_visit = _visit_with_scan(_scan(_checksum_for_stage("CN")), days_offset=0)
    context = _context(_scan(_checksum_for_stage("Severe")), prior=[prior_visit])

    result = _orchestrator().run(context)

    stage_names = set(STAGE_LABELS.values())
    staged = next(c for c in result.candidates if c.name in stage_names)

    assert staged.trend_basis
    assert all(ref.symptom_name == "MRI-derived stage" for ref in staged.trend_basis)
    assert all(ref.visit_id in {prior_visit.id, context.current_visit.id} for ref in staged.trend_basis)


# --------------------------------------------------------------------------
# Stage-first ranking (PRD FR-04, ADR-006 decision 3) and the ceiling
# --------------------------------------------------------------------------


def _strong_parkinsonian_context(checksum: str) -> ClinicalContext:
    """The audit's counterexample: symptoms that out-score the stage."""
    current = ContextVisit(
        id=uuid4(),
        visit_date=BASE_DATE,
        chief_complaint="intermittent hand tremor",
        symptoms=[
            ContextSymptom(id=uuid4(), symptom_name=name, severity=10)
            for name in ("tremor", "bradykinesia", "rigidity", "gait disturbance")
        ],
        scan=_scan(checksum),
    )
    return ClinicalContext(
        patient_id=uuid4(),
        visit_id=current.id,
        current_visit=current,
        prior_visits=[],
        trends=detect_trends([current]),
    )


def test_the_stage_ranks_first_even_below_a_stronger_symptom_candidate() -> None:
    result = _orchestrator().run(_strong_parkinsonian_context("0" * 63 + "1"))

    stage, *rest = result.candidates
    assert stage.name in STAGE_LABELS.values()
    # Pinned, not inflated: a stronger symptom candidate keeps its number.
    assert any(c.confidence > stage.confidence for c in rest)
    assert [c.confidence for c in rest] == sorted(
        (c.confidence for c in rest), reverse=True
    )


def test_trimming_to_one_candidate_keeps_the_stage() -> None:
    result = _orchestrator(max_candidates=1).run(
        _strong_parkinsonian_context("0" * 63 + "1")
    )

    assert [c.name for c in result.candidates][0] in STAGE_LABELS.values()
    assert len(result.candidates) == 1


class _StageDroppingLLM:
    """A reasoner that ignores the scan, as a live model might."""

    name = "drops-stage"
    provenance = "simulated"

    def __init__(self, inner):
        self._inner = inner

    def generate_analysis(self, request):
        result = self._inner.generate_analysis(request)
        return result.model_copy(
            update={
                "candidates": [
                    c
                    for c in result.candidates
                    if c.name not in STAGE_LABELS.values()
                ]
            }
        )


def test_a_scanned_visit_whose_stage_was_dropped_fails_controlled() -> None:
    retriever, llm, stager = build_providers()
    orchestrator = AnalysisOrchestrator(
        retriever, _StageDroppingLLM(llm), stager
    )

    with pytest.raises(AIError) as exc_info:
        orchestrator.run(_context(_scan()))

    assert exc_info.value.error_code == "ai_stage_missing"


def _candidate(name: str, confidence: float):
    from app.ai.providers.mock_retriever import MockEvidenceRetriever
    from app.schemas.analysis import DiagnosisCandidate
    from app.schemas.evidence import RetrievalQuery

    [document, *_] = MockEvidenceRetriever().retrieve(
        RetrievalQuery(symptom_names=["tremor"], chief_complaint="tremor")
    )
    return DiagnosisCandidate(
        name=name,
        category="differential_diagnosis",
        confidence=confidence,
        supporting_findings=["finding"],
        explanation="why",
        evidence=[document],
    )


def _result(*candidates):
    from app.schemas.analysis import AnalysisResult

    return AnalysisResult(
        visit_id=uuid4(),
        patient_id=uuid4(),
        model_name="m",
        provider_mode="simulated",
        pipeline_note="n",
        disclaimer="d",
        generated_at=BASE_DATE,
        candidates=list(candidates),
    )


def test_only_a_stage_may_sit_above_a_more_confident_candidate() -> None:
    from pydantic import ValidationError

    _result(_candidate("Mild dementia", 0.6), _candidate("Essential tremor", 0.8))

    with pytest.raises(ValidationError):
        _result(
            _candidate("Essential tremor", 0.6),
            _candidate("Parkinsonian syndrome", 0.8),
        )


def test_the_ceiling_is_enforced_by_the_contract_not_only_the_providers() -> None:
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        _candidate("Essential tremor", MAX_CONFIDENCE + 0.01)
    with pytest.raises(ValidationError):
        StagingResult(
            model_name="x",
            provenance="live",
            stage="CN",
            confidence=MAX_CONFIDENCE + 0.01,
        )
