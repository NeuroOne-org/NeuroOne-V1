# NeuroONE handbook evidence audit

MODE: TEST

Audit date: **13 September 2026**. Checkout: **`5d391b1`** (`5d391b1` is the implementation baseline before these documentation additions). Purpose: produce an accurate professor-facing learning and progress reference. This is a focused code/documentation audit, not a clinical evaluation or full security assessment.

## PR preparation update — `a01ae83`

Before publication, `main` advanced through PR #41. This follow-up on 13 September 2026 inspected the changed auth/config/frontend sources and reran the complete backend suite: **437 passed in 7.68 seconds**. The historical table and findings below remain evidence from `5d391b1`; the following updates supersede their auth/config/graph descriptions:

- OTP is now backend-enforced by default (`AUTH_REQUIRE_OTP=true`), and production refuses OTP-off configuration. The frontend follows the OTP-required response. Login and password-reset codes have isolated purpose keys.
- Login has per-IP and per-account limits of 10 attempts/15 minutes. Code requests have per-email/purpose limits of 3/10 minutes; verification/reset has 8/15 minutes. Counters and OTPs remain process-local. Session-cookie limitations remain.
- Gmail settings are required only with default email delivery. Explicit `OTP_DELIVERY=console` permits local synthetic-data rehearsal without Gmail and logs codes/identity; this qualifies HB-10. Checked-in Compose still omits the default email requirements and durable scan mounting.
- Upstream refreshed the root graph to 3,041 nodes/7,116 links and the dated snapshot to 3,012/7,063. Both record build commit `5d391b1` and now include ADR-007 nodes, superseding the omission in HB-18. They still predate the newer auth commit. This authoring task did not rebuild those graphs.

The learning reference, professor guide and tutor prompts use `a01ae83` as their refresh baseline. Non-auth findings retain their original inspected/probe evidence; the diff to this baseline did not change those application components. Frontend execution, live PostgreSQL, SMTP and external model evaluation remain unperformed.

## Evidence and verification

| Check | Observation |
|---|---|
| Existing Graphify query | Used root graph to identify product/safety/provider/ownership/report concepts, then inspected referenced source |
| Vocabulary expansion | `architecture, clinical, decision, demo, evidence, history, llm, mri, provider, report, review` selected from graph vocabulary |
| Requirements inspected | PRD, APP-FLOW, TRD, MVP scope, AGENTS.md and CLAUDE.md |
| Decisions inspected | ADR-001 through ADR-007 and AI-02b implementation plan |
| Current backend OpenAPI | **35 `/api/v1` method/path operations**, generated from current app under synthetic test settings |
| ORM metadata | **10 mapped tables**: users, patients, patient_phones, visits, symptoms, scans, analyses, analysis_findings, analysis_evidence, reports |
| Migration inventory | **13 migration files** in `backend/alembic/versions/` |
| Existing backend suite | **414 passed in 30.33s**, full suite, synthetic/offline provider configuration |
| Earlier backend attempt | 409 passed, five `tmp_path` setup errors due to sandbox denial of the default pytest temp directory |
| Recovery | Reran pytest with a new permitted `--basetemp`; all five storage tests then passed |
| Frontend source | Clinical endpoint wrappers and actual screen/hook consumers exist |
| Frontend test inventory | **6 test files**, plus CI defining lint, typecheck, test and production build |
| Local frontend execution | Not performed: `frontend/node_modules` absent. No dependency install performed. |
| Live reasoning probe | Serialized keys are PATIENT, CURRENT_VISIT, PRIOR_VISITS, TRENDS, EVIDENCE, MAX_CANDIDATES. No imaging, scan or scan_trend data included. |
| Stage-order probe | Confirmed non-stage candidate can rank above stage candidate |
| Report schema probe | No reviewed_by/reviewed_at fields in ReportSnapshot |
| Empty-input probe | No scan, no symptoms and complaint `routine visit` returns controlled `AIError`, code `rag_no_evidence` |
| Existing presentation | Extracted text from 15-slide `docs/NeuroOne Project PPT.pptx`; no visual/render audit performed |
| Live system / data | No live database seeded, no patient data modified, no external model call or SMTP email sent |

