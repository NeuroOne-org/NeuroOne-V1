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
    TREND_WEIGHT,
    MockCondition,
)
from app.ai.trends import normalize_symptom_name, worsening_symptom_names
from app.schemas.analysis import (
    MAX_CONFIDENCE,
    MODERATE_CONFIDENCE,
    DiagnosisCandidate,
    ReasoningRequest,
    ReasoningResult,
    TrendBasisRef,
)
from app.schemas.clinical_context import ClinicalContext, SymptomTrend
from app.schemas.evidence import EvidenceRef, RetrievedDocument


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

    def _trend_refs(
        self,
        trends: list[SymptomTrend],
        matched: set[str],
    ) -> list[TrendBasisRef]:
        """Build history references for the matched worsening symptoms.

        Every reference points at a real visit and symptom row, which is what
        makes an early_watch flag traceable (AGENTS.md section 8.2).
        """

        refs: list[TrendBasisRef] = []
        for trend in trends:
            if trend.direction != "worsening" or trend.symptom_name not in matched:
                continue

            observation = (
                f"{trend.symptom_name} severity {trend.first_severity} -> "
                f"{trend.latest_severity} across {trend.visit_span} visits"
            )
            for point in trend.points:
                refs.append(
                    TrendBasisRef(
                        visit_id=point.visit_id,
                        symptom_id=point.symptom_id,
                        symptom_name=trend.symptom_name,
                        visit_date=point.visit_date,
                        severity=point.severity,
                        observation=observation,
                    )
                )
        return refs

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
        # and the orchestrator drops it.
        evidence = [
            EvidenceRef.model_validate(evidence_by_id[document_id])
            for document_id in condition.document_ids
            if document_id in evidence_by_id
        ]
        if not evidence:
            return None

        if not supporting:
            supporting.append("recorded findings overlap with this presentation")

        trend_basis = self._trend_refs(context.trends, trend_matched)
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

        # Name as secondary key makes the ordering total, so ties are stable.
        candidates.sort(key=lambda candidate: (-candidate.confidence, candidate.name))

        return ReasoningResult(
            model_name=self.name,
            provider_mode="simulated",
            candidates=candidates[: request.max_candidates],
        )


__all__ = ["MockLLMClient"]
