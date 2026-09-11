# ADR-003: AI Analysis Contract and the Mocked-Provider Seam

## Status
Accepted. Extended by [ADR-004](ADR-004-live-llm-provider.md), which lands a live `LLMClient` behind this seam and revises the `pipeline_note` derivation described under *Consequences*.

## Context

`AI-01` is the fifth ticket on the locked roadmap (`docs/NEUROONE-MVP-SCOPE.md`), reached now that `CASE-01` has merged. Its scope is deliberately split by `AGENTS.md` §8.1: the AI orchestrator interface, the structured Diagnosis/Evidence output contract, validation of that contract, ranking, and citation attachment are **real and enforced now**; only the **retrieval corpus** and the **LLM call** are mocked. Those two sit behind the same interface the real providers will use, so `AI-02` is a provider swap rather than a pipeline rewrite.

That framing forces several decisions before any code exists. The output contract is a published surface that `REPORT-01` and the frontend will both consume, and `AGENTS.md` §17 requires a decision record before implementation for contract changes and AI/RAG interface changes. `AI-01` is both.

Three existing constraints shape everything below:

- **§8.2**: *"Never represent the output as a definitive diagnosis — not in the schema, not in API field naming."* Confidence is likelihood, never certainty.
- **§8.2**: `trend_basis` traces the patient's **own visit history**; `evidence[]` traces **external literature**. *"Do not conflate them."*
- **§8.5**: an AI or retrieval failure must preserve clinical data, return a controlled error, and never corrupt or partially overwrite a patient or case record.

## Problem

1. Where is the seam that `AI-02` replaces, and what exactly crosses it?
2. What is the persisted shape of an analysis, its ranked candidates, and their citations?
3. How does `trend_basis` reference the patient's own history?
4. How is a mocked provider "deterministic" in a way that is demonstrable rather than arbitrary?
5. How is §8.5 actually guaranteed, rather than merely attempted?

## Constraints

- The contract field names are fixed by `AGENTS.md` §8.2 and may not be renamed for convenience.
- The pipeline stages are fixed by TRD §8 / APP-FLOW §5 / `AGENTS.md` §8.
- Layering is fixed by `AGENTS.md` §7: API → Service → Repository → Model → Schema.
- Ownership/authorization must follow [ADR-002](ADR-002-visit-ownership-derivation.md); a foreign record must 404 without disclosing the parent.
- Mock output must simulate at least one multi-visit trend (§8.1) and stay labeled *"pipeline complete, evidence retrieval simulated."*

## Options Considered

**For the provider seam:** (a) a single `AIProvider` doing retrieval and reasoning together; (b) two narrow protocols, `EvidenceRetriever` and `LLMClient`; (c) no formal seam, with mock branching inside the orchestrator.

**For determinism:** (a) seeded RNG; (b) golden fixture files returning a canned result; (c) a pure rule-based function of the clinical context.

**For `trend_basis` storage:** (a) a join table with real foreign keys to `visits` and `symptoms`; (b) a JSON column holding the references.

**For evidence storage:** (a) reuse the existing report-scoped `Rag` stub; (b) a table scoped to each ranked finding; (c) a JSON column alongside the finding.

## Decision

**1. Two narrow protocols form the seam** — `EvidenceRetriever.retrieve(RetrievalQuery) -> list[RetrievedDocument]` and `LLMClient.generate_analysis(ReasoningRequest) -> ReasoningResult`, both in `backend/app/ai/providers/base.py`. Provider selection is a config setting (`AI_PROVIDER`, currently `Literal["mock"]`) resolved by `registry.build_providers()`.

`ReasoningResult.candidates` is `list[DiagnosisCandidate]` — the same model the API returns. A real LLM returning malformed output therefore fails validation **at the seam**, inside the orchestrator, and becomes a controlled `AIError`.

**2. `app/ai/` never imports a repository and never touches a `Session`.** It accepts a `ClinicalContext` and returns an `AnalysisResult`. The single exception is `context.py`, which reads attributes off already-loaded ORM instances — that *is* the "Normalize Input" stage. Everything downstream is database-free and therefore unit-testable without one.

