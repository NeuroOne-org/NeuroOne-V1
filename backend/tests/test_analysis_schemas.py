"""Contract tests for the structured AI output schema.

The first four cases are the ones AGENTS.md section 14 names as required:
valid output accepted, missing evidence rejected, malformed confidence
rejected, and early_watch without trend_basis rejected.
"""

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.analysis import (
    DISCLAIMER,
    MAX_CONFIDENCE,
    SIMULATED_PIPELINE_NOTE,
    AnalysisResult,
    DiagnosisCandidate,
    ReasoningResult,
    TrendBasisRef,
)
from app.schemas.evidence import EvidenceRef


NOW = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)


def _evidence(**overrides) -> EvidenceRef:
    payload = {
        "source": "Journal of Neurology",
        "citation": "Doe J et al. Early motor signs. J Neurol. 2024;271(3):112-120.",
        "relevant_passage": "Progressive resting tremor is an early motor sign.",
    }
    payload.update(overrides)
    return EvidenceRef(**payload)


def _trend_ref(**overrides) -> TrendBasisRef:
    payload = {
        "visit_id": uuid4(),
        "symptom_id": uuid4(),
        "symptom_name": "resting tremor",
        "visit_date": NOW,
        "severity": 3,
        "observation": "resting tremor severity 3 -> 8 across 3 visits",
    }
    payload.update(overrides)
    return TrendBasisRef(**payload)


def _candidate(**overrides) -> dict:
    payload = {
        "name": "Parkinsonian syndrome",
        "category": "differential_diagnosis",
        "confidence": 0.55,
        "supporting_findings": ["resting tremor severity 8", "bradykinesia"],
        "contradicting_findings": [],
        "explanation": "Motor findings across visits are consistent with...",
        "trend_basis": [],
        "evidence": [_evidence()],
    }
    payload.update(overrides)
    return payload


# --------------------------------------------------------------------------
# The four cases AGENTS.md section 14 requires
# --------------------------------------------------------------------------


def test_valid_output_is_accepted() -> None:
    candidate = DiagnosisCandidate(**_candidate())

    assert candidate.name == "Parkinsonian syndrome"
    assert candidate.category == "differential_diagnosis"
    assert len(candidate.evidence) == 1


def test_missing_evidence_is_rejected() -> None:
    """An uncited ranked condition is untraceable output (section 18)."""
    with pytest.raises(ValidationError) as exc_info:
        DiagnosisCandidate(**_candidate(evidence=[]))

    assert "evidence" in str(exc_info.value)


@pytest.mark.parametrize("confidence", [1.4, -0.1, "high"])
def test_malformed_confidence_is_rejected(confidence) -> None:
    with pytest.raises(ValidationError):
        DiagnosisCandidate(**_candidate(confidence=confidence))


def test_early_watch_without_trend_basis_is_rejected() -> None:
    with pytest.raises(ValidationError) as exc_info:
        DiagnosisCandidate(
            **_candidate(category="early_watch", trend_basis=[])
        )

    assert "trend_basis" in str(exc_info.value)


# --------------------------------------------------------------------------
# The fifth case: trend_basis is a trace, not a category marker
# --------------------------------------------------------------------------


def test_differential_diagnosis_may_also_carry_trend_basis() -> None:
    """Pins the semantic so the validator is never made an exclusive-or.

    early_watch REQUIRES trend_basis; it does not MONOPOLISE it. A condition
    already in the differential can still cite the patient's own history.
    """
    candidate = DiagnosisCandidate(
        **_candidate(
            category="differential_diagnosis",
            trend_basis=[_trend_ref()],
        )
    )

    assert candidate.category == "differential_diagnosis"
    assert len(candidate.trend_basis) == 1


def test_early_watch_with_trend_basis_is_accepted() -> None:
    candidate = DiagnosisCandidate(
        **_candidate(
            category="early_watch",
            confidence=0.28,
            trend_basis=[_trend_ref()],
        )
    )

    assert candidate.category == "early_watch"
    assert candidate.trend_basis[0].symptom_name == "resting tremor"


