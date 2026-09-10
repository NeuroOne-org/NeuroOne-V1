# ADR-004: Clinical Report Snapshot and Rendering

## Status
Accepted

## Context

`REPORT-01` is next on the locked roadmap (`docs/NEUROONE-MVP-SCOPE.md` line 49) and is the ticket that makes the PRD §8 acceptance journey demoable end to end: `Login → Patient → Case → Symptoms → AI Analysis → Differential Diagnosis + Evidence → Clinician Review → PDF Report`. `AGENTS.md` §17 requires a decision record before implementation for a new domain entity and its persisted contract; `Report` is both.

Inspection found the existing `Report` model is `class Report(BaseModel): pass` -- an empty stub carrying only a stale ASCII schema comment (`pdf_path`, `summary`, `recommendations`) that predates every persistence pattern this codebase now uses. `reports.py` is a router with zero routes. Nothing here can be extended; it is replaced.

Two upstream corrections landed immediately before this ADR and are assumed complete: `AI-01C` (evidence provenance -- `document_id`, `chunk_id`, `source_tier`, `published_year`, `relevance_score` now survive retrieval through persistence) and `CASE-01C` (`symptoms.observation`, FR-03). `REPORT-01` consumes both; a report generated before they existed would have nothing to show for citation provenance or clinician observations.

## Problem

1. What does a report persist, and what is it forbidden to persist?
2. Where does PDF bytes live -- at rest, or rendered on demand?
3. What happens if rendering fails partway through generation?
4. How does a report stay immutable when the analysis, visit, or patient it was generated from can still be edited later?
5. How is a report authorized, given it has no owner column of its own?

## Constraints

- FR-07 (`docs/PRD.md` line 51): a report contains patient/case information, clinical inputs, differential diagnosis, reasoning, evidence, citations, and an appropriate disclaimer. A report missing citations or the disclaimer is incomplete (`AGENTS.md` §7).
- `AGENTS.md` §12: minimize unnecessary exposure of patient data; no PHI in logs; no unencrypted temporary files.
- `AGENTS.md` §8.2: never represent output as a definitive diagnosis -- this constraint reaches the PDF, not just the API.
- Layering is fixed (`AGENTS.md` §7): `Client → API → Service → Repository → PostgreSQL`. A renderer is not a layer that queries the database or authorizes anything.
- Ownership must follow the ADR-002 masking pattern applied one level deeper, as `ADR-003` already did for `Analysis`.

## Options Considered

**For PDF storage:** (a) render to a file on the container filesystem and store `pdf_path`; (b) store the rendered PDF as bytes in a database column; (c) store a typed snapshot only, and render PDF bytes on demand for every download.

**For renderer library:** (a) ReportLab (Platypus), programmatic, no system dependency; (b) WeasyPrint, HTML/CSS-driven, requires Pango/Cairo; (c) headless-browser print-to-PDF.

**For report ownership/authorization:** (a) a `doctor_id` column on `reports`, checked directly; (b) no column of its own -- authorize through the existing `analysis_id → visit → patient` chain, exactly as `Analysis` already does one level up.

## Decision

**1. Persist a typed `ReportSnapshot` as JSONB; never store PDF bytes or a filesystem path.** `reports.snapshot` is exactly what `backend/app/reports/renderer.py` is allowed to see. A download re-renders from the stored snapshot; it never re-runs the AI pipeline and never re-queries the (possibly since-edited) `Analysis`, `Visit`, `Patient`, or `Symptom` rows.

**2. ReportLab (Platypus).** No new system dependency, a pure-Python-plus-wheel package already validated against this stack's Python 3.11. WeasyPrint's Pango/Cairo requirement is a real Windows/Docker cost this ticket does not need to pay for a two-to-three-page clinical PDF. A headless-browser render is untestable without a browser in CI and cannot produce a stable protected artifact behind an authenticated download endpoint.

**3. Render before persist.** `ReportService.generate_report` builds the `ReportSnapshot`, calls the renderer to prove it produces valid PDF bytes, and only then constructs and commits the `Report` row. A rendering failure raises before any row exists -- there is nothing to roll back, following the same "failure precedes the first write" pattern `ADR-003` established for `AnalysisService.analyze_visit`.

**4. `reports` has no owner column.** Authorization is `ReportService` calling `AnalysisService.get_analysis(db, analysis_id, current_user)` -- reusing its existing masked-404 behavior -- then `VisitService.get_visit` and `PatientService.get_patient` to assemble the snapshot, exactly the three-read pattern `AnalysisService.analyze_visit` already uses. A `Report` reached by its own id re-derives the same chain and 404s as `Report`, not as `Analysis` or `Visit`, if the caller has no claim to it.

**5. One table, `reports`.** Columns: `id`, `analysis_id` (FK, indexed), `generated_by_id` (FK to `users`), `generated_at`, `filename`, `snapshot` (JSONB), plus the `BaseModel` timestamp/soft-delete columns. No `pdf_path`, no binary PDF column -- the stub's design is explicitly superseded, not extended.

