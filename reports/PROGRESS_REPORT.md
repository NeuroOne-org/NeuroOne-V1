# NeuroONE Progress Report

**Report date:** September 12, 2026
**Supersedes:** the July 23, 2026 edition of this report, which described a
repository with no endpoints, no models and no tests. That description is now
badly out of date and was actively misleading anyone — or any agent — reading
it as current state.
**Current phase:** Backend complete for the MVP journey; frontend not connected
**Overall status:** In progress, with the gap concentrated in one place
**Assessment basis:** Repository contents at `89b4a8d`, a full test run, and the
standards in [`CONTRIBUTING.md`](../CONTRIBUTING.md)

## Executive Summary

The backend implements the full PRD §8 acceptance journey. Every layer the
architecture calls for exists and is exercised: 8 SQLAlchemy models, 8
repositories, 10 services, 8 API modules, 13 Alembic migrations, and 400 tests
across 32 files that pass in under ten seconds. CI runs them on every push.

[ADR-006](../docs/decisions/ADR-006-mri-primary-with-symptoms-as-context.md)
landed in full: MRI scans attach to visits, a staging provider seam sits
alongside the retriever and reasoning seams, trend detection consumes
scan-derived metrics, clinician sign-off gates report generation, and a ranked
triage queue replaces the dashboard's stat tiles.

**The frontend consumes none of it.** A grep of every API call in
`frontend/src` returns four, all authentication, and one of those posts to an
endpoint that AUTH-01 deliberately removed. All twenty-nine clinical endpoints
have no caller. The dashboard renders a hardcoded patient array and still
displays the framing ADR-006 requires be deleted.

This is the single highest-value gap in the repository. The previous report's
risk — "documentation overstates progress" — has inverted: the documents
understated it, and the interface is where the work now is.

## Progress at a Glance

| Workstream | Status | Current evidence |
| --- | --- | --- |
| Backend foundation | Complete | FastAPI app, config, database session, exception handlers, CORS, health route |
| Authentication | Complete | login, me, forgot-password, reset-password, request-otp, verify-otp; self-registration deliberately removed and guarded by a regression test |
| Patient management | Complete | CRUD, search, soft delete, ownership enforcement per ADR-001/ADR-002 |
| Visits and symptoms | Complete | Visit CRUD, symptom CRUD, cross-visit history endpoint |
| Scan intake | Complete | `POST/GET /visits/{id}/scan`, checksum and dimensions in the database, bytes in file storage per ADR-006 decision 5 |
| AI diagnosis | Contract complete, providers mocked | Orchestrator, context building, ranking, trend detection; retrieval and staging simulated, reasoning live-capable per ADR-005 |
| Clinician sign-off | Complete | `POST /analyses/{id}/review`; report generation is gated until an analysis is signed |
| Reports | Complete | Snapshot persistence and PDF rendering per ADR-004 |
| Triage queue | Complete | `GET /triage`, ranked by early-watch flags, trend and review state |
| Database migrations | Complete | 13 revisions, single head verified in CI |
| Automated testing | Complete for backend | 400 tests, 32 files; no frontend tests exist |
| Frontend | Mockup, unconnected | Calls four auth endpoints and no clinical endpoint; dashboard data is a hardcoded array |
| Containerization | Partial | Compose runs Postgres and the API; no volume for scan storage |
| Documentation | Reconciled by this cycle | ADRs are current; this report, `backend-routes.json` and the frontend checklists were stale until now |

## Current Verification Results

| Check | Result |
| --- | --- |
| Backend test suite | Pass: 400 tests, 32 files |
| Alembic heads | Single head |
| Migration revisions | 13 |
| Implemented `/api/v1` business endpoints | 35 |
| Frontend calls to clinical endpoints | 0 |
| Frontend tests | 0 |
| CI coverage | Backend only |

## Implemented API Surface

```text
auth      POST /auth/login, /auth/forgot-password, /auth/reset-password,
          /auth/request-otp, /auth/verify-otp        GET /auth/me
admin     POST|GET /admin/users
patients  POST|GET /patients   GET /patients/search
          GET|PATCH|DELETE /patients/{id}
          POST|GET /patients/{id}/visits   GET /patients/{id}/visits/history
visits    GET|PATCH|DELETE /visits/{id}
          GET|POST|PATCH|DELETE /visits/{id}/symptoms[/{symptom_id}]
          POST|GET /visits/{id}/scan
          POST|GET /visits/{id}/analyses   GET /visits/{id}/analyses/latest
analyses  GET /analyses/{id}   POST /analyses/{id}/review
          POST|GET /analyses/{id}/reports
reports   GET /reports/{id}   GET /reports/{id}/pdf
triage    GET /triage
```

## Conformance With the Contributing Guide

### Architecture

The required `Feature -> API -> Service -> Repository -> Model -> Schema` flow
is implemented and exercised by tests at every layer, not merely present as
directories. The previous report's finding that "architecture exists only as
folders" is resolved.

### Branch and Pull Request Workflow

Feature branches and pull requests are in use; ADR-006 merged as PR #32. Two
residual issues: 14 branches remain outstanding, several apparently merged or
abandoned, and `docs/mri-primary-scope-revision` carried five backend
implementation commits under a documentation branch name.

