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

from app.ai.providers.base import EvidenceRetriever, ImagingStager, LLMClient
from app.ai.ranking import cap_evidence_per_candidate, rank_candidates, rank_evidence
from app.ai.trends import detect_stage_trend
from app.schemas.analysis import (
    DISCLAIMER,
    SIMULATED_PIPELINE_NOTE,
    AnalysisResult,
    DiagnosisCandidate,
    ReasoningRequest,
    ReasoningResult,
)
from app.schemas.clinical_context import ClinicalContext, ScanSummary, ScanTrend
from app.schemas.evidence import RetrievalQuery, RetrievedDocument
from app.schemas.imaging import STAGE_LABELS, StagingRequest, StagingResult
from app.utils.exceptions import AIError


LIVE_PIPELINE_NOTE = "pipeline complete, evidence retrieved from live corpus"

# AI-02 slice 1: live reasoning, still-simulated corpus. Naming this state is
# not cosmetic -- LIVE_PIPELINE_NOTE would claim evidence came from a live
# corpus when it came from mock_corpus, and section 8.1 requires mock-sourced
# output stay labelled as simulated (ADR-005).
HYBRID_PIPELINE_NOTE = (
    "pipeline complete, live model reasoning, evidence retrieval simulated"
)


class AnalysisOrchestrator:
    """Runs the pipeline for one clinical context."""

    def __init__(
        self,
        retriever: EvidenceRetriever,
        llm: LLMClient,
        stager: ImagingStager | None = None,
        *,
        max_candidates: int = 5,
        evidence_per_candidate: int = 3,
    ):
        self.retriever = retriever
        self.llm = llm
        self.stager = stager
        self.max_candidates = max_candidates
        self.evidence_per_candidate = evidence_per_candidate

    # -- stages ----------------------------------------------------------

    def _run_stager(self, scan: ScanSummary) -> StagingResult:
        request = StagingRequest(
            checksum=scan.checksum,
            content_type=scan.content_type,
            dimensions=scan.dimensions,
        )

        try:
            result = self.stager.stage(request)
        except Exception as exc:  # provider failure, not a contract failure
            raise AIError(
                "The imaging staging model is unavailable. The clinical "
                "record was not modified; the analysis can be retried.",
                error_code="staging_error",
            ) from exc

        if not isinstance(result, StagingResult):
            raise AIError(
                "The imaging staging provider returned an unrecognized "
                "result type.",
                error_code="staging_contract_error",
            )

        return result

    def _stage(
        self, context: ClinicalContext
    ) -> tuple[StagingResult | None, ScanTrend | None]:
        """Run imaging staging for the current visit, and a trend across it.

        Symptoms alone must still produce an analysis (ADR-006 decision 1), so
        a visit with no scan skips this stage entirely rather than failing.

        Every prior visit that also has a scan gets staged too, purely to
        feed ``detect_stage_trend`` (ADR-006 consequence: without this, the
        scan contributes nothing to trend-aware early detection). A prior
        visit's own persisted analysis, if any, is not reused -- staging is
        deterministic, so re-running it here costs nothing and keeps this
        module the only place that talks to the provider.
        """

        scan = context.current_visit.scan
        if scan is None:
            return None, None

        if self.stager is None:
            raise AIError(
                "An MRI scan is attached to this visit but no imaging "
                "staging provider is configured. The clinical record was "
                "not modified.",
                error_code="staging_error",
            )

        current_result = self._run_stager(scan)

        observations = [
            (visit.id, visit.visit_date, self._run_stager(visit.scan))
            for visit in context.prior_visits
            if visit.scan is not None
        ]
        observations.append(
            (context.current_visit.id, context.current_visit.visit_date, current_result)
        )

        return current_result, detect_stage_trend(observations)

    def _build_query(
        self,
        context: ClinicalContext,
        imaging: StagingResult | None,
    ) -> RetrievalQuery:
        symptom_names = sorted(
            {
                symptom.symptom_name
                for visit in context.all_visits
                for symptom in visit.symptoms
            }
        )
        # A stage estimate needs its own citations, resolved the same way a
        # symptom-derived candidate's are: by naming the condition and
        # letting retrieval find literature that matches it (ADR-006
        # decision 3 -- a stage is never surfaced without a citation).
        condition_names = [STAGE_LABELS[imaging.stage]] if imaging else []
        return RetrievalQuery(
            condition_names=condition_names,
            symptom_names=symptom_names,
            chief_complaint=context.current_visit.chief_complaint,
            max_results=min(
                self.max_candidates * self.evidence_per_candidate, 50
            ),
        )

    def _retrieve(
        self,
        context: ClinicalContext,
        imaging: StagingResult | None,
    ) -> list[RetrievedDocument]:
        try:
            documents = self.retriever.retrieve(
                self._build_query(context, imaging)
            )
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
        imaging: StagingResult | None,
        scan_trend: ScanTrend | None,
    ) -> ReasoningResult:
        request = ReasoningRequest(
            context=context,
            evidence=evidence,
            max_candidates=self.max_candidates,
            imaging=imaging,
            scan_trend=scan_trend,
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

    def _pipeline_note(
        self,
        provider_mode: str,
        imaging: StagingResult | None,
    ) -> str:
        """Describe what actually produced this analysis.

        Derived from every provider that ran rather than the reasoning model
        alone, because each is swapped independently: live reasoning over a
        simulated corpus is a real state, and it must not be described as
        live evidence (ADR-005). Provenance is now three-dimensional --
        retrieval, reasoning, and imaging staging (ADR-006 decision 4) -- so
        a scanned visit's note says so explicitly rather than only covering
        the two dimensions that predate MRI intake.
        """

        if provider_mode == "simulated":
            note = SIMULATED_PIPELINE_NOTE
        elif self.retriever.provenance == "simulated":
            note = HYBRID_PIPELINE_NOTE
        else:
            note = LIVE_PIPELINE_NOTE

        if imaging is not None:
            note += (
                ", imaging staging simulated"
                if imaging.provenance == "simulated"
                else ", imaging staging live"
            )

        return note

    # -- pipeline --------------------------------------------------------

    def run(self, context: ClinicalContext) -> AnalysisResult:
        """Execute the pipeline and return validated, ranked output."""

        imaging, scan_trend = self._stage(context)
        evidence = self._retrieve(context, imaging)
        reasoning = self._reason(context, evidence, imaging, scan_trend)
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
                # truth about retrieval (ADR-005).
                provider_mode=reasoning.provider_mode,
                # Section 8.1: mock-sourced output stays labelled as simulated.
                pipeline_note=self._pipeline_note(reasoning.provider_mode, imaging),
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
