"""Deterministic stand-in for the reasoning model.

Scores the frozen condition rules against the clinical context. The result is a
pure function of what the clinician entered -- change a severity and the
ranking changes, which is the property a seeded RNG or a canned fixture would
not have (ADR-003).

SIMULATED: this performs no learned inference of any kind. AI-02 replaces this
class behind ``LLMClient``.
"""

from app.ai.corpus.mock_corpus import (
    BASE_SYMPTOM_WEIGHT,
    COMPLAINT_WEIGHT,
    CONTRADICTION_WEIGHT,
    MIN_CONFIDENCE,
    MOCK_CONDITIONS,
    STAGE_CONDITIONS,
    TREND_WEIGHT,
    MockCondition,
)
from app.ai.trends import (
    normalize_symptom_name,
    stage_trend_basis_ref,
    trend_basis_refs,
    worsening_symptom_names,
)
from app.schemas.analysis import (
    MAX_CONFIDENCE,
    MODERATE_CONFIDENCE,
    DiagnosisCandidate,
    ReasoningRequest,
    ReasoningResult,
)
from app.schemas.clinical_context import ClinicalContext, ScanTrend
from app.schemas.evidence import RetrievedDocument
from app.schemas.imaging import StagingResult


class MockLLMClient:
    """Rule-based reasoner over the frozen condition table."""

    name = "neuroone-mock-reasoner-v1"
    provenance = "simulated"

    def __init__(self, conditions: tuple[MockCondition, ...] = MOCK_CONDITIONS):
        self._conditions = conditions

    # -- scoring ---------------------------------------------------------

    def _observed_severities(self, context: ClinicalContext) -> dict[str, int]:
        """Highest recorded severity per symptom, across every visit."""

        severities: dict[str, int] = {}
        for visit in context.all_visits:
            for symptom in visit.symptoms:
                key = normalize_symptom_name(symptom.symptom_name)
                severities[key] = max(severities.get(key, 0), symptom.severity)
        return severities

    def _evaluate(
        self,
        condition: MockCondition,
        context: ClinicalContext,
        severities: dict[str, int],
        worsening: set[str],
        evidence_by_id: dict[str, RetrievedDocument],
    ) -> DiagnosisCandidate | None:
        matched = {
            name
            for name in condition.any_symptoms
            if normalize_symptom_name(name) in severities
        }
        matched_keys = {normalize_symptom_name(name) for name in matched}

        complaint = normalize_symptom_name(context.current_visit.chief_complaint)
        complaint_hits = {
            term for term in condition.complaint_terms if term in complaint
        }

        if not matched_keys and not complaint_hits:
            return None

        score = condition.base_likelihood
        supporting: list[str] = []

        for key in sorted(matched_keys):
            severity = severities[key]
            score += BASE_SYMPTOM_WEIGHT * (severity / 10)
            supporting.append(f"{key} recorded at severity {severity}")

        if complaint_hits:
            score += COMPLAINT_WEIGHT
            supporting.append(
                f"presenting complaint mentions {', '.join(sorted(complaint_hits))}"
            )

        trend_matched = matched_keys & worsening if condition.trend_sensitive else set()
        if trend_matched:
            score += TREND_WEIGHT
            supporting.append(
                "worsening across visits: " + ", ".join(sorted(trend_matched))
            )

        contradicting: list[str] = []
        for name in sorted(condition.contradicting_symptoms):
            key = normalize_symptom_name(name)
            if key in severities:
                score -= CONTRADICTION_WEIGHT
                contradicting.append(f"{key} recorded at severity {severities[key]}")

        confidence = round(
            min(max(score, MIN_CONFIDENCE), MAX_CONFIDENCE), 4
        )

        # Citations are attached from what retrieval actually returned -- a
        # condition whose supporting documents were not retrieved gets none,
        # and the orchestrator drops it. The full retrieved record is kept
        # (not narrowed to the 3-field wire shape) so source metadata
        # survives; the orchestrator re-resolves it against its own
        # retrieved set regardless (AGENTS.md section 8.4.4).
        evidence = [
            evidence_by_id[document_id]
            for document_id in condition.document_ids
            if document_id in evidence_by_id
        ]
        if not evidence:
            return None

        if not supporting:
            supporting.append("recorded findings overlap with this presentation")

        trend_basis = trend_basis_refs(context.trends, trend_matched)
        is_early_watch = bool(trend_basis) and confidence < MODERATE_CONFIDENCE

        return DiagnosisCandidate(
            name=condition.name,
            category="early_watch" if is_early_watch else "differential_diagnosis",
            confidence=confidence,
            supporting_findings=supporting,
            contradicting_findings=contradicting,
            explanation=condition.explanation_template,
            trend_basis=trend_basis,
            evidence=evidence,
        )

    def _stage_finding(
        self,
        imaging: StagingResult,
        scan_trend: ScanTrend | None,
        evidence_by_id: dict[str, RetrievedDocument],
    ) -> DiagnosisCandidate | None:
        """Fold a staging estimate into the same cited candidate shape.

        The stage never gets its own field on the wire (ADR-006 decision 3):
        it is one more ``DiagnosisCandidate``, ranked and cited exactly like a
        symptom-derived one, so it can lose to a stronger symptom-based
        candidate or sit beside it in the differential.

        A worsening cross-visit imaging trend enriches this candidate's
        traceability (trend_basis) but never changes its category: staging
        confidence never dips low enough to qualify as early_watch, and
        decision 3 keeps the stage a differential candidate regardless.
        """

        condition = STAGE_CONDITIONS[imaging.stage]

        evidence = [
            evidence_by_id[document_id]
            for document_id in condition.document_ids
            if document_id in evidence_by_id
        ]
        if not evidence:
            return None

        supporting = [
            f"{region.region} contribution {region.contribution:.2f}"
            for region in imaging.contributing_regions
        ] or ["MRI-derived stage estimate"]

        trend_basis = stage_trend_basis_ref(scan_trend)
        if trend_basis:
            supporting.append(
                f"MRI-derived stage worsening across {scan_trend.visit_span} visits"
            )

        return DiagnosisCandidate(
            name=condition.name,
            category="differential_diagnosis",
            confidence=imaging.confidence,
            supporting_findings=supporting,
            contradicting_findings=[],
            explanation=condition.explanation_template,
            trend_basis=trend_basis,
            evidence=evidence,
        )

    # -- provider interface ----------------------------------------------

    def generate_analysis(self, request: ReasoningRequest) -> ReasoningResult:
        """Rank the condition rules against the supplied context and evidence."""

        context = request.context
        severities = self._observed_severities(context)
        worsening = worsening_symptom_names(context.trends)
        evidence_by_id = {
            document.document_id: document for document in request.evidence
        }

        candidates = [
            candidate
            for candidate in (
                self._evaluate(
                    condition, context, severities, worsening, evidence_by_id
                )
                for condition in self._conditions
            )
            if candidate is not None
        ]

        if request.imaging is not None:
            stage_finding = self._stage_finding(
                request.imaging, request.scan_trend, evidence_by_id
            )
            if stage_finding is not None:
                candidates.append(stage_finding)

        # Name as secondary key makes the ordering total, so ties are stable.
        candidates.sort(key=lambda candidate: (-candidate.confidence, candidate.name))

        return ReasoningResult(
            model_name=self.name,
            provider_mode="simulated",
            candidates=candidates[: request.max_candidates],
        )


__all__ = ["MockLLMClient"]
