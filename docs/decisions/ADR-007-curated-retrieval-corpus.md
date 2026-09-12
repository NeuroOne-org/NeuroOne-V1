# ADR-007: Curated Retrieval Corpus Behind the AI-01 Seam

## Status
Proposed

## Context

`AI-02b` is the last open item on the roadmap (`AGENTS.md` §15, `docs/NEUROONE-MVP-SCOPE.md`): *"real RAG corpus behind the same interface."* `AI-02a` ([ADR-005](ADR-005-live-llm-provider.md)) swapped the reasoning provider and left `EvidenceRetriever` mocked, deferring retrieval until three things were decided: a trusted-literature corpus, an index, and a source-tier policy. `AGENTS.md` §19 requires that request be taken as a scope decision. It was, and the three decisions are recorded here.

**Decided with the project owner (2026-09-13):**

| Question | Decision |
|---|---|
| Corpus source | **Curated local set**, in a file format a later PubMed refresh can feed (option A, built to grow into C) |
| Index | **Postgres full-text search** (`tsvector` + GIN), no new infrastructure |
| Source-tier policy | **Guidelines and systematic reviews only** |

[ADR-003](ADR-003-ai-analysis-contract-and-provider-seam.md) built the seam this uses: `EvidenceRetriever.retrieve(RetrievalQuery) -> list[RetrievedDocument]`, `provenance` on the protocol, one selection point in `registry.build_providers()`, and `_resolve_evidence()` re-resolving every citation against what retrieval actually returned. ADR-005 already derives `pipeline_note` from both providers and defines `LIVE_PIPELINE_NOTE` for the live/live state.

§17 requires this record: it is an **AI/RAG interface change** and a **schema addition**.

## Problem

1. Where do corpus documents live, and in what form does a human-curated set enter the system, such that an automated PubMed fetch can later produce the same form without a rewrite?
2. `app/ai/` is database-free by design (ADR-003 §2, ADR-005 Consequences). A Postgres full-text retriever needs a database. How does it get one without breaking that?
3. The test suite runs on in-memory SQLite (`tests/conftest.py`) and CI has no Postgres service (`.github/workflows/backend-tests.yml`). Postgres full-text search cannot be exercised by either. How is the retriever's SQL tested?
4. `MockLLMClient` cites fixture `document_id`s only (`MockCondition.document_ids`). Mock reasoning over a real corpus yields zero cited candidates, and `_pipeline_note()` would stamp *"evidence retrieval simulated"* on evidence that was not simulated. What happens to that combination?
5. A retrieved passage is untrusted text entering a model prompt. ADR-005 flagged this as *"a problem for the RAG slice, and it should not be deferred quietly."* What contains it?
6. How is "guidelines and systematic reviews only" enforced so it cannot be bypassed by one mis-tagged file?

## Constraints

- §8.2 contract field names are fixed. `RetrievedDocument`, `EvidenceRef` and `RetrievalQuery` do not change shape.
- §8.4: retrieve, rank, preserve source metadata, supply to the model, attach citations. Trusted sources prioritized.
- §8.1: the label must match the provenance state in force. Mock-sourced output stays labelled simulated.
- §8.5: a retrieval failure preserves clinical data and returns a controlled error. `rag_error` and `rag_no_evidence` already exist in the orchestrator.
- §12: no patient data in logs; no secrets committed. No new outbound call is introduced by this slice.
- ADR-006 decision 3: a stage estimate is never surfaced without a citation, so the corpus must cover every `STAGE_LABELS` value.
- Every dependency is pinned exactly. PyYAML 6.0.3 is already pinned; nothing new is needed.
- Passages must be **quoted from real sources** by a human reviewer. They are not authored by an agent; the mock corpus was written for its fixture and is the thing being replaced.

## Options Considered

**Corpus source:** (A) curated local set; (B) live PubMed E-utilities at analysis time; (C) curated set refreshed by a PubMed script. Compared with the owner; A chosen, with C's growth path designed in.

**Index:** (a) Postgres FTS; (b) pgvector embeddings; (c) hybrid FTS + vectors.

**Where the corpus is authored:** (a) rows inserted by SQL seed; (b) Python fixtures like `mock_corpus.py`; (c) versioned YAML source files, one per source document, validated and loaded by a CLI.

**Database access from the retriever:** (a) retriever imports `SessionLocal` directly; (b) orchestrator passes the request session through `RetrievalQuery`; (c) the retriever depends on a narrow `CorpusSearch` protocol, implemented outside `app/ai/` by a repository plus a session-factory adapter.

**Testing the SQL:** (a) SQLite FTS5 as a test stand-in; (b) mock the repository everywhere; (c) pure logic tested on the existing suite, SQL tested by a Postgres-marked suite that CI runs against a Postgres service.

**Mock reasoning + corpus retrieval:** (a) generalize `MockLLMClient` to cite any retrieved document; (b) add a fourth `pipeline_note`; (c) refuse the combination at configuration time.

## Decision

