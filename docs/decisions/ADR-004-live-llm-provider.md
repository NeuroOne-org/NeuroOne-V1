# ADR-004: Live LLM Provider Behind the AI-01 Seam

## Status
Accepted

## Context

`AI-02` is the final item on the locked roadmap (`docs/NEUROONE-MVP-SCOPE.md`): *"real LLM + RAG swap-in behind the AI-01 interface (post-demo)."* `REPORT-01` has merged, so the PRD §8 acceptance journey is demoable end to end and this is next in sequence.

`AGENTS.md` §19 classifies real LLM/RAG providers as **deferred, not excluded**, and requires the request be treated as a scope decision rather than a feature request. That decision was taken deliberately and is recorded here.

**Scope decided: the LLM only.** `EvidenceRetriever` stays mocked. Real retrieval is a separate later slice.

[ADR-003](ADR-003-ai-analysis-contract-and-provider-seam.md) built the seam for exactly this: two narrow protocols in `app/ai/providers/base.py`, a single selection point in `registry.build_providers()`, `provider_mode` already admitting `"live"`, and `_resolve_evidence()` already rejecting a `document_id` a provider invented. ADR-003 §Consequences predicted `AI-02` would change `app/ai/providers/` and widen `AI_PROVIDER` and *"not touch the orchestrator, the schemas, the service, the API, or the database."* That prediction holds for the schemas, the service, the API and the database. It does **not** hold for the orchestrator, for one reason developed under *Problem 4* below.

The reason this ADR is required rather than optional: §17 mandates a decision record for **AI/RAG interface changes** and **new dependencies**. This is both.

## Problem

1. Which provider, and how is the choice kept from hardening into the code?
2. A live model is untrusted output. `DiagnosisCandidate` sets `extra="forbid"`, `evidence` is `min_length=1`, confidence clamps at `MAX_CONFIDENCE = 0.92`, and `early_watch` without `trend_basis` raises. A real model violates each of these routinely. Which violations should fail the run, and which should be absorbed?
3. `TrendBasisRef` carries real `visits.id` / `symptoms.id` values. How is a model prevented from *fabricating* one?
4. With a live LLM and a mocked retriever, what is the output honestly called?
5. Patient-shaped data now leaves the machine. Under what conditions is that acceptable?

## Constraints

- The contract field names are fixed by `AGENTS.md` §8.2 and may not be renamed. Confidence is likelihood, never certainty.
- §8.1: mock-sourced output must stay labelled *"pipeline complete, evidence retrieval simulated."*
- §8.4.4: source metadata must be preserved end to end, not echoed back by a provider.
- §8.5: an AI or retrieval failure must preserve clinical data and return a controlled error.
- §12: never put sensitive patient data in logs; never commit secrets.
- §12 records synthetic demo data as an **assumption awaiting confirmation**, not settled policy.
- ADR-003's invariant *`early_watch` ⇒ non-empty `trend_basis`* must keep holding **by construction**, not by validator alone.

## Options Considered

**For the provider:** (a) the Anthropic SDK; (b) the OpenAI SDK; (c) a vendor-specific free-tier SDK (Google `google-genai`); (d) a thin OpenAI-compatible `/chat/completions` client over `httpx`, with base URL and model as configuration.

**For containing model output:** (a) hand the model `DiagnosisCandidate.model_json_schema()` and validate the result directly; (b) a narrow intermediate payload schema that the provider maps into `DiagnosisCandidate`; (c) accept free-form JSON and coerce field by field.

**For `trend_basis`:** (a) let the model emit `TrendBasisRef` objects including UUIDs; (b) let the model reference trends by symptom name and have the provider resolve names to real trend points.

**For the hybrid label:** (a) leave `pipeline_note` deriving from the LLM alone; (b) derive it from both providers and add a third note; (c) widen `provider_mode` to a third `"hybrid"` member.

## Decision

**1. A thin OpenAI-compatible client, with the provider as configuration** — option (d). `AI_LLM_BASE_URL` + `AI_LLM_MODEL` + `AI_LLM_API_KEY` select the provider; no vendor SDK is added. Groq's free tier is the default base URL. Gemini's OpenAI-compatible endpoint, OpenRouter, a paid OpenAI key, or a local Ollama are all reachable by changing `.env`, with no code branch per vendor.

The only new dependency is `httpx==0.28.1`, promoted from `requirements-dev.txt` to `requirements.txt` at the same pin.

