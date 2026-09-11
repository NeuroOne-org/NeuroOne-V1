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

# AI-02 slice 1: live reasoning, still-simulated corpus. Naming this state is
# not cosmetic -- LIVE_PIPELINE_NOTE would claim evidence came from a live
# corpus when it came from mock_corpus, and section 8.1 requires mock-sourced
# output stay labelled as simulated (ADR-004).
HYBRID_PIPELINE_NOTE = (
    "pipeline complete, live model reasoning, evidence retrieval simulated"
)


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

    def _resolve_evidence(
        self,
        candidates: list[DiagnosisCandidate],
        retrieved: list[RetrievedDocument],
    ) -> list[DiagnosisCandidate]:
        """Re-attach evidence from the orchestrator's own retrieved set.

        A provider names its evidence by ``document_id``; the orchestrator,
        not the provider, is the source of truth for what that id actually
        contains (AGENTS.md section 8.4.4: source metadata must be
        preserved, not merely echoed back). This also rejects a document_id
        the provider invented rather than selected from what retrieval
        actually returned -- exactly the untraceable output section 18
        forbids.
        """

        retrieved_by_id = {
            document.document_id: document for document in retrieved
        }

        resolved = []
        for candidate in candidates:
            try:
                evidence = [
                    retrieved_by_id[item.document_id]
                    for item in candidate.evidence
                ]
            except KeyError as exc:
                raise AIError(
                    "The analysis model cited evidence that was not "
                    "retrieved for this case. The clinical record was not "
                    "modified.",
                    error_code="ai_contract_error",
                ) from exc
            resolved.append(candidate.model_copy(update={"evidence": evidence}))
        return resolved

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

    def _pipeline_note(self, provider_mode: str) -> str:
        """Describe what actually produced this analysis.

        Derived from both providers rather than the model alone, because the
        two are swapped independently: live reasoning over a simulated corpus
        is a real state, and it must not be described as live evidence
        (ADR-004).
        """

        if provider_mode == "simulated":
            return SIMULATED_PIPELINE_NOTE
        if self.retriever.provenance == "simulated":
            return HYBRID_PIPELINE_NOTE
        return LIVE_PIPELINE_NOTE

    # -- pipeline --------------------------------------------------------

    def run(self, context: ClinicalContext) -> AnalysisResult:
        """Execute the pipeline and return validated, ranked output."""

        evidence = self._retrieve(context)
        reasoning = self._reason(context, evidence)
        resolved = self._resolve_evidence(list(reasoning.candidates), evidence)
        candidates = self._finalize(resolved)

        if not candidates:
            raise AIError(
                "No candidate condition could be supported by retrieved "
                "evidence for this case. The clinical record was not modified.",
                error_code="ai_no_candidates",
            )

        try:
            return AnalysisResult(
                visit_id=context.visit_id,
                patient_id=context.patient_id,
                model_name=reasoning.model_name,
                # Describes the reasoning provider, which is where it has
                # always been sourced from; pipeline_note carries the fuller
                # truth about retrieval (ADR-004).
                provider_mode=reasoning.provider_mode,
                # Section 8.1: mock-sourced output stays labelled as simulated.
                pipeline_note=self._pipeline_note(reasoning.provider_mode),
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


__all__ = [
    "HYBRID_PIPELINE_NOTE",
    "LIVE_PIPELINE_NOTE",
    "AnalysisOrchestrator",
]