The suite was run from `backend` as `python -m pytest -q`. The successful run added `--basetemp` pointing to a fresh sandbox-permitted directory. Tests pin `AI_PROVIDER=mock`; live-provider tests use mocked transport. No actual secrets were reproduced in the handbook.

## Findings that affect the presentation

The priorities below reflect risk to an accurate report and working demo. They are recommendations, not approved production fixes.

| ID | Priority | Verified finding | Effect on your report / recommended next step |
|---|---|---|---|
| HB-01 | High | Old README/progress report says frontend calls no clinical endpoints. Current endpoints/hooks/pages do. | Report “frontend wiring implemented; browser verification outstanding.” Update stale status after current frontend checks. |
| HB-02 | High | APP-FLOW §10 excludes MRI while revised PRD §7/FR-08 and accepted ADR-006 admit scan intake/staging. | State the documented revision and unresolved APP-FLOW inconsistency. Reconcile behavior document through a separate planned documentation change. |
| HB-03 | High | LiveLLMClient ignores `ReasoningRequest.imaging` and `.scan_trend` and omits scan metadata. | Avoid claiming live MRI-plus-symptom reasoning works. Extend serialization/prompt/mapping and add a real integration regression check. |
| HB-04 | High | Ranker sorts confidence/name, without stage-first enforcement. | Describe a stage as one candidate. Resolve tension between required stage-first order and confidence ordering before implementing the fix. |
| HB-05 | High | Revised FR-07 says PDF records reviewer/time; ReportSnapshot and renderer omit them. | Say sign-off gate is implemented, reviewer-in-report content remains. Extend snapshot/rendering through an approved contract plan. |
| HB-06 | High | New-patient intake submits complaint/history/notes, with no structured symptoms. Follow-up submits name/severity/onset only. | Avoid demonstrating a complete FR-03 form. Complete duration/observation/symptom capture. Use seeded structured symptoms during rehearsal. |
| HB-07 | High | New-patient intake creates records before analysis and restarts creation on retry. | An analysis error preserves records but retry can duplicate intake. Add resume behavior and make saved records easy to recover. |
| HB-08 | High | Mock staging hashes checksum string and does not read image anatomy. Region values are digest-derived. | Disclose “simulated staging,” not trained imaging classification or measured region attribution. Real model/data/evaluation remain. |
| HB-09 | High | Mock corpus is synthetic. Registry always constructs MockEvidenceRetriever. AI-02b branch merged a Proposed ADR and plan, not a live retriever. | Do not claim PubMed/real RAG is live. Accept plan/ADR, assign reviewer, implement/index reviewed content and verify with PostgreSQL. |
| HB-10 | High | Compose API lacks required Gmail settings; Docker excludes `.env`. No scan volume is mounted. | Do not rely on clean container startup or retained scans after recreation. Complete configuration and storage, then verify boot/restart. |
| HB-11 | Medium | History excludes current id but not later dates, requests oldest other visits and appends target visit. | Historical target visits can use newer encounters, and default window is oldest ten. Plan an explicit temporal/window policy and tests. |
| HB-12 | Medium | Report builds current clinical inputs at report time, not analysis context time. | Later edits can mismatch earlier reasoning. Decide whether report should use the analysis snapshot or require rerun before sign-off/report. |
| HB-13 | Medium | Review uses active-user dependency and inherited ownership, not clinician-only role guard. No amendment payload/editor exists. | Authorized admin can sign; do not advertise clinician-only amendment workflow. Decide/reconcile intended review policy. |
| HB-14 | Medium | OTP codes are process-local, TTL 300 seconds, five failed guesses. JavaScript writes token cookie. | Describe demo mechanisms, not production MFA/session hardening. Persistent OTP/rate policies/session review remain. |
| HB-15 | Medium | Upload stores `dimensions={}` and MIME type from client; validates emptiness/size but does not parse MRI format. Conflict path deletes orphan file; general DB failure cleanup is not present there. | Claim retained bytes/checksum, not parsed MRI/DICOM geometry or fully coordinated file/DB transaction. Broaden parser/error cleanup under a plan. |
| HB-16 | Medium | Queue derives flags from latest analysis and signing does not close early-watch flags. UI fetches at most 100 rows. | Describe review prioritization, not a complete urgency/flag-resolution system or unlimited panel view. |
| HB-17 | Medium | No dedicated transaction-ownership ADR was found, though generic repositories commit and specific repositories group writes. | Describe observed convention; formalize before additional multi-repository orchestration. |
| HB-18 | Medium | Root graph and dated graph snapshots predate HEAD and omit ADR-007. Only two prior query-memory files found. | Treat graph as navigation and partial memory. Do not claim every chat/decision is captured. |
| HB-19 | Low | Leftover signup posts to nonexistent `/auth/register`; older route listings include nonexistent `GET /admin/users`. | Use admin-provisioned demo login and actual POST route. Clean up stale UI/contracts/documentation. |
| HB-20 | Medium | Candidate schema permits confidence up to 1; shipped providers clamp to 0.92. | Describe provider behavior accurately. Future provider must not be trusted to honor the ceiling without a shared enforcement check. |