**2. A narrow intermediate payload schema, not `DiagnosisCandidate` directly** — option (b). `LiveCandidatePayload` carries only what a model should author:

```text
name, category, confidence, supporting_findings,
contradicting_findings, explanation,
evidence_document_ids: list[str]    # ids, selected from the supplied list
trend_symptom_names: list[str]      # names, never UUIDs
```

`LiveLLMClient` maps payloads into `DiagnosisCandidate`. The model is never handed `DiagnosisCandidate`'s own schema.

**3. The hard/soft failure line.** **Structural violations fail hard; per-candidate content violations are normalized or dropped.**

| Model output | Treatment |
|---|---|
| Unparseable JSON, or a response object missing `candidates` | raise ⇒ `AIError(ai_contract_error)` |
| An invented field on the payload (`extra="forbid"`) | raise ⇒ `AIError(ai_contract_error)` |
| A `document_id` not in the supplied evidence | drop that id |
| A candidate left with zero resolved evidence | skip that candidate |
| `confidence` above `MAX_CONFIDENCE` | clamp to 0.92 |
| `early_watch` with no resolvable trend | downgrade to `differential_diagnosis` |
| A candidate that fails `DiagnosisCandidate` validation | skip that candidate |
| Every candidate skipped | the orchestrator's existing `ai_no_candidates` |

**4. `trend_basis` UUIDs are system-authored** — option (b). The model names worsening symptoms; `LiveLLMClient` resolves those names through `normalize_symptom_name` against `context.trends` and builds refs from real `TrendPoint` rows. The shared builder is extracted to `app/ai/trends.trend_basis_refs()` and used by both the mock and live providers, so there is one implementation of this logic rather than two.

**5. `pipeline_note` derives from both providers** — option (b). A third constant is added to the orchestrator:

```python
HYBRID_PIPELINE_NOTE = "pipeline complete, live model reasoning, evidence retrieval simulated"
```

Selection reads `self.retriever.provenance` alongside `reasoning.provider_mode`: both simulated ⇒ `SIMULATED_PIPELINE_NOTE`; live reasoning + simulated retrieval ⇒ `HYBRID_PIPELINE_NOTE`; both live ⇒ `LIVE_PIPELINE_NOTE`.

**6. `provider_mode` is not widened.** It stays `Literal["simulated", "live"]` and continues to describe the **reasoning** provider, which is what it has always been sourced from (`ReasoningResult.provider_mode`). `pipeline_note` carries the fuller truth. Option (c) was rejected — see *Alternatives Rejected*.

**7. `AI_PROVIDER` defaults to `mock`.** Live reasoning is opt-in per environment. `build_providers()` raises a configuration error if `live-llm` is selected without an API key, so the failure lands at startup rather than mid-request on a clinician's screen.

## Why

**Configuration over an SDK** because the wire format is the commodity here. Groq, OpenRouter, Gemini's compatibility endpoint, Together, Ollama and OpenAI all speak the same `/chat/completions` shape, so one ~50-line client covers every provider this project is plausibly going to try — including a free one today and a paid one later — without a second code path. A vendor SDK would buy typed errors and retry helpers at the cost of pinning the project to one vendor's release cadence, in a repository that pins every dependency exactly. The free tier matters for a student project with no budget, and the base URL being config means outgrowing the free tier is an `.env` edit, not a refactor.

**A narrow payload schema** because handing a model `DiagnosisCandidate.model_json_schema()` would be actively harmful, not merely redundant. That model has `extra="forbid"` *and* a `likelihood_band` computed field: the computed field appears in the serialization schema, a model shown that schema will dutifully echo `likelihood_band` back, and `extra="forbid"` then rejects the response. The strictness ADR-003 chose deliberately would become a self-inflicted failure on every single call. Separating what the model authors from what the system assembles avoids that entirely, and keeps `evidence` as `list[RetrievedDocument]` — which a model could never populate faithfully anyway, because §8.4.4 forbids trusting it to.

**The hard/soft line follows the traceability rule, not convenience.** ADR-003 §Consequences is explicit that an invented field is *"a contract failure, not a field to ignore"* — so structural malformation still fails hard, unchanged. But the same ADR also warns `AI-02` *"must expect"* uncited-condition validation failures. Those are different in kind: a malformed envelope means the provider is broken, while one over-confident or uncited candidate among five means the model was imprecise about one row. Dropping that row degrades the answer; raising on it destroys an otherwise-good analysis and, because §8.5 orders every failure before the first write, costs the clinician the whole run. Dropping is also not lenient in the way it looks: a dropped candidate cannot reach the database, and a citation that does not resolve is discarded rather than persisted, which is exactly the §18 outcome.