**3. Determinism is a pure rule-based function of the clinical context** — no RNG, no canned results. Conditions carry matched symptoms, complaint terms, contradicting symptoms and a base likelihood; the score is arithmetic over what the clinician actually entered, clamped to a **maximum of 0.92**. Ordering is `(-confidence, name)`, making ties total and reproducible.

**4. `category` is decided by trend evidence, not by a confidence band**: a candidate is `early_watch` when one of its matched symptoms participates in a worsening multi-visit trend *and* its confidence is below the differential threshold. Because such a candidate takes its `trend_basis` from those very trend points, the invariant *`early_watch` ⇒ non-empty `trend_basis`* holds **by construction**. The schema validator is a second line of defence, not the only one.

**5. Three tables: `analyses`, `analysis_findings`, `analysis_evidence`.** Evidence is scoped to a **finding**, not to a report. The legacy `Diagnosis` and `Rag` stubs are deleted.

**6. `trend_basis` is a JSON column; evidence is a real table.**

**7. §8.5 is satisfied by ordering, not by exception handling.** Every read and every provider call happens before the first write:

```
1-3. get_visit / get_patient / get_patient_history   ← pure reads, and they authorize
4.   build_clinical_context(...)                     ← pure
5.   orchestrator.run(context)                       ← EVERY failure happens HERE
6.   repository.create_with_status(...)              ← ONE commit: analysis + findings
                                                       + evidence + visit.status=ANALYZED
```

**8. Field naming is constrained by the safety boundary.** The numeric is `confidence` (§8.2 sanctions "likelihood / confidence"); the persisted column is `condition_name` on a table called `analysis_findings`. The names `final_diagnosis`, `doctor_verified`, `probability`, `certainty`, and a bare `diagnosis` are **excluded by decision**, not by oversight.

## Why

**Two protocols rather than one** because retrieval and reasoning fail differently and are swapped independently — `AI-02` may land a real corpus before a real LLM, or vice versa. Splitting them also lets tests inject a failing retriever and a healthy LLM to exercise §8.5 precisely.

**Rule-based determinism** because the alternatives fail the demo, not just the tests. Seeded RNG is stable but arbitrary: it cannot make an `early_watch` point at a real trend, which is exactly the credibility risk §8.1 names. Golden fixtures do not respond to what the clinician typed, so ranking and validation would never actually execute and the demo would return the same answer regardless of input.

**`trend_basis` as JSON** because it is a *snapshot of reasoning*, not a live relation. Foreign keys would let a later severity edit silently rewrite what a past analysis said, which defeats the traceability §18 requires. It is never queried or filtered — only read whole — which is precisely the case `Visit.vitals` already established, using the same `.with_variant(JSON(), "sqlite")` idiom that keeps the table creatable under SQLite.

**Evidence as a table** because `AGENTS.md` §7 names **Evidence** as an initial domain entity, `REPORT-01` iterates it per finding, and each row carries stable metadata (`source_tier`, `published_year`, `document_id`, `chunk_id`) that §8.4.4 requires be preserved.

**Evidence scoped to a finding, not a report**, because §8.4.6 says attach citations *to recommendations*. A report-scoped bag of sources cannot say which condition a given citation supports, so the traceability chain §8.4 mandates — `patient finding + reasoning factor + supporting evidence + citation` — would be unrepresentable. `REPORT-01` reaches evidence via `report → analysis → finding → evidence` and needs no table of its own.

**Ordering rather than exception handling for §8.5** because it is the stronger guarantee. When every failure precedes the first write, there is nothing to roll back and no recovery path to get wrong. A `try/except` around a partially-completed write would satisfy the letter of §8.5 while leaving a window the ordering approach does not have.

## Consequences