### Testing and Definition of Done

Backend features meet the definition of done. Frontend work does not: there are
no frontend tests and no CI job that would run them.

## Risks and Blockers

### High

1. **The frontend is not connected to the backend.** Twenty-nine clinical
   endpoints have no caller. Until this closes there is no demoable product
   regardless of backend completeness, and the acceptance journey cannot be
   walked through the UI as `NEUROONE-MVP-SCOPE.md` requires.
2. **The dashboard still carries framing ADR-006 requires removed.** A "Model
   certainty" stat tile, `Critical`/`Stable` severity vocabulary with no
   backing in the model, confidence figures above the 0.92 ceiling, and
   `stageLabel` as a headline badge. These are FR-04 violations that are
   currently rendering, not theoretical.
3. **Scan storage is not durable in the container.** `SCAN_STORAGE_DIR`
   defaults to a local filesystem path and the `api` service in
   `docker-compose.yml` mounts no volume for it, so uploaded scans are lost
   when the container restarts. ADR-006 predicted this dependency; it is
   unaddressed.

### Medium

1. **Seed data predates ADR-006.** `scripts/seed_demo_case.py` creates the
   multi-visit symptom trend that an `early_watch` flag needs, which is real
   coverage. It seeds no `Scan`, so scan-derived trends are unexercised, and it
   seeds one patient, so a ranked triage *queue* has a single row to rank.
2. **The synthetic-data assumption is still unconfirmed.**
   `NEUROONE-MVP-SCOPE.md` flags it and ADR-006 raises its cost, because scans
   are imaging PHI retained as source data rather than discarded after
   analysis. It should be confirmed explicitly before any non-synthetic scan is
   loaded.
3. **A mocked staging model is more convincing than mocked text.** A brain
   region with a percentage reads as measurement. The per-analysis provenance
   line (ADR-006 decision 9) is the mitigation and must reach the UI, not just
   the API response.
4. **Version mismatch persists.** `APP_VERSION` is `1.0.0` in
   `backend/app/core/config.py` and `0.1.0` in `backend/.env.example`. This was
   flagged in the July report and is still open.
5. **No frontend CI.** `.github/workflows/backend-tests.yml` is the only
   workflow.

### Resolved Since the Previous Report

- `backend/.env` is no longer tracked.
- Compose starts a real API and Postgres with health checks.
- Domain models, migrations, services, repositories and tests all exist.
- The health route returns 503 with a body rather than a normal response.

## Recommended Next Milestones

### Milestone 1: Document reconciliation (this cycle)

Bring the written record in line with the code: this report,
`backend-routes.json`, the two frontend checklists, the root README module
table, and the parked status of `frontend/web-page`. Refresh the graphify graph
afterwards so the god nodes reflect the corrections.

### Milestone 2: Connect the frontend, in vertical slices

Each slice demoable end-to-end against real endpoints, in demo-narration order:

1. **FE-00 foundations** — typed API client generated from the live
   `openapi.json`, real 401/session handling, design tokens, and removal of the
   signup page that posts to a deliberately dead endpoint.
2. **FE-01 triage queue** replacing the dashboard, against `GET /triage`.
3. **FE-02 patients** — list, search, detail, create (demographics only, per
   ADR-006 decision 8).
4. **FE-03 visit** — new visit, scan upload, symptoms. The current upload page
   posts a contract that never existed and is rebuilt, not adapted.
5. **FE-04 analysis** — ranked differential, evidence and citations,
   `early_watch` with `trend_basis` held visually distinct from external
   evidence, provenance line, no lone stage badge, no confidence above 92%.
6. **FE-05 sign-off to PDF** — `POST /analyses/{id}/review`, then download.

Extend the seed script to cover scans and several patients before FE-01, or the
queue has nothing to rank.

### Milestone 3: Deployment readiness

Mount scan storage, align the version settings, add a frontend CI job, confirm
the synthetic-data decision in writing, and prune the outstanding branches.

### Milestone 4: AI-02b, deferred

The real retrieval corpus behind the AI-01 interface. Deliberately deferred in
`NEUROONE-MVP-SCOPE.md` until a trusted-literature corpus, an index and a
source-tier policy are decided — and it is where prompt-injection exposure
actually lands, because a retrieved passage is untrusted text in a way a
symptom field is not.

## Definition-of-Done Dashboard

| Requirement | Backend | Frontend |
| --- | --- | --- |
| Code implemented | Yes | Mockup only |
| API works | Yes, 35 endpoints | Not applicable |
| Tests pass | Yes, 400 | None exist |
| Documentation updated | Yes, as of this cycle | Checklists reconciled this cycle |
| Migration verified | Yes, single head in CI | Not applicable |
| Pull request approved | Yes | Not applicable |

## Next Review Exit Criteria

The next review should occur after FE-01 and FE-02 merge. At minimum it should
demonstrate:

- A clinician logging in and seeing a triage queue populated from `GET /triage`.
- A patient list and detail view reading real records.
- No hardcoded clinical data remaining in the frontend.
- None of the FR-04 framing violations listed above still rendering.
- A frontend CI job that runs on pull requests.