**Symptom names rather than UUIDs** because this is the one place a hallucination would be indistinguishable from a legitimate record. ADR-003 §Consequences accepts dangling `trend_basis` ids on the reasoning that *"a dangling id honestly means the underlying record changed since this analysis ran — that is information, not corruption."* That reasoning holds precisely because the only writer of those ids was the system. A model that authors UUIDs breaks the premise: a fabricated id would be indistinguishable from a stale one, and the §18 traceability chain would silently become unfalsifiable. Never letting the model near a UUID preserves the existing interpretation of a dangling reference. It is the same principle as `_resolve_evidence`, applied to the other half of the traceability chain — **a provider selects, the system resolves.**

**Deriving the note from both providers** because the alternative ships a false statement. `LIVE_PIPELINE_NOTE` reads *"evidence retrieved from live corpus."* With a live LLM and a mocked retriever, `reasoning.provider_mode == "live"`, so the current expression stamps that sentence onto an analysis whose evidence came from `mock_corpus.py`. That is not a cosmetic defect: §8.1 requires mock-sourced output stay labelled as simulated, and `NEUROONE-MVP-SCOPE.md` names a mocked pipeline that *looks* real as the project's principal credibility risk — a risk it explicitly says is mitigated by `provider_mode` and `pipeline_note`. Leaving the expression alone would disable the one technical mitigation on record at the exact moment it starts mattering. That is why ADR-003's prediction about not touching the orchestrator is knowingly broken here: honest labelling outranks a prediction about file scope, the change is four lines, and it removes a lie rather than adding a feature. `EvidenceRetriever` already declares `provenance`, so no protocol changes.

## Consequences

- **Clinical context leaves the machine.** A live call sends the patient's visit history, symptoms and clinician free text to a third-party API. §12 records synthetic demo data as an *unconfirmed assumption*, so this is acceptable **only** under that assumption. `AI_PROVIDER` defaults to `mock`; pointing `live-llm` at real patient data is a PLAN-mode decision requiring the security review §12 names, and is not authorized by this ADR. Free tiers in particular may retain or train on submitted data — a consideration that does not apply to the mock provider at all.
- **A prompt-injection surface opens.** Clinician-entered free text (`chief_complaint`, `history`, `notes`, `observation`) now reaches a model prompt. The structural mitigations are the ones already in place for other reasons: output is schema-validated at the seam, evidence is re-resolved against the retrieved set, and UUIDs are system-authored — so the worst realistic outcome is a degraded or dropped candidate, not a fabricated citation or a rewritten record. This gets materially worse when real retrieval lands: retrieved passages are *also* untrusted text, and a corpus document is a far more attractive injection vector than a symptom field. That is a problem for the RAG slice, and it should not be deferred quietly.
- **No prompt or response body may be logged.** Both contain patient data (§12). Logging is restricted to model name, latency, HTTP status, `visit_id` and candidate count.
- **Output stops being deterministic when `live-llm` is selected.** ADR-003 chose rule-based mock scoring specifically so two identical runs produce byte-identical JSON, and the existing determinism test asserts it. That test covers the mock provider and continues to pass; no equivalent guarantee exists or can exist for the live path, and re-running an analysis will legitimately produce different candidates. `get_latest_for_visit` ordering by `created_at DESC` already accommodates this.
- **The mock provider is not deprecated.** It remains the default, keeps the test suite network-free and deterministic, and is what the demo runs on unless deliberately switched. This slice adds a path; it does not replace one.
- **`app/ai/` stays database-free.** `LiveLLMClient` touches no `Session` and imports no repository, so the pipeline remains unit-testable without a database (ADR-003 §2).
- **`trends.py` gains an import from `app.schemas.analysis`** for `TrendBasisRef`. No cycle: `analysis.py` does not import `trends.py`.
- **Rate limits are now a runtime failure mode.** A free tier returns 429 under load. One bounded retry absorbs a transient limit; a persistent one surfaces as `AIError(ai_error)`, which §8.5 already guarantees leaves the clinical record untouched and the analysis retryable.

## Risks