# --------------------------------------------------------------------------
# Safety-boundary naming and shape
# --------------------------------------------------------------------------


def test_candidate_rejects_an_invented_field() -> None:
    """A model inventing a field is a contract failure, not noise to ignore."""
    with pytest.raises(ValidationError):
        DiagnosisCandidate(**_candidate(final_diagnosis="Parkinson disease"))


def test_contract_exposes_no_definitive_diagnosis_fields() -> None:
    """AGENTS.md 8.2: not in the schema, not in API field naming."""
    fields = set(DiagnosisCandidate.model_fields)

    for forbidden in (
        "final_diagnosis",
        "doctor_verified",
        "certainty",
        "probability",
        "diagnosis",
    ):
        assert forbidden not in fields


def test_unknown_category_is_rejected() -> None:
    with pytest.raises(ValidationError):
        DiagnosisCandidate(**_candidate(category="confirmed"))


def test_supporting_findings_must_not_be_empty() -> None:
    with pytest.raises(ValidationError):
        DiagnosisCandidate(**_candidate(supporting_findings=[]))


# --------------------------------------------------------------------------
# likelihood_band -- the confidence-tiered output of section 8.3
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("confidence", "band"),
    [
        (0.0, "low"),
        (0.39, "low"),
        (0.40, "moderate"),
        (0.69, "moderate"),
        (0.70, "high"),
        (MAX_CONFIDENCE, "high"),
    ],
)
def test_likelihood_band_tiers_at_the_documented_boundaries(
    confidence, band
) -> None:
    candidate = DiagnosisCandidate(**_candidate(confidence=confidence))

    assert candidate.likelihood_band == band


def test_likelihood_band_is_serialized() -> None:
    body = DiagnosisCandidate(**_candidate()).model_dump()

    assert body["likelihood_band"] == "moderate"


# --------------------------------------------------------------------------
# Result envelopes
# --------------------------------------------------------------------------


def _result(candidates) -> dict:
    return {
        "visit_id": uuid4(),
        "patient_id": uuid4(),
        "model_name": "neuroone-mock-reasoner-v1",
        "provider_mode": "simulated",
        "pipeline_note": SIMULATED_PIPELINE_NOTE,
        "disclaimer": DISCLAIMER,
        "generated_at": NOW,
        "candidates": candidates,
    }


def test_analysis_result_accepts_descending_candidates() -> None:
    result = AnalysisResult(
        **_result(
            [
                DiagnosisCandidate(**_candidate(name="A", confidence=0.8)),
                DiagnosisCandidate(**_candidate(name="B", confidence=0.5)),
                DiagnosisCandidate(**_candidate(name="C", confidence=0.5)),
            ]
        )
    )

    assert len(result.candidates) == 3


def test_analysis_result_rejects_unranked_candidates() -> None:
    with pytest.raises(ValidationError) as exc_info:
        AnalysisResult(
            **_result(
                [
                    DiagnosisCandidate(**_candidate(name="A", confidence=0.3)),
                    DiagnosisCandidate(**_candidate(name="B", confidence=0.9)),
                ]
            )
        )

    assert "ranked" in str(exc_info.value)


def test_analysis_result_requires_at_least_one_candidate() -> None:
    with pytest.raises(ValidationError):
        AnalysisResult(**_result([]))


def test_reasoning_result_permits_an_empty_differential() -> None:
    """A provider reporting "nothing matched" is an answer, not malformed output.

    AnalysisResult still requires a candidate; the orchestrator is what turns
    an empty differential into a distinct, controlled error.
    """
    result = ReasoningResult(
        model_name="mock", provider_mode="simulated", candidates=[]
    )

    assert result.candidates == []


def test_disclaimer_does_not_claim_a_diagnosis() -> None:
    lowered = DISCLAIMER.lower()

    assert "not a diagnosis" in lowered
    assert "clinician remains responsible" in lowered