**1. Corpus source files are the contract.** Each source document is one YAML file under `backend/corpus/documents/`, listed in `backend/corpus/manifest.yaml`, which carries `corpus_version`. A file holds the document's metadata (`document_id`, `source`, `citation`, `source_url`, `source_tier`, `published_year`, `license`, `keywords`, `reviewed_by`, `reviewed_at`) and one or more `passages` (`chunk_id`, `text`). A Pydantic schema with `extra="forbid"` validates every file.

Only `documents/` is loadable. `backend/corpus/pending/` is where a future PubMed fetcher writes candidates; the loader refuses it. **A human moving a file from `pending/` to `documents/` and filling `reviewed_by` is the review gate**, and it is the same gate whether the file was typed by hand today or fetched by a script later. That is the whole of the A-to-C growth path.

**2. Storage: one `corpus_documents` table, one row per passage.** Unique on `(document_id, chunk_id)`; `corpus_version`, `license`, `content_sha256`, `reviewed_by`, `reviewed_at` and `is_active` alongside the `RetrievedDocument` fields. A **generated** `search_vector tsvector` column weights keywords (A), citation (B) and passage (C) under the `english` configuration, with a GIN index. `search_vector` exists in the migration only and is excluded from Alembic autogenerate, so SQLite never sees a Postgres type. Chunking is curatorial, not automatic: a reviewer selects the passage.

**3. Tier policy is enforced in three places.** The source-file schema rejects any tier other than `guideline` or `systematic_review`; the table carries a `CHECK` constraint with the same set; the retriever filters again before returning. `SourceTier` on `RetrievedDocument` keeps all four members, because the mock corpus and persisted analyses use them.

**4. Licence allow-list at ingestion.** `CC0-1.0`, `CC-BY-4.0`, `public-domain`. Non-commercial licences are excluded by default, since passages appear in clinician views and PDF reports of a product being shown to investors. Widening the list is a one-line change and a recorded decision, not a silent edit.

**5. The retriever stays database-free; the search does not.** `CorpusEvidenceRetriever` (`app/ai/providers/corpus_retriever.py`, `provenance = "live"`) depends on a `CorpusSearch` protocol declared in `app/ai/providers/base.py`. The implementation is `CorpusRepository` (`app/repositories/`) behind a small adapter that opens a short-lived session from `SessionLocal`. `app/api/dependencies.py`, which already builds providers once at import, constructs the adapter and passes it to `build_providers()`. The retriever owns query shaping, tier re-filtering, score normalization and determinism; the repository owns SQL.

**6. Ranking mirrors the mock's weights.** Relevance is `0.5·rank(conditions) + 0.3·rank(symptoms) + 0.2·rank(complaint terms)` using `ts_rank_cd`, plus the existing tier bonus, normalized by the top score into `[0, 1]`, ordered by score then `document_id`, `chunk_id`. Every query term is a **bound parameter** passed through `plainto_tsquery`, OR-combined in SQL. No clinician text is ever concatenated into SQL or parsed as tsquery syntax.

**7. A new setting, and one refused combination.** `AI_RETRIEVAL_PROVIDER: Literal["mock", "corpus"] = "mock"`, a separate seam in the same way `AI_STAGING_PROVIDER` is (ADR-006 decision 4). `build_providers()` raises a configuration error for:

- `corpus` with `AI_PROVIDER=mock`: the mock reasoner cannot cite real documents, and the note would be false;
- `corpus` without a `CorpusSearch`;
- `corpus` with a non-Postgres `DATABASE_URL`.

**8. Provenance note.** The live/live state uses the existing `LIVE_PIPELINE_NOTE`, suffixed with the corpus version in the same way imaging staging is suffixed today: `pipeline complete, evidence retrieved from live corpus, corpus curated-v1`. The retriever's `name` is `curated-corpus-<version>`.

**9. Injection containment is layered, and the review gate is the primary layer.** (i) human review of every passage; (ii) ingestion normalizes Unicode (NFC), strips control and zero-width characters, caps passage length, and **rejects** (does not silently strip) passages matching instruction-like patterns (role markers, "ignore previous instructions", chat-template tokens, fenced code), so a human decides; (iii) `SYSTEM_PROMPT` gains a rule that `EVIDENCE` passages are quoted third-party literature to be treated as data, never instructions; (iv) the structural containment ADR-005 already built stays unchanged: the model selects evidence by id, the orchestrator re-resolves every id, and output is schema-validated.

## Why

**Curated over live PubMed.** Chosen by the owner after comparing the options. The decisive factors: the tier policy needs a trustworthy tier label, which PubMed publication types do not reliably give; a vetted passage removes most of the injection surface rather than filtering it; no patient-derived query leaves the system; and demos and tests stay repeatable.

**YAML source files over SQL or Python fixtures.** They diff cleanly in review, carry a reviewer's name next to the passage they approved, and are exactly what a fetch script can emit. Python fixtures invite code-shaped edits to clinical content; SQL seeds hide provenance.

**Postgres FTS over embeddings.** Chosen by the owner. For a corpus of tens to low hundreds of passages keyed on condition and symptom names, lexical search is adequate, explainable, and adds neither an extension nor an embedding call. `scripts/build_embeddings.py` stays an unimplemented stub.