- **A live model makes the credibility risk worse, not better.** Mock output was at least transparently rule-based — `NEUROONE-MVP-SCOPE.md` notes that anyone reading `mock_corpus.py` can see why a condition ranked where it did. Live reasoning over a *simulated* corpus is the hardest state to describe honestly: the reasoning is real, the evidence is not. `HYBRID_PIPELINE_NOTE` says so on every stored and returned analysis, but as ADR-003 already observed, the mitigation is ultimately narrative. How the demo is described still matters more than what it stores.
- **A model can produce clinically plausible, clinically wrong output** with fluent supporting findings attached to real citations. The safety boundary (§2.1) — decision support, ranked possibilities, clinician-owned interpretation — is what contains this, and it is unchanged. But the failure mode is now persuasive prose rather than a visibly arbitrary score.
- **Provider JSON-mode support varies.** `response_format: {"type": "json_object"}` is widely but not uniformly honoured across OpenAI-compatible endpoints. A provider that ignores it returns prose, which fails parsing and surfaces as `ai_contract_error` — a controlled failure, but one that makes the endpoint unusable rather than degraded. Verify JSON mode when changing `AI_LLM_BASE_URL`.
- **An API key is now a secret in `backend/.env`.** §12 forbids committing it. `.env.example` carries a placeholder only.
- **Free-tier models are weaker at instruction-following** than frontier models, so dropped candidates will be more common on the default configuration than on a paid one. This degrades output quality without weakening any guarantee — every containment rule above holds regardless of model strength.

## Alternatives Rejected

- **A vendor SDK (Anthropic, OpenAI, `google-genai`)** — pins the project to one vendor and adds a dependency tree to a repository that pins exact versions, to replace a client small enough to read in one screen. The compatibility endpoint is the portable choice.
- **Handing the model `DiagnosisCandidate`'s own JSON schema** — the `likelihood_band` computed field plus `extra="forbid"` makes this fail on essentially every call. See *Why*.
- **Letting the model emit `TrendBasisRef` UUIDs** — makes fabrication indistinguishable from staleness and breaks the premise ADR-003 relied on to accept soft references.
- **Widening `provider_mode` to `"hybrid"`** — it is persisted on `analyses.provider_mode` and exposed on `AnalysisResponse`, so a third member means a migration, a wire-contract change for the frontend and `REPORT-01`, and a new state every existing consumer must learn. `pipeline_note` is already a free-text field carried on every analysis for exactly this purpose, and it conveys the same information without a schema change.
- **Raising on any per-candidate defect** — one imprecise row would destroy an otherwise-usable analysis, and because §8.5 orders every failure before the first write, the clinician loses the whole run rather than one candidate.
- **Catching exceptions inside `LiveLLMClient`** — the orchestrator already maps provider exceptions to the correct `AIError` codes (`orchestrator.py` `_reason`). Handling them twice would either swallow a distinction the error codes depend on or duplicate the mapping.
- **Swapping the retriever in the same slice** — real retrieval needs a corpus, an index, a chunking decision and a trust-tier policy for sources, which is a larger scope decision than this one and carries the injection exposure noted above. Splitting the swap is what the two-protocol seam was designed to allow (ADR-003 §Why).

## Testing Impact

New suite: `backend/tests/test_ai_live_llm.py`. No existing test file changes behaviour, and the suite stays network-free — there is no prior HTTP-mocking convention in this repository, so `httpx.MockTransport` is introduced, injected through the constructor's optional `client` parameter.

Covered: a well-formed response maps correctly; a hallucinated `document_id` is dropped; a candidate left uncited is skipped; `trend_basis` refs resolve to real context ids and a model-supplied UUID never appears; confidence above 0.92 is clamped; `early_watch` with no resolvable trend is downgraded rather than raised; an invented payload field and malformed JSON both become `ai_contract_error`; a transport failure becomes `ai_error`; `HYBRID_PIPELINE_NOTE` is stamped when reasoning is live and retrieval is simulated; `build_providers()` returns the live pair when configured and raises without a key.

`test_ai_mock_providers.py` is the regression gate for the `trend_basis_refs` extraction — it must pass unchanged, including its determinism assertion.

## Migration / Rollback Impact

**No migration.** No table, column or enum changes: `provider_mode` is not widened and `pipeline_note` is already a free-text column populated on every analysis.

Rollback is a configuration change. Setting `AI_PROVIDER=mock` restores the previous behaviour completely, with no data to reverse — prior analyses keep the `pipeline_note` they were stored with, which is the correct historical record of how each one was produced.

The only irreversible artifact is external: prompts already sent to a third-party provider cannot be recalled. This is the operative reason `AI_PROVIDER` defaults to `mock` and why enabling it against real patient data requires sign-off rather than a config edit.