- `AI-02` changes `app/ai/providers/` and widens the `AI_PROVIDER` literal. It does not touch the orchestrator, the schemas, the service, the API, or the database.
- **`evidence` is `min_length=1` on every candidate.** A ranked condition with no citation is exactly the untraceable output §18 forbids, so the orchestrator drops any candidate left with zero evidence and raises if none survive. A real LLM that returns an uncited condition will therefore fail validation — intended, and `AI-02` must expect it.
- **`DiagnosisCandidate` sets `extra="forbid"`.** A real LLM inventing a field is a contract failure, not a field to ignore.
- **The UUIDs inside `trend_basis` are soft references by design.** They are real `visits.id` / `symptoms.id` values, so traceability is a resolvable lookup, but nothing enforces referential integrity. A dangling id honestly means *"the underlying record changed since this analysis ran"* — that is information, not corruption, and it should not be filed as a bug.
- **Re-running analysis creates a new row.** There is no unique constraint on `visit_id`. Re-analysing after adding symptoms is the natural clinician action, and overwriting would destroy prior traceable output. `get_latest_for_visit` orders by `created_at DESC`.
- **A failed run persists nothing** — no `FAILED` rows, no status enum. Failure telemetry is logging (visit id only, never patient data, per §12).
- **The ownership gate runs three times per analysis** (`get_visit`, `get_patient`, `get_patient_history` each re-check). This is accepted deliberately: one uniform rule applied in one place is worth three small selects on a request that runs an entire pipeline. It is a decision, not an oversight.
- **`VisitStatus.ANALYZED` is written in exactly one place**, `AnalysisRepository.create_with_status`. The existing guard on `VisitService.update_visit` (and its test) is unaffected, because this path never calls it.
- `/diagnosis` and `/rag` are unmounted and their empty routers deleted. An OpenAPI tag literally named "diagnosis" is the framing §8.2 forbids, and `/rag` is an implementation detail rather than a public resource. `/reports` stays mounted for `REPORT-01`.

## Risks

- **A mocked pipeline returning schema-valid output will look real in a demo.** This is the credibility risk `NEUROONE-MVP-SCOPE.md` records. Mitigated in code by `provider_mode` and `pipeline_note` on every stored and returned analysis — but the mitigation is ultimately narrative, not technical, and how the demo is *described* matters as much as what it stores.
- **`SQLEnum` persists member names, not values.** A mismatch between the model and the migration fails at `INSERT` on PostgreSQL, and SQLite renders enums as `VARCHAR` + `CHECK`, so unit tests will not catch it. Verified once against real PostgreSQL.
- **Rule-based scoring is transparent, which cuts both ways.** Anyone reading `mock_corpus.py` can see exactly why a condition ranked where it did. That is good for review and bad for anyone tempted to present the output as model-derived.

## Alternatives Rejected

- **A single combined `AIProvider`** — couples two independently swappable concerns and makes retrieval-failure tests awkward.
- **Mock branching inside the orchestrator** (`if settings.AI_PROVIDER == "mock"`) — puts the thing `AI-02` must delete inside the thing `AI-02` must keep. The seam exists precisely so that does not happen.
- **Seeded RNG / golden fixtures** — see *Why*.
- **A `trend_basis` join table** — see *Why*.
- **Reusing the report-scoped `Rag` stub** — cannot attribute a citation to a specific recommendation, and `__tablename__ = "Rag"` is a capitalized quoted identifier that would be a permanent PostgreSQL papercut.
- **Persisting `FAILED` analysis rows** — adds an enum and a migration hazard to represent something logging already covers, and risks a failed run being read as clinical output.
- **A `likelihood_band` stored column** — it is derived from `confidence`, so it is exposed as a computed field instead. Storing it would allow the two to drift.

## Testing Impact

New suites: `test_analysis_schemas.py`, `test_ai_trends.py`, `test_ai_context.py`, `test_ai_mock_providers.py`, `test_ai_orchestrator.py`, `test_analysis_service.py`, `test_analysis_api.py`, `test_analysis_repository.py`. No existing test file is modified.