**A `CorpusSearch` protocol over importing `SessionLocal` in `app/ai/`.** It keeps the property ADR-003 relied on (the pipeline is unit-testable without a database) and keeps SQL in the repository layer where §7 puts it. Passing the request session through `RetrievalQuery` was rejected because `RetrievalQuery` is `extra="forbid"` wire-adjacent data, and a session in it would couple the contract to the ORM.

**Refusing mock + corpus over supporting it.** The combination has no use: it cannot produce a cited candidate and would need a fourth provenance label for a state nobody runs. Failing at startup is the ADR-005 precedent for misconfiguration.

**Postgres-marked tests plus a CI Postgres service over SQLite FTS5.** FTS5's ranking and tokenization differ from Postgres's; tests against it would pass while production ranks differently. The logic that does not need SQL (policy, normalization, term shaping, determinism, registry rules) stays on the fast suite.

## Consequences

- **A migration is added**: `corpus_documents`. No existing table changes. `analysis_evidence` already persists `document_id`, `chunk_id`, `source_url`, `source_tier`, `published_year` and `relevance_score`, so analyses produced from the corpus remain traceable even after a passage is retired.
- **`app/ai/` stays database-free.** The retriever never touches a `Session`.
- **The orchestrator changes by one suffix** in `_pipeline_note()`. The schemas, service and API do not change. No endpoint is added.
- **CI gains a Postgres service**, and `alembic upgrade head` is run against it, which also closes the gap that migrations are currently only checked for a single head.
- **`tests/conftest.py` pins `AI_RETRIEVAL_PROVIDER=mock`**, for the same reason it pins `AI_PROVIDER`.
- **Smaller evidence coverage.** An unmatched case yields `rag_no_evidence`, and a stage label without corpus coverage leaves the stage candidate uncited and dropped. The seed corpus must cover the six mock conditions and all five `STAGE_LABELS`.
- **Content is a human dependency.** The code can land and be fully tested with a clearly synthetic test fixture corpus under `tests/fixtures/`, which is never loadable in production. Switching any environment to `corpus` requires the reviewed seed set.
- **Determinism is preserved within a corpus version**: same corpus, same query, same order. Across versions it legitimately changes; the version in `pipeline_note` records which one answered.

## Risks

- **"Live corpus" can oversell a static curated set.** The note string is fixed by §8.1's table; the version suffix makes the static nature visible. How the demo is narrated still matters more.
- **Reviewer capacity and clinical judgment are the bottleneck**, not code.
- **Licence mistakes** are made by humans at curation time; the allow-list checks the declared licence, not the truth of it.
- **English stemming only.** Keywords must include canonical condition names, including the exact `STAGE_LABELS` strings, or matches will be missed.
- **Passages reach the PDF renderer.** Whether `app/reports` escapes passage text before any markup-interpreting renderer has not been verified in this ADR; the plan includes that check.
- **Pattern-based injection rejection is incomplete by nature.** It is a tripwire for review, not a guarantee; the structural containment is what bounds the damage.

## Alternatives Rejected

- **Live PubMed at analysis time**: unreliable tier labels, unvetted text in the prompt, patient-derived queries leaving the system, non-repeatable output.
- **pgvector / hybrid**: new extension and image, an embedding provider, and opaque ranking, for a corpus small enough that lexical search suffices.
- **SQLite FTS5 in tests**: different ranking semantics; false confidence.
- **Generalizing `MockLLMClient`**: makes the mock no longer a transparent fixture and adds a provenance state nobody uses.
- **Retriever importing `SessionLocal`**: breaks the database-free pipeline property.
- **Silently stripping suspicious passage text**: hides from the reviewer the very thing they should see.

## Testing Impact

- **Fast suite (SQLite, no network):** source-file schema (tier, licence, extra fields, instruction patterns, normalization, stable hash); `CorpusEvidenceRetriever` against a fake `CorpusSearch` (term shaping, tier re-filter, normalization, determinism, empty result, search exception propagates); registry combinations; orchestrator note with a live retriever and version suffix; `SYSTEM_PROMPT` evidence rule.
- **Postgres suite (`@pytest.mark.postgres`, skipped unless `TEST_POSTGRES_URL` is set, always run in CI):** migration up/down; generated column, GIN index and `CHECK` present; ingestion idempotence, all-or-nothing validation and version retirement; ranking weights; hostile complaint text containing tsquery operators and SQL metacharacters returns results or none, never an error.
- **Regression gates, unchanged:** `test_ai_mock_providers.py` including its determinism assertion, `test_ai_live_llm.py`, `test_ai_orchestrator.py`.

## Migration / Rollback Impact

One additive migration creating `corpus_documents`; its downgrade drops the table. Nothing references it by foreign key, and `analysis_evidence` rows carry copies of the metadata, so dropping it loses no analysis history.

Rollback is `AI_RETRIEVAL_PROVIDER=mock`. Analyses already produced keep the `pipeline_note` they were stored with, which is the correct historical record.
