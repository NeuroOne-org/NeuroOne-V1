"""Deterministic stand-in for a retrieval corpus and a reasoning model.

Everything here is SIMULATED. The passages are written for this fixture; they
are not quotations from real literature, and the citations are illustrative
rather than resolvable. AI-02 replaces this file wholesale with a real corpus
behind ``app/ai/providers/base.py``.

Determinism is achieved by making the output a pure function of the clinical
context -- no RNG, no canned results. See ADR-003 for why both alternatives
were rejected.
"""

from dataclasses import dataclass, field

from app.schemas.evidence import RetrievedDocument
from app.schemas.imaging import STAGE_LABELS, StageLabel


# Scoring weights. Tuned so a strong presentation lands in the moderate/high
# band while a weak signal riding a worsening trend lands below the
# differential threshold, which is what makes it an early_watch.
BASE_SYMPTOM_WEIGHT = 0.12
COMPLAINT_WEIGHT = 0.15
TREND_WEIGHT = 0.10
CONTRADICTION_WEIGHT = 0.12
MIN_CONFIDENCE = 0.05


@dataclass(frozen=True)
class MockCondition:
    """A rule mapping clinical findings to a candidate condition."""

    name: str
    any_symptoms: frozenset[str]
    complaint_terms: frozenset[str]
    contradicting_symptoms: frozenset[str]
    base_likelihood: float
    explanation_template: str
    document_ids: tuple[str, ...]
    trend_sensitive: bool = True
    supporting_notes: tuple[str, ...] = field(default_factory=tuple)


def _document(
    document_id: str,
    source: str,
    citation: str,
    passage: str,
    tier: str,
    year: int,
    keywords: tuple[str, ...],
) -> RetrievedDocument:
    return RetrievedDocument(
        document_id=document_id,
        chunk_id=f"{document_id}#c1",
        source=source,
        citation=citation,
        relevant_passage=passage,
        source_url=None,
        source_tier=tier,  # type: ignore[arg-type]
        published_year=year,
        keywords=keywords,
    )