The four negative tests `AGENTS.md` §14 names are mandatory: valid output accepted; missing evidence rejected; malformed confidence rejected; `early_watch` without `trend_basis` rejected. A fifth is added deliberately — `differential_diagnosis` **with** a populated `trend_basis` is *accepted* — to pin the semantic so the validator is never "fixed" into an exclusive-or. `trend_basis` is a trace, not a category marker.

The §10 / TRD §12 AI category is covered end to end: structured-output validation, citation presence, traceability (every `early_watch`'s `trend_basis` resolves to a visit in the context and a symptom on that visit), malformed model output, missing evidence, AI failure, and RAG failure. Determinism is asserted directly: two identical runs produce byte-identical JSON. §8.5 is asserted by proving that when the orchestrator raises, the repository is never called and the visit status is unchanged.

Because `app/ai/` is database-free, the entire pipeline is tested without a database.

## Migration / Rollback Impact

One migration creates `analyses`, `analysis_findings`, and `analysis_evidence`, plus the `findingcategory` enum. It contains **no drops**: neither a `diagnoses` nor a `Rag` table was ever created by any migration, so the deleted stubs are dead Python, not live schema.

`downgrade()` drops the three tables in reverse dependency order and then drops the enum type explicitly — PostgreSQL retains an enum type after its table is dropped, so without that the next upgrade fails with "type already exists". This follows the pattern established in `a3c7be51d904`.

**Merge-order dependency:** this migration chains off `b8d41e2f7c53` (the `deleted_at` timezone fix, shipped in parallel). `AI-01` must not merge into any branch lacking that revision, or Alembic fails with "Can't locate revision". The test suite never runs Alembic, so tests are unaffected either way.

Rollback is clean: no existing table is altered and no existing row is touched.

## Addendum: evidence-resolution correction (pre-`REPORT-01`)

**Context.** Inspection ahead of `REPORT-01` found that `DiagnosisCandidate.evidence` was typed `list[EvidenceRef]` — the 3-field wire shape — and `mock_llm.py` narrowed each selected document to it with `EvidenceRef.model_validate(...)` before a candidate was even built. `document_id`, `chunk_id`, `source_tier`, `published_year`, and `relevance_score` were discarded at that point, before `AnalysisService` ever ran. `AnalysisEvidence` already carried nullable columns for all of them, so the loss was silent: nothing failed, the columns were simply always `NULL`. This violates §8.4.4 ("preserve source metadata") and would have made `REPORT-01`'s citation-level traceability requirement (FR-05/06, FR-07) impossible to satisfy without re-deriving evidence metadata from nothing.

**Decision.** `DiagnosisCandidate.evidence` is now typed `list[RetrievedDocument]` — the full retrieved record, not the narrowed wire shape. The orchestrator gains a `_resolve_evidence` stage, run after `_reason()` and before `_finalize()`: for every candidate, each evidence item's `document_id` is looked up against the orchestrator's own `_retrieve()` output, and the **retrieved copy replaces whatever the provider attached**. A `document_id` that does not resolve raises `AIError(error_code="ai_contract_error")`.

**Why re-resolve rather than trust the provider's copy.** A provider (mock today, a real LLM under `AI-02`) is only trusted to *select* evidence by id; it is not the source of truth for that evidence's content. Re-resolving against the retrieved set means a future real LLM cannot alter or fabricate citation metadata even if it echoes a document back with different field values — only `document_id` is load-bearing. This is a direct extension of the existing "reject an uncited candidate" rule in §18: an evidence reference to a document retrieval never returned is exactly the same class of untraceable output.

**Consequences.**
- `EvidenceResponse` gains `document_id`, `chunk_id`, and `relevance_score` (additive; `source_url`/`source_tier`/`published_year` were already present).
- `AnalysisService._to_finding` now copies every `RetrievedDocument` field into `AnalysisEvidence`, populating the columns that already existed but were previously always `NULL`.
- No migration is required for this addendum — the `analysis_evidence` columns were already nullable and already present.
- `AI-02` inherits `_resolve_evidence` unchanged: a real `LLMClient` must still name evidence by `document_id` from what `EvidenceRetriever.retrieve()` actually returned, which is a stronger, not weaker, constraint than before.