Sources for findings: [frontend endpoints](../../frontend/src/lib/endpoints.ts), [follow-up form](../../frontend/src/app/dashboard/patients/[id]/visits/new/page.tsx), [new intake](../../frontend/src/app/dashboard/upload/page.tsx), [live client](../../backend/app/ai/providers/live_llm.py), [ranker](../../backend/app/ai/ranking.py), [analysis schema](../../backend/app/schemas/analysis.py), [report service](../../backend/app/services/report_service.py), [report schema](../../backend/app/schemas/report.py), [scan service](../../backend/app/services/scan_service.py), [history repository](../../backend/app/repositories/visit_repository.py), [triage service](../../backend/app/services/triage_service.py), [review API](../../backend/app/api/v1/analysis.py), [Compose](../../docker-compose.yml), [config](../../backend/app/core/config.py), [Docker exclusions](../../backend/.dockerignore).

## Exact document conflicts and proposed reconciliation

MODE: PLAN

No disputed application behavior was implemented during handbook authoring.

| Sources in conflict | Impact | Recommended resolution |
|---|---|---|
| APP-FLOW §10 “No MRI/image analysis…” versus PRD §7/FR-08 and accepted ADR-006 | Agents/presenters can incorrectly refuse or omit implemented scan flow | Align APP-FLOW primary, case, review, report and boundary flows with the accepted scan/sign-off revision |
| README Current Development and PROGRESS_REPORT September 12 “unconnected frontend/no frontend tests” versus current frontend and CI | Progress report understates delivered work | Rerun frontend checks and browser journey, then replace status with dated verified evidence |
| MVP scope Revised Roadmap still omits scan/review/dashboard phases, while AGENTS §15 and ADR-006 add them | Team can misstate remaining sequence | Update roadmap and remove stale “still no imaging” text in Early-detection design / Unaffected |
| AGENTS §8.3 clinician-entered-only/no imaging language versus revised PRD and AGENTS §19 | Internally contradictory architecture guidance | Reconcile the earlier design description with its accepted MRI extension |
| PRD FR-04/ADR-006 stage-first versus schema descending-confidence invariant and ordinary confidence ranking | Fix cannot simply prepend stage without deciding ranking semantics | Choose a representation/order that satisfies product intent, document it and test all providers |
| PRD FR-07 reviewer/time versus current report schema | Gate alone does not satisfy report content requirement | Add review snapshot fields and render them after a specific contract decision |
| ADR-006 “accepted or amended” versus sign-off-only service/API | Requirement broader than implemented review behavior | Specify amendment semantics or deliberately narrow the product requirement; do not quietly treat sign-off as an editor |

Relevant sources: [PRD](../PRD.md), [APP-FLOW](../APP-FLOW.md), [scope](../NEUROONE-MVP-SCOPE.md), [AGENTS](../../AGENTS.md), [old progress report](../../reports/PROGRESS_REPORT.md), [old frontend README](../../frontend/README.md), [ADR-006](../decisions/ADR-006-mri-primary-with-symptoms-as-context.md).

## Isolated probe details

These probes used existing `test_ai_staging.py` helpers and synthetic settings. No production database was queried.

**Stage rank counterexample:** use scan checksum `0000000000000000000000000000000000000000000000000000000000000001`, complaint `intermittent hand tremor`, and current symptoms tremor, bradykinesia, rigidity and gait disturbance, all severity 10. Running the mock orchestrator produced:

```text
Parkinsonian syndrome     confidence 0.83
Cognitively normal        confidence 0.7444
Essential tremor          confidence 0.21
```

The stage appears and is cited, but ranks second. This is an observed requirement gap despite the passing suite. Tests currently check that a stage candidate appears; they do not establish stage-first ranking for all input combinations.

**Live prompt probe:** construct a ReasoningRequest with both context scan and a StagingResult, then call `LiveLLMClient._render_case`. Top-level JSON keys omit staging/scan trend, and current/prior visit serialization also omits scan metadata. This verifies the omission independently of an external model response.

**Reviewer probe:** inspect `ReportSnapshot.model_fields` and the mapping/rendering path. There are no review fields. That means reviewer identity and review time cannot reach the renderer through its supported input.

## Graph audit

| Item | Root graph | `2026-09-13` snapshot |
|---|---|---|
| Nodes | 2,875 | 2,831 |
| Links | 6,754 | 6,675 |
| Built commit | `7c1308ee` | `9ab89749` |
| ADR-007 source nodes | 0 | 0 |

Root confidence tags: 6,143 EXTRACTED, 606 INFERRED, 5 AMBIGUOUS. Report's rounded 0% ambiguous does not mean zero ambiguous links. Existing run reports zero extraction input/output tokens. Query results were explicitly truncated, so they were used for orientation rather than as an exhaustive implementation inventory.

Prior memory contains migration CI guidance and an AI-01-era planning answer. It is useful historical context, not proof of current defects or complete chat retention. A new supported Graphify memory record will point to this handbook; graph rebuilding is a separate operation, and this authoring pass did not rebuild the graph.

## Existing presentation audit limits

Text extraction found 15 slides. Slides 2–4 include general medical motivation and imaging/explainability claims. Slide 8 mentions public datasets, PyTorch, Colab, low cost, minimal training and scalability. These are proposal/feasibility statements unless independently supported. This audit did not research clinical background, dataset licences, current provider pricing or training outcomes.

Slides 5, 6, 7, 9, 10, 11, 12 and 13 yielded only headings in text extraction. Their substantive content may be raster artwork, diagrams or other objects. It was not visually inspected. The presenter should check it manually using the slide-specific guidance in [PROFESSOR-PRESENTATION.md](PROFESSOR-PRESENTATION.md).

## Validation assessment

MODE: TEST

**Scope:** current backend checks, source/graph/deck-text audit and handbook correctness.

**Requirements verified:** tested auth, authorization, input/AI validation, citation metadata, deterministic staging/trends, report generation gate and controlled failures under test conditions. FR-03 UI completeness, FR-04 stage-first behavior, FR-07 reviewer content and real FR-05/FR-08 provider capability are not fully satisfied.

**Tests run / passed:** existing backend suite, 414 passed; isolated stage-order, live serialization, report-field, empty-input, OpenAPI and metadata probes.

**Failed:** no product-test failures in the final run. Initial storage fixture errors resolved through permitted temp-path configuration. Probes revealed requirements not covered by the passing suite.

**Regression status:** backend suite passed. Frontend and full browser regression unverified.

**Logic assessment:** substantial workflow implementation, with specific input, temporal, ranking and report-consistency gaps recorded above.

**Security assessment:** server authentication/authorization exists and is covered by tests; this is not an independent production penetration/security review.

**Clinical safety assessment:** ranked output, citation resolution, disclaimer and report gate exist. Simulated evidence/imaging and missing integration prevent any clinical validation claim.

**Known gaps:** local frontend execution, live PostgreSQL migration/application flow, clean Compose boot/restart, visual PPT review, real model/corpus evaluation and complete chat recovery.

**Handbook validation:** all six Markdown documents were checked for local file/heading links and paired code fences. All 151 local links resolved. Repeated API, migration, test and graph counts were checked against the recorded inspection/probe results. Application source was not changed.

**Final verdict for this focused audit:** PASS WITH KNOWN LIMITATIONS

That verdict means the learning material can describe the inspected state with disclosed limitations. It does not certify the MVP as fully demo-ready or clinically ready.
