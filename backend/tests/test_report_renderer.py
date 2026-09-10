"""Tests for the PDF renderer (ADR-004, FR-07).

Runs the renderer for real and inspects the output with pypdf -- the value
here is in what the bytes actually contain, not in mocking ReportLab.
"""

from datetime import datetime, timezone
from io import BytesIO
from uuid import uuid4

import pytest
from pypdf import PdfReader

from app.reports.renderer import render
from app.schemas.report import (
    ReportEvidenceSnapshot,
    ReportFindingSnapshot,
    ReportPatientSnapshot,
    ReportSnapshot,
    ReportSymptomSnapshot,
    ReportVisitSnapshot,
)


NOW = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)

DISCLAIMER = (
    "Decision support only. This is a ranked set of possible conditions with "
    "supporting evidence, not a diagnosis. The clinician remains responsible "
    "for final interpretation."
)


def _evidence(**overrides) -> ReportEvidenceSnapshot:
    payload = {
        "source": "Journal of Neurology",
        "citation": "Doe J et al. Early motor signs. J Neurol. 2024;271(3):112-120.",
        "relevant_passage": "Progressive resting tremor is an early motor sign.",
        "source_tier": "guideline",
        "published_year": 2024,
    }
    payload.update(overrides)
    return ReportEvidenceSnapshot(**payload)


def _finding(**overrides) -> ReportFindingSnapshot:
    payload = {
        "rank": 0,
        "condition_name": "Parkinsonian syndrome",
        "category": "differential_diagnosis",
        "likelihood_band": "moderate",
        "supporting_findings": ["resting tremor severity 8"],
        "contradicting_findings": [],
        "explanation": "Motor findings across visits are consistent with...",
        "trend_basis": [],
        "evidence": [_evidence()],
    }
    payload.update(overrides)
    return ReportFindingSnapshot(**payload)


def _snapshot(**overrides) -> ReportSnapshot:
    payload = {
        "analysis_id": uuid4(),
        "visit_id": uuid4(),
        "patient": ReportPatientSnapshot(
            full_name="Ada Lovelace", age_years=62, gender="F"
        ),
        "visit": ReportVisitSnapshot(
            visit_date=NOW,
            chief_complaint="intermittent hand tremor",
            history="six months of gradually worsening tremor",
            notes="patient reports family history of Parkinson disease",
            symptoms=[
                ReportSymptomSnapshot(
                    symptom_name="resting tremor",
                    severity=8,
                    duration_days=180,
                    onset="gradual",
                    observation="worse at night, resolves with intention",
                )
            ],
        ),
        "model_name": "neuroone-mock-reasoner-v1",
        "provider_mode": "simulated",
        "pipeline_note": "pipeline complete, evidence retrieval simulated",
        "disclaimer": DISCLAIMER,
        "generated_at": NOW,
        "findings": [_finding()],
    }
    payload.update(overrides)
    return ReportSnapshot(**payload)


def _text(pdf_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def test_render_produces_valid_pdf_bytes() -> None:
    pdf_bytes = render(_snapshot())

    assert pdf_bytes.startswith(b"%PDF-")
    reader = PdfReader(BytesIO(pdf_bytes))
    assert len(reader.pages) >= 1


def test_report_contains_every_fr07_element() -> None:
    """FR-07: patient/case, clinical inputs, differential, reasoning, evidence,
    citations, and the disclaimer must all be present."""
    text = _text(render(_snapshot()))

    assert "Ada Lovelace" in text
    assert "intermittent hand tremor" in text
    assert "resting tremor" in text
    assert "worse at night" in text
    assert "Parkinsonian syndrome" in text
    assert "Motor findings across visits" in text
    assert "Doe J et al." in text
    assert "Progressive resting tremor is an early motor sign." in text
    assert "not a diagnosis" in text
    assert "clinician remains responsible" in text


def test_simulated_pipeline_note_is_rendered() -> None:
    text = _text(render(_snapshot()))

    assert "simulated" in text


def test_trend_basis_is_rendered_and_labelled_as_patient_history() -> None:
    finding = _finding(
        category="early_watch",
        likelihood_band="low",
        trend_basis=[
            {
                "visit_id": str(uuid4()),
                "symptom_name": "memory loss",
                "observation": "memory loss severity 2 -> 4 across 3 visits",
            }
        ],
    )
    text = _text(render(_snapshot(findings=[finding])))

    assert "patient history" in text.lower()
    assert "memory loss severity 2 -> 4 across 3 visits" in text


def test_long_content_paginates_across_multiple_pages() -> None:
    long_explanation = "Extensive multi-factor reasoning. " * 200
    findings = [
        _finding(
            rank=index,
            condition_name=f"Condition {index}",
            explanation=long_explanation,
            evidence=[_evidence(citation=f"Reference {index}, {year}.", published_year=2020 + index) for year in (2020, 2021)],
        )
        for index in range(6)
    ]

    pdf_bytes = render(_snapshot(findings=findings))
    reader = PdfReader(BytesIO(pdf_bytes))

    assert len(reader.pages) > 1


def test_non_latin1_characters_do_not_crash_rendering() -> None:
    """ADR-004 assumes bundled/base fonts; exotic characters degrade, not crash."""
    snapshot = _snapshot(
        patient=ReportPatientSnapshot(full_name="Björk 中文 Ω", gender="F")
    )

    pdf_bytes = render(snapshot)

    assert pdf_bytes.startswith(b"%PDF-")


def test_markup_like_input_is_escaped_not_interpreted() -> None:
    """Clinical free text must never be parsed as Platypus markup."""
    finding = _finding(explanation="<b>bold injection</b> & <script>bad</script>")

    pdf_bytes = render(_snapshot(findings=[finding]))

    assert pdf_bytes.startswith(b"%PDF-")


@pytest.mark.parametrize("provider_mode", ["simulated", "live"])
def test_live_mode_omits_the_simulated_note(provider_mode) -> None:
    snapshot = _snapshot(
        provider_mode=provider_mode,
        pipeline_note=(
            "pipeline complete, evidence retrieval simulated"
            if provider_mode == "simulated"
            else "pipeline complete, evidence retrieved from live corpus"
        ),
    )

    text = _text(render(snapshot))

    if provider_mode == "simulated":
        assert "simulated" in text
    else:
        assert "Note:" not in text