**6. Filenames carry no PHI.** `neuroone-report-{report_id}.pdf`. The report id is generated in the service (not left to a database default) so the filename is available before the row is constructed.

**7. Multiple reports per analysis are permitted; none are ever mutated.** Regenerating a report for the same analysis creates a new row with a new snapshot, mirroring `Analysis` never overwriting on visit re-run (`ADR-003` §92). There is no "latest report" convenience endpoint: a report is always requested by its own `report_id` or listed under its `analysis_id`, never inferred.

## Why

**Snapshot-only, no stored PDF** because a stored PDF is either wrong twice (once at rest, once if regenerated) or a second source of truth to keep consistent with the snapshot. Rendering on every download is cheap for a document this size and means the download endpoint can never serve stale bytes -- correctness follows directly from the immutability the snapshot already guarantees. It also directly serves `AGENTS.md` §12: no PHI-bearing PDF sits on a container filesystem or in a binary database column that a routine backup or log scrape could pick up.

**Render before persist** because it is the same guarantee `ADR-003` already made for the AI pipeline, applied to a much smaller surface: when every failure precedes the first write, there is nothing to roll back and no partial `Report` row can exist to be found half-rendered or re-downloaded broken.

**No owner column** because `analysis_id` already resolves to exactly one owning clinician through the chain `ADR-002` and `ADR-003` established, and a second, independent authorization path would eventually drift from the first. Re-deriving through `AnalysisService` also means a `Report`'s authorization is exactly as correct as `Analysis`'s already-tested authorization, not a parallel implementation that could disagree with it.

**A snapshot, not live relations, because a report is read once at generation time and is never expected to reflect later edits** -- exactly the reasoning `ADR-003` gave for `trend_basis`, applied one level up. A clinician revising a symptom's severity after generating a report must not silently rewrite what that report already said a patient's case looked like.

## Consequences

- `backend/app/reports/renderer.py` is a pure function `render(snapshot: ReportSnapshot) -> bytes`. It imports no repository, opens no `Session`, and performs no authorization -- mirroring how `app/ai/` stays database-free (`ADR-003` §2).
- `ReportService` composes `AnalysisService`, `VisitService`, and `PatientService` rather than querying their tables directly, so a change to any of their authorization rules is inherited automatically.
- `EvidenceResponse`'s additive `document_id`/`chunk_id`/`relevance_score` fields (`AI-01C`) and `SymptomBase.observation` (`CASE-01C`) are both consumed here; `ReportSnapshot` is the first schema to require both.
- A report's `snapshot` duplicates clinical data already stored on `Analysis`/`Visit`/`Patient`/`Symptom` by design. This is the cost of immutability, not an oversight, and it means `reports` inherits the same retention and authorization sensitivity as those tables.
- Downloading a report is idempotent and side-effect-free: it always re-renders the same bytes from the same stored snapshot.

## Risks

- ReportLab 5.0.1 is a recent pin for this stack; a rendering smoke test runs immediately after the dependency lands, before the full layout is built.
- A snapshot duplicating patient data means a retention or right-to-erasure policy (not yet defined for this MVP) will eventually need to reach `reports.snapshot` as well as the source tables. Flagged, not solved, here.
- Re-rendering on every download means a very large snapshot could make downloads slow; not a concern at MVP data volumes, worth revisiting only if report content grows materially (e.g. embedded images).

## Alternatives Rejected

- **Storing a rendered PDF (file or column)** -- see *Why*: a second source of truth and a PHI-at-rest surface neither the snapshot-only design nor `AGENTS.md` §12 need.
- **A `doctor_id` column on `reports`** -- would duplicate authorization logic that `analysis_id → visit → patient` already provides correctly, and could drift from it.
- **WeasyPrint / browser print-to-PDF** -- see *Why*: system-dependency cost and testability, respectively.
- **An implicit "latest report" endpoint** -- multiple reports per analysis are allowed by design (§4 of the Decision), so "latest" is ambiguous in a way "by `analysis_id`, newest first" is not.

## Testing Impact

New suites: `test_report_model.py` or folded into `test_report_repository.py` (model + migration), `test_report_repository.py` (CRUD, soft-delete, scoping to `analysis_id`), `test_report_renderer.py` (PDF signature, page count, `pypdf`-extracted required content, pagination, Unicode fallback), `test_report_service.py` (render-before-persist ordering, masked 404s, no partial row on render failure), `test_report_api.py` (all four endpoints, cross-clinician masking, download headers). No existing test file is modified beyond what `AI-01C`/`CASE-01C` already touched.

## Migration / Rollback Impact

One additive migration on top of `b2b31bad27df` (the `CASE-01C` `symptoms.observation` column) creates `reports`: `id`, `analysis_id` (FK to `analyses`, indexed), `generated_by_id` (FK to `users`), `generated_at`, `filename`, `snapshot` (JSONB), plus the standard timestamp/soft-delete columns. No existing table is altered. `downgrade()` drops `reports` and its index; there is no enum type to drop.