MOCK_DOCUMENTS: tuple[RetrievedDocument, ...] = (
    _document(
        "doc-park-01",
        "Movement Disorders Review",
        "Illustrative reference (simulated corpus), Mov Disord Rev. 2023;18(2):88-101.",
        "Asymmetric resting tremor combined with bradykinesia is described as a "
        "core motor presentation of parkinsonian syndromes.",
        "systematic_review",
        2023,
        ("tremor", "resting tremor", "bradykinesia", "rigidity", "parkinsonian"),
    ),
    _document(
        "doc-park-02",
        "Clinical Neurology Guidelines",
        "Illustrative reference (simulated corpus), Clin Neurol Guidel. 2022;9:41-59.",
        "Gradual onset and progression of motor severity across successive "
        "assessments is noted as characteristic of neurodegenerative parkinsonism.",
        "guideline",
        2022,
        ("bradykinesia", "progression", "parkinsonian", "gait disturbance"),
    ),
    _document(
        "doc-et-01",
        "Tremor Research Quarterly",
        "Illustrative reference (simulated corpus), Tremor Res Q. 2021;12(4):203-215.",
        "Action tremor without bradykinesia or rigidity is more consistent with "
        "essential tremor than with a parkinsonian syndrome.",
        "primary_study",
        2021,
        ("tremor", "action tremor", "essential tremor"),
    ),
    _document(
        "doc-cog-01",
        "Journal of Cognitive Neurology",
        "Illustrative reference (simulated corpus), J Cogn Neurol. 2024;31(1):15-29.",
        "Progressive episodic memory impairment with word-finding difficulty is "
        "reported as an early amnestic presentation.",
        "systematic_review",
        2024,
        ("memory loss", "aphasia", "word-finding", "confusion", "cognitive decline"),
    ),
    _document(
        "doc-cog-02",
        "Dementia Care Guidelines",
        "Illustrative reference (simulated corpus), Dement Care Guidel. 2023;7:77-95.",
        "Serial cognitive assessment across visits is recommended over a single "
        "snapshot when characterising suspected progressive decline.",
        "guideline",
        2023,
        ("memory loss", "cognitive decline", "progression", "disorientation"),
    ),
    _document(
        "doc-vasc-01",
        "Cerebrovascular Medicine",
        "Illustrative reference (simulated corpus), Cerebrovasc Med. 2022;44(6):310-322.",
        "Stepwise cognitive change with focal neurological signs is described as "
        "favouring a vascular contribution.",
        "primary_study",
        2022,
        ("memory loss", "weakness", "confusion", "vascular", "focal deficit"),
    ),
    _document(
        "doc-ms-01",
        "Demyelinating Disease Reports",
        "Illustrative reference (simulated corpus), Demyelinating Dis Rep. 2023;15(3):130-144.",
        "Relapsing sensory disturbance with ataxia and visual symptoms in younger "
        "adults is discussed as a demyelinating pattern.",
        "systematic_review",
        2023,
        ("ataxia", "numbness", "visual disturbance", "demyelinating", "paresthesia"),
    ),
    _document(
        "doc-neuro-01",
        "Peripheral Nerve Studies",
        "Illustrative reference (simulated corpus), Peripher Nerve Stud. 2021;28(2):64-78.",
        "Symmetric distal numbness and paresthesia are characteristic of a "
        "length-dependent peripheral neuropathy.",
        "primary_study",
        2021,
        ("numbness", "paresthesia", "tingling", "neuropathy"),
    ),
    _document(
        "doc-neuro-02",
        "Neurology Reference Text",
        "Illustrative reference (simulated corpus), Neurol Ref Text. 2020;ch.14.",
        "Distal sensory symptoms that remain stable over long intervals are less "
        "suggestive of an actively progressive central process.",
        "reference_text",
        2020,
        ("numbness", "neuropathy", "stable", "sensory"),
    ),
    _document(
        "doc-head-01",
        "Headache Medicine Review",
        "Illustrative reference (simulated corpus), Headache Med Rev. 2022;19(5):221-233.",
        "Recurrent headache with visual aura is described within primary headache "
        "disorders rather than neurodegenerative disease.",
        "systematic_review",
        2022,
        ("headache", "visual disturbance", "aura", "migraine"),
    ),
    # MRI staging citations (ADR-006). One document per stage label, keyed by
    # the exact normalized STAGE_LABELS text so a retrieval query built from
    # a stage code always has something to cite.
    _document(
        "doc-mri-cn-01",
        "Neuroimaging in Aging Reference",
        "Illustrative reference (simulated corpus), Neuroimaging Aging Ref. 2022;5:12-24.",
        "An MRI without significant hippocampal or cortical atrophy is consistent "
        "with a cognitively normal aging pattern.",
        "reference_text",
        2022,
        ("cognitively normal", "mri", "no atrophy", "normal aging"),
    ),
    _document(
        "doc-mri-mci-01",
        "Journal of Neuroimaging in Dementia",
        "Illustrative reference (simulated corpus), J Neuroimaging Dement. 2023;10(2):55-70.",
        "Mild hippocampal volume loss on MRI is described as an early structural "
        "correlate of mild cognitive impairment.",
        "systematic_review",
        2023,
        ("mild cognitive impairment (mci)", "hippocampal atrophy", "mri", "mci"),
    ),
    _document(
        "doc-mri-mild-01",
        "Alzheimer's Imaging Consortium Guidelines",
        "Illustrative reference (simulated corpus), Alz Imaging Guidel. 2022;14:101-118.",
        "Moderate medial temporal lobe atrophy on MRI is reported at the mild "
        "dementia stage of Alzheimer's disease.",
        "guideline",
        2022,
        ("mild dementia", "medial temporal atrophy", "mri", "staging"),
    ),
    _document(
        "doc-mri-moderate-01",
        "Structural MRI in Dementia Progression",
        "Illustrative reference (simulated corpus), Struct MRI Dement Prog. 2021;8(3):140-156.",
        "Widespread cortical atrophy and ventricular enlargement on MRI are "
        "associated with the moderate dementia stage.",
        "primary_study",
        2021,
        ("moderate dementia", "cortical atrophy", "ventricular enlargement", "mri"),
    ),
    _document(
        "doc-mri-severe-01",
        "Advanced Neurodegeneration Imaging Review",
        "Illustrative reference (simulated corpus), Adv Neurodegen Imaging Rev. 2020;6:33-49.",
        "Severe global cortical atrophy on MRI, with marked ventricular enlargement, "
        "is described at the severe dementia stage.",
        "systematic_review",
        2020,
        ("severe dementia", "global atrophy", "mri", "ventricular enlargement"),
    ),
)


