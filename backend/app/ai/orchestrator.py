"""The AI pipeline (TRD section 8, APP-FLOW section 5).

    Clinical Case -> Normalize -> Build Clinical Context -> Retrieve Literature
    -> Rank Evidence -> Construct AI Context -> LLM Reasoning
    -> Validate Structured Output -> Persist / Return

This module owns everything from retrieval through validation. It is
provider-agnostic and database-free: it accepts a ``ClinicalContext`` and
returns a validated ``AnalysisResult``, touching no ``Session``. Persistence is
the service layer's job.

Every failure mode raises ``AIError`` (HTTP 502) with a distinguishing
``error_code``, and every failure happens before the caller writes anything --
which is how AGENTS.md section 8.5 is satisfied (ADR-003).
"""

from datetime import datetime, timezone

from pydantic import ValidationError

from app.ai.providers.base import EvidenceRetriever, LLMClient
from app.ai.ranking import cap_evidence_per_candidate, rank_candidates, rank_evidence
from app.schemas.analysis import (
    DISCLAIMER,
    SIMULATED_PIPELINE_NOTE,
    AnalysisResult,
    DiagnosisCandidate,
    ReasoningRequest,
    ReasoningResult,
)
from app.schemas.clinical_context import ClinicalContext
from app.schemas.evidence import RetrievalQuery, RetrievedDocument
from app.utils.exceptions import AIError


LIVE_PIPELINE_NOTE = "pipeline complete, evidence retrieved from live corpus"


class AnalysisOrchestrator:
    """Runs the pipeline for one clinical context."""

    def __init__(
        self,
        retriever: EvidenceRetriever,
        llm: LLMClient,
        *,
        max_candidates: int = 5,
        evidence_per_candidate: int = 3,
    ):
        self.retriever = retriever
        self.llm = llm
        self.max_candidates = max_candidates
        self.evidence_per_candidate = evidence_per_candidate

    # -- stages ----------------------------------------------------------

    def _build_query(self, context: ClinicalContext) -> RetrievalQuery:
        symptom_names = sorted(
            {
                symptom.symptom_name
                for visit in context.all_visits
                for symptom in visit.symptoms
            }
        )
        return RetrievalQuery(
            symptom_names=symptom_names,
            chief_complaint=context.current_visit.chief_complaint,
            max_results=min(
                self.max_candidates * self.evidence_per_candidate, 50
            ),
        )

    def _retrieve(self, context: ClinicalContext) -> list[RetrievedDocument]:
        try:
            documents = self.retriever.retrieve(self._build_query(context))
        except Exception as exc:  # provider failure, not a contract failure
            raise AIError(
                "Evidence retrieval is unavailable. The clinical record was "
                "not modified; the analysis can be retried.",
                error_code="rag_error",
            ) from exc

        if not documents:
            raise AIError(
                "No supporting literature was retrieved for this case, so no "
                "citable analysis could be produced. The clinical record was "
                "not modified.",
                error_code="rag_no_evidence",
            )

        return rank_evidence(documents)

    def _reason(
        self,
        context: ClinicalContext,
        evidence: list[RetrievedDocument],
    ) -> ReasoningResult:
        request = ReasoningRequest(
            context=context,
            evidence=evidence,
            max_candidates=self.max_candidates,
        )

        try:
            result = self.llm.generate_analysis(request)
        except ValidationError as exc:
            # The model produced output that violates the contract.
            raise AIError(
                "The analysis model returned output that does not satisfy the "
                "diagnosis contract. The clinical record was not modified.",
                error_code="ai_contract_error",
            ) from exc
        except Exception as exc:
            raise AIError(
                "The analysis model is unavailable. The clinical record was "
                "not modified; the analysis can be retried.",
                error_code="ai_error",
            ) from exc

        if not isinstance(result, ReasoningResult):
            raise AIError(
                "The analysis model returned an unrecognized result type.",
                error_code="ai_contract_error",
            )

        return result

    def _finalize(
        self,
        candidates: list[DiagnosisCandidate],
    ) -> list[DiagnosisCandidate]:
        """Drop uncited candidates, then rank and trim.

        A ranked condition without a citation is exactly the untraceable output
        AGENTS.md section 18 forbids, so it is removed rather than surfaced.
        """

        cited = [candidate for candidate in candidates if candidate.evidence]

        ranked = rank_candidates(cited, limit=self.max_candidates)
        return cap_evidence_per_candidate(
            ranked, limit=self.evidence_per_candidate
        )

    # -- pipeline --------------------------------------------------------

    def run(self, context: ClinicalContext) -> AnalysisResult:
        """Execute the pipeline and return validated, ranked output."""

        evidence = self._retrieve(context)
        reasoning = self._reason(context, evidence)
        candidates = self._finalize(list(reasoning.candidates))

        if not candidates:
            raise AIError(
                "No candidate condition could be supported by retrieved "
                "evidence for this case. The clinical record was not modified.",
                error_code="ai_no_candidates",
            )

        simulated = reasoning.provider_mode == "simulated"

        try:
            return AnalysisResult(
                visit_id=context.visit_id,
                patient_id=context.patient_id,
                model_name=reasoning.model_name,
                provider_mode=reasoning.provider_mode,
                # Section 8.1: mock-sourced output stays labelled as simulated.
                pipeline_note=(
                    SIMULATED_PIPELINE_NOTE if simulated else LIVE_PIPELINE_NOTE
                ),
                disclaimer=DISCLAIMER,
                generated_at=datetime.now(timezone.utc),
                candidates=candidates,
            )
        except ValidationError as exc:
            raise AIError(
                "The assembled analysis does not satisfy the output contract. "
                "The clinical record was not modified.",
                error_code="ai_contract_error",
            ) from exc


__all__ = ["LIVE_PIPELINE_NOTE", "AnalysisOrchestrator"]