MOCK_CONDITIONS: tuple[MockCondition, ...] = (
    MockCondition(
        name="Parkinsonian syndrome",
        any_symptoms=frozenset(
            {"tremor", "resting tremor", "bradykinesia", "rigidity", "gait disturbance"}
        ),
        complaint_terms=frozenset({"tremor", "slow", "stiff", "gait", "shaking"}),
        contradicting_symptoms=frozenset({"action tremor"}),
        base_likelihood=0.20,
        explanation_template=(
            "Motor findings recorded for this patient overlap with the "
            "presentations described for parkinsonian syndromes."
        ),
        document_ids=("doc-park-01", "doc-park-02"),
    ),
    MockCondition(
        name="Essential tremor",
        any_symptoms=frozenset({"tremor", "action tremor"}),
        complaint_terms=frozenset({"tremor", "shaking"}),
        contradicting_symptoms=frozenset({"bradykinesia", "rigidity"}),
        base_likelihood=0.18,
        explanation_template=(
            "Tremor is present without the additional motor features that would "
            "point away from an isolated tremor disorder."
        ),
        document_ids=("doc-et-01",),
    ),
    MockCondition(
        name="Progressive amnestic cognitive impairment",
        any_symptoms=frozenset(
            {"memory loss", "aphasia", "word-finding difficulty", "disorientation", "confusion"}
        ),
        complaint_terms=frozenset({"memory", "forget", "confus", "word"}),
        contradicting_symptoms=frozenset(),
        base_likelihood=0.16,
        explanation_template=(
            "Cognitive findings recorded across this patient's visits overlap "
            "with described early amnestic presentations."
        ),
        document_ids=("doc-cog-01", "doc-cog-02"),
    ),
    MockCondition(
        name="Vascular cognitive impairment",
        any_symptoms=frozenset({"memory loss", "confusion", "weakness", "focal deficit"}),
        complaint_terms=frozenset({"memory", "weak", "stroke"}),
        contradicting_symptoms=frozenset(),
        base_likelihood=0.12,
        explanation_template=(
            "Cognitive findings alongside focal signs raise a vascular "
            "contribution as an alternative to consider."
        ),
        document_ids=("doc-vasc-01",),
    ),
    MockCondition(
        name="Demyelinating disease",
        any_symptoms=frozenset({"ataxia", "numbness", "visual disturbance", "paresthesia"}),
        complaint_terms=frozenset({"balance", "numb", "vision", "tingl"}),
        contradicting_symptoms=frozenset(),
        base_likelihood=0.12,
        explanation_template=(
            "Sensory and coordination findings overlap with described "
            "demyelinating patterns."
        ),
        document_ids=("doc-ms-01",),
    ),
    MockCondition(
        name="Peripheral neuropathy",
        any_symptoms=frozenset({"numbness", "paresthesia", "tingling"}),
        complaint_terms=frozenset({"numb", "tingl", "feet", "hands"}),
        contradicting_symptoms=frozenset({"aphasia", "memory loss"}),
        base_likelihood=0.15,
        explanation_template=(
            "Distal sensory findings are consistent with a peripheral rather "
            "than central process."
        ),
        document_ids=("doc-neuro-01", "doc-neuro-02"),
        trend_sensitive=False,
    ),
)


# One MockCondition per MRI stage label (ADR-006), kept out of MOCK_CONDITIONS
# deliberately: those are evaluated against symptoms, these against a
# StagingResult the mock reasoner receives directly. any_symptoms /
# complaint_terms / contradicting_symptoms go unused on this path but are
# still required by the dataclass, so they are left empty rather than typed
# as optional -- a staging condition is a citation source, not a rule.
STAGE_CONDITIONS: dict[StageLabel, MockCondition] = {
    stage: MockCondition(
        name=STAGE_LABELS[stage],
        any_symptoms=frozenset(),
        complaint_terms=frozenset(),
        contradicting_symptoms=frozenset(),
        base_likelihood=0.0,
        explanation_template=explanation,
        document_ids=(document_id,),
        trend_sensitive=False,
    )
    for stage, document_id, explanation in (
        (
            "CN",
            "doc-mri-cn-01",
            "The MRI staging estimate for this scan places it in the "
            "cognitively normal range, with no atrophy pattern noted.",
        ),
        (
            "MCI",
            "doc-mri-mci-01",
            "The MRI staging estimate for this scan is consistent with mild "
            "cognitive impairment, based on the structural pattern observed.",
        ),
        (
            "Mild",
            "doc-mri-mild-01",
            "The MRI staging estimate for this scan is consistent with the "
            "mild dementia stage, based on the structural pattern observed.",
        ),
        (
            "Moderate",
            "doc-mri-moderate-01",
            "The MRI staging estimate for this scan is consistent with the "
            "moderate dementia stage, based on the structural pattern observed.",
        ),
        (
            "Severe",
            "doc-mri-severe-01",
            "The MRI staging estimate for this scan is consistent with the "
            "severe dementia stage, based on the structural pattern observed.",
        ),
    )
}


DOCUMENTS_BY_ID: dict[str, RetrievedDocument] = {
    document.document_id: document for document in MOCK_DOCUMENTS
}


__all__ = [
    "BASE_SYMPTOM_WEIGHT",
    "COMPLAINT_WEIGHT",
    "CONTRADICTION_WEIGHT",
    "DOCUMENTS_BY_ID",
    "MIN_CONFIDENCE",
    "MOCK_CONDITIONS",
    "MOCK_DOCUMENTS",
    "MockCondition",
    "STAGE_CONDITIONS",
    "TREND_WEIGHT",
]
