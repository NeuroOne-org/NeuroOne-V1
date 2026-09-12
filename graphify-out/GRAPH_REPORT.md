# Graph Report - audit-dependencies-api-container-268d38  (2026-09-13)

## Corpus Check
- 283 files · ~194,094 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2977 nodes · 6982 edges · 186 communities (132 shown, 45 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 647 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5d391b1c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- EntityNotFoundError
- UserRole
- new/page.tsx
- test_ai_orchestrator.py
- RetrievedDocument
- visits.py
- test_report_renderer.py
- v1/analysis.py
- DiagnosisCandidate
- test_ai_live_llm.py
- get_db
- AuthService
- reset-password/page.tsx
- test_ai_staging.py
- test_visits_api.py
- Analysis
- test_analysis_api.py
- types.ts
- index.ts
- build_backend_architecture_report.py
- auth-provider.tsx
- PatientService
- User
- frontend/package.json
- StagingRequest
- ReportRepository
- Patient
- v1/auth.py
- Visit
- detect_trends
- LocalScanStorage
- analysis-findings.tsx
- ReasoningRequest
- r3f-canvas-scene.tsx
- NeuroOne Design System
- patient_visits.py
- BaseRepository
- components.json
- NeuroOne Frontend — Design System
- BaseModel
- Clinician Sign-Off Gates the Report
- PLAN — AI-02b: Curated Retrieval Corpus
- compilerOptions
- test_scan_api.py
- cn
- Base
- SymptomRepository
- test_report_service.py
- VisitRepository
- ReportSnapshot (typed JSONB snapshot)
- NeuroOne Frontend — Redesign Checklist
- compilerOptions
- Three Provenance States and pipeline_note
- test_auth_api.py
- ADR-006: MRI Becomes a Primary Input, With Symptoms as Context
- Two Narrow Protocol Provider Seam
- Backend Tests Workflow
- ADR-006 MRI Primary With Symptoms as Context
- ScanResponse
- UserResponse
- Ownership Violations Return 404, Not 403
- dependencies
- [id]/page.tsx
- ReportService
- web-page/src/lib/api.ts
- AI Output Contract
- test_otp_service.py
- MVP Acceptance Journey
- build_clinical_context
- create_access_token
- Per-Record Ownership Check
- interactive-pipeline-demo.tsx
- AnalysisOrchestrator
- dashboard/layout.tsx
- ADR-003: AI Analysis Contract and the Mocked-Provider Seam
- REPORT-01D — Frontend Requirements & Backend Mapping Checklist
- ADR-006-mri-primary-with-symptoms-as-context.md
- UserRepository
- ScanService
- ADR-004: Clinical Report Snapshot and Rendering
- ADR-005: Live LLM Provider Behind the AI-01 Seam
- Current Development Status Table
- reports.py
- devDependencies
- FR-04 Differential Diagnosis
- test_patients_api.py
- Design boundaries
- web-page/package.json
- test_report_api.py
- get_triage_queue
- NeuroOne Login Neurons Artwork v1
- ValidationApplicationError
- ReportFindingSnapshot
- neural-network.tsx
- 2. Color system
- test_scan_service.py
- .get_by_patient
- FR-07 Clinical Report
- web-page/next-env.d.ts
- NeuroONE Frontend Redesign (parked)
- register_exception_handlers
- UserService
- .verify_credentials
- test_deleted_at_timezone_migration.py
- test_triage_api.py
- likelihood_band_for
- 14056b8ec27d_create_scans.py
- 1f74d19af1b8_widen_patient_email_and_promote_phone_.py
- 7544ad0b1ed6_add_analysis_sign_off.py
- 8e72c1f4a9b0_replace_legacy_user_roles.py
- a3c7be51d904_create_visits_and_symptoms.py
- b2b31bad27df_add_symptom_observation.py
- b8d41e2f7c53_make_deleted_at_timezone_aware.py
- c4e19a7b6d20_create_analyses_findings_and_evidence.py
- dcfbc7d5b2c9_create_reports.py
- frontend/next.config.mjs
- scripts
- ADR-007: Curated Retrieval Corpus Behind the AI-01 Seam
- web-page/src/lib/validation.ts
- Q: How are Alembic migrations and backend tests configured, and where should PR CI run pytest?
- Q: The parallel AI-01 work is committed and pulled; plan our next work
- frontend/src/app/layout.tsx
- web-page/src/app/layout.tsx
- Password-strength
- 17. Implementation Tasks
- RAG Requirements
- get_user_service
- test_health.py
- api service (FastAPI backend)
- Clinician Review Flow
- frontend/next-env.d.ts
- web-page/tailwind.config.ts
- PLAN.md
- NeuroOne login artwork v1
- corpus/__init__.py
- constants.py
- reports/__init__.py
- conftest.py
- CLAUDE.md
- Standard API Response Envelope
- Feature Branch Strategy
- AI Flow
- Middleware-Based Route Protection
- frontend/tailwind.config.ts
- fonts/README.md
- backup.py
- build_embeddings.py
- ingest_documents.py
- seed_database.py
- app/main.py
- FastAPI
- AI-01 Contract-Real Provider-Mocked
- Error Handling Contract
- .__init__
- vocabulary.test.ts
- scan_repository.py
- schemas/patient.py
- web-page/src/app/login/page.tsx
- pytest-asyncio
- uvicorn
- CONTRIBUTING — NeuroONE Contributing Guide
- Commit Message Convention
- docker-compose.yml — Local Dev Stack
- JWT Environment Configuration (HS256, 30-min access token)
- APP-FLOW — Application Flow
- Authentication Flow
- Failure Flows (AI/RAG, Database, Invalid Input)
- Patient Flow (Patient Profile → Cases / History)
- Primary Flow (Login → Dashboard → … → Report)
- Single-Source Ownership Rule via Service Composition
- Patient Soft-Delete Does Not Cascade to Visits
- Implementation Sequence
- Frontend README — Next.js 14 Client
- Client-Side Password Rule
- OTP Email Verification Flow
- Radiology-Viewer Design Aesthetic
- proxy.ts

## God Nodes (most connected - your core abstractions)
1. `User` - 127 edges
2. `EntityNotFoundError` - 92 edges
3. `UserRole` - 84 edges
4. `BaseModel` - 81 edges
5. `Visit` - 61 edges
6. `VisitService` - 58 edges
7. `cn()` - 54 edges
8. `AnalysisOrchestrator` - 53 edges
9. `get_db()` - 53 edges
10. `VisitStatus` - 52 edges

## Surprising Connections (you probably didn't know these)
- `MAX_CONFIDENCE 0.92 Ceiling` --semantically_similar_to--> `Clinical Safety Boundary`  [INFERRED] [semantically similar]
  docs/REPORT-01D-frontend-checklist.md → AGENTS.md
- `404 Ownership Masking` --semantically_similar_to--> `Security and Privacy Rules`  [INFERRED] [semantically similar]
  docs/REPORT-01D-frontend-checklist.md → AGENTS.md
- `Parked Design Reference (frontend/web-page)` --conceptually_related_to--> `Intake Splits Into New Patient and New Visit`  [INFERRED]
  frontend/web-page/README.md → docs/decisions/ADR-006-mri-primary-with-symptoms-as-context.md
- `MRI Upload + Prediction Polling` --conceptually_related_to--> `V1 Exclusions`  [AMBIGUOUS]
  frontend/README.md → docs/PRD.md
- `storage_key Deliberately Off the Wire` --semantically_similar_to--> `Security and Privacy Rules`  [INFERRED] [semantically similar]
  docs/REPORT-01D-frontend-checklist.md → AGENTS.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Three-Seam AI Provider Architecture (retrieval, reasoning, staging)** — docs_decisions_adr_003_ai_analysis_contract_and_provider_seam_evidenceretriever, docs_decisions_adr_003_ai_analysis_contract_and_provider_seam_llmclient, docs_decisions_adr_006_mri_primary_with_symptoms_as_context_staging_provider_seam, docs_decisions_adr_003_ai_analysis_contract_and_provider_seam_registry_build_providers [EXTRACTED 1.00]
- **Honest Provenance Labelling Across Analysis, PDF and UI** — docs_decisions_adr_003_ai_analysis_contract_and_provider_seam_pipeline_note, docs_decisions_adr_005_live_llm_provider_hybrid_pipeline_note, docs_decisions_adr_006_mri_primary_with_symptoms_as_context_per_analysis_provenance, frontend_web_page_readme_design_boundaries [EXTRACTED 1.00]
- **MVP Acceptance Journey Across Product, Scope and Implementation** — docs_prd_mvp_acceptance_journey, docs_neuroone_mvp_scope_mvp_definition, agents_demo_ready_definition, reports_progress_report_implemented_api_surface [EXTRACTED 1.00]
- **Per-Record Ownership Enforcement Pattern (404 masking, derived one hop up)** — docs_decisions_adr_001_ownership_violation_status_code_enumeration_resistance, docs_decisions_adr_002_visit_ownership_derivation_single_ownership_rule, docs_decisions_adr_002_visit_ownership_derivation_404_relabelling, docs_decisions_adr_002_visit_ownership_derivation_symptom_parent_check [EXTRACTED 1.00]
- **Provider Selects, System Resolves (traceability containment)** — docs_decisions_adr_003_ai_analysis_contract_and_provider_seam_resolve_evidence, docs_decisions_adr_005_live_llm_provider_system_authored_trend_basis_uuids, docs_decisions_adr_005_live_llm_provider_derived_category, docs_decisions_adr_005_live_llm_provider_livecandidatepayload [EXTRACTED 1.00]
- **Three Independently Swappable Provider Seams** — agents_ai_01_contract_real_provider_mocked, docs_neuroone_mvp_scope_ai_02a_live_llm, docs_neuroone_mvp_scope_ai_02b_real_retrieval_corpus, agents_scan_staging_seam, agents_provenance_pipeline_note [EXTRACTED 1.00]
- **Frontend Reconnection Gap** — reports_progress_report_frontend_not_connected, docs_report_01d_frontend_checklist_baseline_finding, frontend_checklist_build_checklist, readme_dashboard_not_started, reports_progress_report_milestone_connect_frontend [INFERRED 0.95]

## Communities (186 total, 45 thin omitted)

### Community 0 - "EntityNotFoundError"
Cohesion: 0.07
Nodes (96): str, Lifecycle of a clinical case. ANALYZED is written by the AI pipeline (AI-01),…, VisitStatus, Payload used to record a symptom against a visit., Payload used to partially update a symptom., SymptomCreate, SymptomUpdate, _as_utc() (+88 more)

### Community 1 - "UserRole"
Cohesion: 0.22
Nodes (30): str, UserRole, PatientUpdate, PhoneNumber, A patient phone number., Payload used to partially update a patient., _create_payload(), _patient() (+22 more)

### Community 2 - "new/page.tsx"
Cohesion: 0.06
Nodes (42): EMPTY_SYMPTOM, StepKey, STEPS, ADR-0006, IntakeInput, intakeSchema, splitList(), StepKey (+34 more)

### Community 3 - "test_ai_orchestrator.py"
Cohesion: 0.11
Nodes (41): What the LLM provider returns. Validated at the seam, so a real provider in…, ReasoningResult, _candidate(), _context(), _document(), _orchestrator(), Pipeline tests covering the AI test category (AGENTS.md section 10, TRD 12).…, AGENTS.md 8.1: never let simulated evidence read as clinically validated. (+33 more)

### Community 4 - "RetrievedDocument"
Cohesion: 0.11
Nodes (19): _document(), MockCondition, Deterministic stand-in for a retrieval corpus and a reasoning model. Everything…, A rule mapping clinical findings to a candidate condition., Return documents relevant to the query, most relevant first. Returning an empty…, MockLLMClient, Deterministic stand-in for the reasoning model. Scores the frozen condition…, Rank the condition rules against the supplied context and evidence. (+11 more)

### Community 5 - "visits.py"
Cohesion: 0.10
Nodes (46): get_scan_service(), get_visit_service(), Provide the configured scan service., Provide the configured visit service., add_symptom(), _analysis_page(), create_analysis(), delete_symptom() (+38 more)

### Community 6 - "test_report_renderer.py"
Cohesion: 0.19
Nodes (23): Render a complete, multi-page clinical report PDF. Raises whatever ReportLab…, render(), The patient/case identification FR-07 requires a report to carry., A citation as it must appear in the PDF (FR-05/06)., ReportEvidenceSnapshot, ReportPatientSnapshot, _evidence(), _finding() (+15 more)

### Community 7 - "v1/analysis.py"
Cohesion: 0.14
Nodes (23): get_analysis_service(), Provide the configured analysis service., create_report(), get_analysis(), list_reports(), Depends, ge, get (+15 more)

### Community 8 - "DiagnosisCandidate"
Cohesion: 0.11
Nodes (33): AnalysisResult, DiagnosisCandidate, An early-watch flag must point at the patient's own history. Note the…, Validated pipeline output, before persistence., One ranked possible condition. ``extra="forbid"`` is deliberate: a model that…, _candidate(), _evidence(), parametrize (+25 more)

### Community 9 - "test_ai_live_llm.py"
Cohesion: 0.05
Nodes (101): MockEvidenceRetriever, _normalize(), Deterministic stand-in for a literature retriever. Matches the query against a…, Keyword retriever over the frozen mock corpus., Return matching documents, most relevant first. An empty result is a legitimate…, What the orchestrator asks the retriever for., RetrievalQuery, _analyze() (+93 more)

### Community 10 - "get_db"
Cohesion: 0.10
Nodes (43): get_current_active_user(), get_current_user(), get_db(), get_patient_service(), Depends, Session, User, Reusable FastAPI dependencies for database and access control. (+35 more)

### Community 11 - "AuthService"
Cohesion: 0.14
Nodes (21): TokenPayload, AuthService, Hash a plaintext password., Validate an access token and return its payload., Validate the reset code and set a new password., Business logic for authentication operations., InvalidCredentialsError, InvalidOtpError (+13 more)

### Community 12 - "reset-password/page.tsx"
Cohesion: 0.09
Nodes (28): ForgotPasswordPage(), LoginForm(), handleOtpLogin(), handleSubmit(), validate(), ResetPasswordForm(), SignupPage(), VerifyOtpForm() (+20 more)

### Community 13 - "test_ai_staging.py"
Cohesion: 0.18
Nodes (23): Normalize Input + Build Clinical Context (TRD section 8, stages 1-2). This is…, Map a Visit and its live symptoms into the AI-facing shape., _to_context_visit(), ContextSymptom, A symptom as the AI layer sees it., The MRI scan attached to a visit, as the AI layer sees it. PHI-minimal like the…, ScanSummary, _context() (+15 more)

### Community 14 - "test_visits_api.py"
Cohesion: 0.15
Nodes (34): _client(), _db_override(), TestClient, Contract tests for the clinical case (visit) and symptom endpoints. Extends…, Only patient_id is exposed, so no endpoint can lazy-load per row., _symptom(), test_a_whitespace_only_observation_is_rejected(), test_add_symptom_returns_201() (+26 more)

### Community 15 - "Analysis"
Cohesion: 0.05
Nodes (79): Analysis, AnalysisEvidence, AnalysisFinding, FindingCategory, str, One ranked candidate condition. Decision support, never a definitive diagnosis:…, One citation supporting one ranked finding. Scoped to a finding rather than to…, Whether a ranked condition sits in the differential or is flagged early.… (+71 more)

### Community 16 - "test_analysis_api.py"
Cohesion: 0.15
Nodes (31): _analysis(), _client(), _db_override(), _evidence(), _finding(), TestClient, Contract tests for the analysis endpoints. Beyond the usual status/shape…, A consumer must be able to tell simulated evidence from live evidence. (+23 more)

### Community 17 - "types.ts"
Cohesion: 0.07
Nodes (36): analyses, PageParams, reports, ADR-0006, Analysis, Evidence, FindingCategory, Paginated (+28 more)

### Community 18 - "index.ts"
Cohesion: 0.03
Nodes (61): ArrowRight(), IconProps, Bell(), IconProps, Calendar(), IconProps, ChevronDown(), IconProps (+53 more)

### Community 19 - "build_backend_architecture_report.py"
Cohesion: 0.18
Nodes (31): Document, RGBColor, add_body(), add_bullets(), add_callout(), add_code(), add_cover(), add_field() (+23 more)

### Community 20 - "auth-provider.tsx"
Cohesion: 0.12
Nodes (24): VisitAnalysis(), downloadReport(), runAnalysis(), signOff(), AuthContext, AuthContextValue, AuthProvider(), persistToken() (+16 more)

### Community 21 - "PatientService"
Cohesion: 0.16
Nodes (19): PhoneNumber, PatientCreate, Payload used to create a patient., PatientService, Patient, Session, User, UUID (+11 more)

### Community 22 - "User"
Cohesion: 0.14
Nodes (21): User model definitions., User, Session, Symptom, UUID, Visit, Open a clinical case for a patient the caller owns. The patient id came from…, Retrieve a visit by ID. Ownership violations read as 404. (+13 more)

### Community 23 - "frontend/package.json"
Cohesion: 0.06
Nodes (29): autoprefixer, axios, eslint, eslint-config-next, js-cookie, lucide-react, next, postcss (+21 more)

### Community 24 - "StagingRequest"
Cohesion: 0.09
Nodes (29): EvidenceRetriever, ImagingStager, LLMClient, Protocol, The provider seam. This module is the entire surface AI-02 replaces. Everything…, Retrieves candidate literature for a clinical context. Implementations must…, Produces ranked candidate conditions from context plus evidence. The return…, Reason over the supplied context and evidence. (+21 more)

### Community 25 - "ReportRepository"
Cohesion: 0.17
Nodes (19): Session, UUID, Report persistence operations., Provide report-specific queries in addition to common CRUD., Return an analysis's reports, newest first., Count an analysis's active reports., ReportRepository, _engine() (+11 more)

### Community 26 - "Patient"
Cohesion: 0.14
Nodes (15): Patient, Patient model definitions., PatientRepository, Session, UUID, Patient persistence operations., Count active patients assigned to a doctor., Return the active patient with the given phone number, if any. (+7 more)

### Community 27 - "v1/auth.py"
Cohesion: 0.15
Nodes (28): get_auth_service(), Provide the configured authentication service., forgot_password(), login(), Depends, get, post, Session (+20 more)

### Community 28 - "Visit"
Cohesion: 0.11
Nodes (19): Enum, Persisted AI analysis, its ranked findings, and their citations. Naming is…, Immutable snapshot of a generated clinical report (ADR-004)., MRI scan metadata for a visit (ADR-006). The scan's bytes are not a column here…, One MRI scan attached to a visit. Attaches to the Visit, not the Patient…, Scan, Symptom model definitions., A neurological symptom recorded against a clinical case. (+11 more)

### Community 29 - "detect_trends"
Cohesion: 0.19
Nodes (21): detect_trends(), Detect per-symptom severity trends across a patient's visits. ``visits`` must…, Tests for cross-visit trend detection. A trend is what an early_watch flag…, symptoms: (name, severity) tuples., One visit per severity, 30 days apart, oldest-first., One observation is a snapshot, not a direction., Two rows on the same visit still span only one visit., _series() (+13 more)

### Community 30 - "LocalScanStorage"
Cohesion: 0.08
Nodes (35): Storage backends for artifacts that do not belong in the database., LocalScanStorage, Path, UUID, Storage for MRI scan bytes, outside the database (ADR-006 decision 5). A PDF…, Persist ``content`` and return its storage key., Filesystem-backed storage under a configured base directory. The concrete…, Tests for LocalScanStorage (ADR-006 decision 5). (+27 more)

### Community 31 - "analysis-findings.tsx"
Cohesion: 0.10
Nodes (16): AnalysisFindings(), BAND_TONE, BAR_TONE, FindingRow(), PointList(), AnalysisProvenance(), ADR-0006, IconProps (+8 more)

### Community 32 - "ReasoningRequest"
Cohesion: 0.09
Nodes (27): LiveCandidatePayload, LiveLLMClient, LiveReasoningPayload, Any, Client, Live reasoning over an OpenAI-compatible chat-completions endpoint. The AI-02…, The model's whole response. ``extra="forbid"`` is the structural half of the…, Reasoner backed by a real model behind ``LLMClient``. (+19 more)

### Community 33 - "r3f-canvas-scene.tsx"
Cohesion: 0.14
Nodes (10): R3fCanvasScene, FloatingParticles(), Particle, PARTICLES, StoryCard3D(), StoryCardProps, framer-motion, @react-three/drei (+2 more)

### Community 34 - "NeuroOne Design System"
Cohesion: 0.12
Nodes (20): 1. Brand identity, 3. Typography, 4. Login screen, 5. Open items, Brand Color Palette, Cormorant Garamond Fallback, IBM Plex Sans UI Font, Login Screen Spec (+12 more)

### Community 35 - "patient_visits.py"
Cohesion: 0.14
Nodes (23): alias, create_visit(), get_visit_history(), list_patient_visits(), Depends, ge, get, le (+15 more)

### Community 36 - "BaseRepository"
Cohesion: 0.16
Nodes (12): BaseRepository, Session, UUID, Generic repository providing reusable CRUD operations. This base repository…, Soft-delete an entity. Marks the entity as deleted by setting the `is_deleted`…, Check whether a record exists. Returns True if an active record with the given…, Create a new database record and persist it. Adds the model instance to the…, Retrieve a single record by its unique identifier. Returns the entity if it… (+4 more)

### Community 37 - "components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, registries (+11 more)

### Community 38 - "NeuroOne Frontend — Design System"
Cohesion: 0.09
Nodes (21): 10. Data layer, 11. Writing, 1. The idea, 2. Color, 3. Typography, 4. Shape and spacing, 5. Components, 6. Icons (+13 more)

### Community 39 - "BaseModel"
Cohesion: 0.06
Nodes (41): Fold a staging estimate into the same cited candidate shape. The stage never…, detect_stage_trend(), _direction(), datetime, UUID, Cross-visit symptom trend detection. This is the mechanism behind AGENTS.md…, Build history references for the matched worsening symptoms. Every reference…, Detect how an imaging-derived stage moved across a patient's visits. Mirrors… (+33 more)

### Community 40 - "Clinician Sign-Off Gates the Report"
Cohesion: 0.15
Nodes (14): ClinicalContext, Database-Free app/ai Package, Re-Running Analysis Creates a New Row, Multiple Immutable Reports per Analysis, Render Before Persist, ReportLab (Platypus) Renderer, ReportService, Clinical Context Leaves the Machine (+6 more)

### Community 41 - "PLAN — AI-02b: Curated Retrieval Corpus"
Cohesion: 0.09
Nodes (23): 10. Recommended Design, 11. Data / Schema Impact, 12. API / Contract Impact, 13. AI / RAG Impact, 14. Security / Privacy Impact, 15. Clinical Safety Impact, 16. Failure / Recovery Behavior, 18. Task Dependencies (+15 more)

### Community 42 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+13 more)

### Community 43 - "test_scan_api.py"
Cohesion: 0.33
Nodes (11): _client(), _db_override(), TestClient, Contract tests for the scan endpoints (ADR-006)., _scan(), test_getting_a_scan_on_a_scanless_visit_is_404(), test_getting_a_visits_scan_succeeds(), test_uploading_a_scan_returns_201_with_metadata() (+3 more)

### Community 44 - "cn"
Cohesion: 0.07
Nodes (40): DashboardPage(), filterEyebrow(), matchesFilter(), QueueRow(), REASON_STYLE, Signal(), summarise(), ADR-0006 (+32 more)

### Community 45 - "Base"
Cohesion: 0.22
Nodes (7): Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), Database engine and session configuration., Base, DeclarativeBase

### Community 46 - "SymptomRepository"
Cohesion: 0.23
Nodes (7): Session, UUID, Symptom persistence operations., Provide symptom-specific queries in addition to common CRUD operations., Return a visit's active symptoms in recording order., Count a visit's active symptoms., SymptomRepository

### Community 47 - "test_report_service.py"
Cohesion: 0.19
Nodes (27): One generated PDF report, snapshotting its source analysis. Never mutated after…, Report, _analysis(), _evidence(), _finding(), _patient(), Unit tests for ReportService. Two properties carry the weight, mirroring…, ADR-006 decision 6: sign-off gates the report. (+19 more)

### Community 48 - "VisitRepository"
Cohesion: 0.28
Nodes (17): Provide visit-specific queries in addition to common CRUD operations., VisitRepository, _engine(), Real-database tests for cross-visit history retrieval. These run against SQLite…, The loader criteria, not just the read path, must filter soft deletes., Regression guard for the N+1 the selectinload exists to prevent. One SELECT for…, test_get_by_patient_paginates_and_filters_by_status(), test_get_with_symptoms_hides_soft_deleted_visits() (+9 more)

### Community 49 - "ReportSnapshot (typed JSONB snapshot)"
Cohesion: 0.13
Nodes (19): Alembic Migration Policy, Team Repository Ownership Matrix, AIError Controlled Failure, analyses / analysis_findings / analysis_evidence Tables, Evidence Scoped to a Finding, Not a Report, EvidenceRef (narrowed wire shape), _resolve_evidence Orchestrator Stage, RetrievedDocument (+11 more)

### Community 50 - "NeuroOne Frontend — Redesign Checklist"
Cohesion: 0.11
Nodes (19): Confirmed Roles ADMIN and CLINICIAN, Users: Clinician and Administrator, Account & Settings, Admin, Admin Screens, Auth, Frontend Redesign Build Checklist, Clinical Input (+11 more)

### Community 51 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 52 - "Three Provenance States and pipeline_note"
Cohesion: 0.24
Nodes (10): Three Provenance States and pipeline_note, Scan Staging Provider Seam (SCAN-02), Mocked AI Credibility Risk, Analysis and Evidence Contract, AnalysisResponse, Stage Estimate as Top-Ranked Candidate Only, Diagnosis and Explainability Screens, Contributing Regions Visualization Has No API (+2 more)

### Community 53 - "test_auth_api.py"
Cohesion: 0.19
Nodes (18): Raised when a unique user identity is already registered., UserAlreadyExistsError, _client(), _db_override(), TestClient, Integration-style contract tests for authentication endpoints., test_admin_can_create_user_without_returning_password(), test_clinician_cannot_create_users() (+10 more)

### Community 54 - "ADR-006: MRI Becomes a Primary Input, With Symptoms as Context"
Cohesion: 0.18
Nodes (11): ADR-006: MRI Becomes a Primary Input, With Symptoms as Context, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Problem (+3 more)

### Community 55 - "Two Narrow Protocol Provider Seam"
Cohesion: 0.11
Nodes (22): DiagnosisCandidate, early_watch Category Derived From Trend Evidence, EvidenceRetriever Protocol, LLMClient Protocol, ReasoningResult, registry.build_providers(), trend_basis as a JSON Column, Two Narrow Protocol Provider Seam (+14 more)

### Community 56 - "Backend Tests Workflow"
Cohesion: 0.12
Nodes (17): Alembic Heads Check, Backend Tests Workflow, Pytest Run, Architectural Decision Records, Client to API to Service to Repository Layering, Transaction Boundary Ownership (open convention), alembic, pytest (+9 more)

### Community 57 - "ADR-006 MRI Primary With Symptoms as Context"
Cohesion: 0.12
Nodes (21): Security and Privacy Rules, V1 Scope Guard, python-multipart, APP-FLOW V1 Boundary, ADR-006 MRI Primary With Symptoms as Context, AI-02b Real Retrieval Corpus (deferred), Synthetic Demo Data Assumption, Revised Exclusions (+13 more)

### Community 58 - "ScanResponse"
Cohesion: 0.50
Nodes (3): Scan wire schema (ADR-006). No storage_key: that is an internal reference into…, A persisted scan's metadata, as returned by the API., ScanResponse

### Community 59 - "UserResponse"
Cohesion: 0.11
Nodes (20): Require the current user to have the administrator role., require_admin(), create_user(), Depends, post, Session, User, Administrator-only endpoints. (+12 more)

### Community 60 - "Ownership Violations Return 404, Not 403"
Cohesion: 0.14
Nodes (14): Enumeration Resistance for PHI-Adjacent Resources, Ownership Violations Return 404, Not 403, Server-Side Audit Logging of the Real Reason, 404 Re-Labelling / Identifier Masking, Symptom-Belongs-To-Visit Verification, AnalysisRepository.create_with_status, Failure Precedes the First Write, MAX_CONFIDENCE Ceiling of 0.92 (+6 more)

### Community 61 - "dependencies"
Cohesion: 0.11
Nodes (18): dependencies, axios, clsx, framer-motion, @hookform/resolvers, js-cookie, lucide-react, next (+10 more)

### Community 62 - "[id]/page.tsx"
Cohesion: 0.12
Nodes (25): PatientDetailPage(), VisitButton(), NewVisitPage(), onSubmit(), PatientsPage(), IconProps, Plus(), Card() (+17 more)

### Community 63 - "ReportService"
Cohesion: 0.11
Nodes (23): Clinical report contract (FR-07, ADR-004). ``ReportSnapshot`` is exactly what…, One clinical input as recorded for the visit (FR-03)., The clinical case the analysis was run against., Everything the renderer may draw on. Nothing else reaches the PDF., ReportSnapshot, ReportSymptomSnapshot, ReportVisitSnapshot, _age_years() (+15 more)

### Community 64 - "web-page/src/lib/api.ts"
Cohesion: 0.15
Nodes (8): api, ApiClient, ApiError, ApiResponse, extractApiError(), LoginResponse, OtpResponse, OtpVerifyResponse

### Community 65 - "AI Output Contract"
Cohesion: 0.13
Nodes (16): AI Output Contract, Clinical Safety Boundary, Definition of Done, Document Precedence, Sources of Truth, trend_basis Distinct from evidence, MVP Definition (locked), USP Framing as Vision Narrative (+8 more)

### Community 66 - "test_otp_service.py"
Cohesion: 0.23
Nodes (16): generate_and_send_otp(), _OtpEntry, Generates a 6-digit OTP, stores it, and emails it via Gmail SMTP., Checks a submitted OTP against the stored one. The code is only consumed…, verify_otp(), ExternalServiceError, parametrize, Tests for the OTP generation/verification helpers behind password reset. (+8 more)

### Community 67 - "MVP Acceptance Journey"
Cohesion: 0.11
Nodes (20): Demo-Ready Definition, bcrypt, passlib, python-jose, Definition of Demo-Ready MVP, FR-01 Authentication, FR-02 Patient Management, FR-03 Clinical Input (+12 more)

### Community 68 - "build_clinical_context"
Cohesion: 0.21
Nodes (21): _age_years(), build_clinical_context(), date, Whole years, so a date of birth never reaches the reasoning layer., Assemble the context the AI pipeline reasons over. ``prior_visits`` must be…, _patient(), Tests for the ORM -> ClinicalContext normalize stage. The PHI-minimization…, The current severity is part of the trajectory, not outside it. (+13 more)

### Community 69 - "create_access_token"
Cohesion: 0.21
Nodes (13): create_access_token(), decode_access_token(), hash_password(), Any, Password hashing and JSON Web Token helpers., Hash a plaintext password using the configured password context., Verify a plaintext password against a stored hash., Create a signed access token from the supplied claims. (+5 more)

### Community 70 - "Per-Record Ownership Check"
Cohesion: 0.13
Nodes (15): Coding Standards (type hints, PEP 8, services own business logic), Feature → API → Service → Repository → Model → Schema Flow, EntityNotFoundError, PatientService._authorize_access, Per-Record Ownership Check, require_roles Role-Level 403 Signaling, detect_trends Must Be Extended for Scan Metrics, Intake Splits Into New Patient and New Visit (+7 more)

### Community 71 - "interactive-pipeline-demo.tsx"
Cohesion: 0.42
Nodes (7): CASESHOTS, InteractivePipelineDemo(), SampleCase, DemoDiseaseLabel, DemoDiseaseStage, DemoRegion, RegionBars()

### Community 72 - "AnalysisOrchestrator"
Cohesion: 0.12
Nodes (21): AI orchestration. Layering rule: nothing in this package imports a repository…, AnalysisOrchestrator, The AI pipeline (TRD section 8, APP-FLOW section 5). Clinical Case -> Normalize…, Re-attach evidence from the orchestrator's own retrieved set. A provider names…, Drop uncited candidates, then rank and trim. A ranked condition without a…, Describe what actually produced this analysis. Derived from every provider that…, Execute the pipeline and return validated, ranked output., Runs the pipeline for one clinical context. (+13 more)

### Community 73 - "dashboard/layout.tsx"
Cohesion: 0.16
Nodes (10): DashboardLayout(), NAV_ITEMS, Activity(), IconProps, IconProps, Users(), sizes, SwitchButton() (+2 more)

### Community 74 - "ADR-003: AI Analysis Contract and the Mocked-Provider Seam"
Cohesion: 0.14
Nodes (14): Addendum: evidence-resolution correction (pre-`REPORT-01`), ADR-003: AI Analysis Contract and the Mocked-Provider Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact (+6 more)

### Community 75 - "REPORT-01D — Frontend Requirements & Backend Mapping Checklist"
Cohesion: 0.18
Nodes (14): 0. Baseline finding: this is not a "reconcile," it's mostly new pages, 1. Auth, 1A. Triage queue — the dashboard (ADR-006 decision 7), 2. Patients, 3. Clinical Case (Visit) + Symptoms, 3A. Scan intake (ADR-006 decisions 1, 2, 5), 4. AI Analysis + Differential Diagnosis + Evidence, 5. Clinician Sign-off → PDF Report (+6 more)

### Community 76 - "ADR-006-mri-primary-with-symptoms-as-context.md"
Cohesion: 0.27
Nodes (6): NeuroONE Agent Operating Contract, BUILD Mode, DEBUG Mode, PLAN Mode, TEST Mode, ADR-002 — Visit Ownership Derives From Parent Patient

### Community 78 - "ScanService"
Cohesion: 0.14
Nodes (14): Provide scan-specific queries in addition to common CRUD., ScanRepository, Scan, Session, UUID, Business logic for attaching an MRI scan to a visit (ADR-006). Authorization is…, Retrieve the scan attached to a visit, if any., Attaches, and retrieves, the one scan a visit may have. (+6 more)

### Community 79 - "ADR-004: Clinical Report Snapshot and Rendering"
Cohesion: 0.15
Nodes (13): ADR-004: Clinical Report Snapshot and Rendering, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 80 - "ADR-005: Live LLM Provider Behind the AI-01 Seam"
Cohesion: 0.15
Nodes (13): ADR-005: Live LLM Provider Behind the AI-01 Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 81 - "Current Development Status Table"
Cohesion: 0.18
Nodes (12): Repository Inspection Rules, REPORT-01D Contract Map, Authentication Complete, Backend APIs Complete (35 endpoints, 400 tests), Dashboard Not Started Against Real Data, Explainable AI in the API, Not the UI, Current Development Status Table, Status Stated Plainly (+4 more)

### Community 82 - "reports.py"
Cohesion: 0.24
Nodes (12): get_report_service(), Provide the configured report service., download_report_pdf(), get_report(), Depends, get, Session, UUID (+4 more)

### Community 83 - "devDependencies"
Cohesion: 0.11
Nodes (18): devDependencies, autoprefixer, eslint, eslint-config-next, jsdom, postcss, tailwindcss, @testing-library/dom (+10 more)

### Community 84 - "FR-04 Differential Diagnosis"
Cohesion: 0.13
Nodes (20): Early-Detection Design, Graphify Knowledge Graph Convention, Early-Detection Design (confirmed), FR-04 Differential Diagnosis, Suggested Build Order, MAX_CONFIDENCE 0.92 Ceiling, seed_demo_case.py Predates ADR-006, TriageEntry (+12 more)

### Community 85 - "test_patients_api.py"
Cohesion: 0.30
Nodes (14): _client(), _db_override(), _patient(), TestClient, Integration-style contract tests for patient endpoints. Covers the ownership-…, test_clinician_cannot_create_patient_for_another_doctor(), test_delete_on_other_doctors_patient_is_404(), test_delete_own_patient_returns_204() (+6 more)

### Community 86 - "Design boundaries"
Cohesion: 0.32
Nodes (8): pipeline_note Provenance Label, provider_mode, HYBRID_PIPELINE_NOTE, provider_mode Is Not Widened to hybrid, Clinical Safety Boundary (NeuroONE assists, never autonomously diagnoses), Provenance Stated per Analysis, Not per Environment, Stage Estimate as Top-Ranked Candidate, Never a Lone Verdict, Design boundaries

### Community 87 - "web-page/package.json"
Cohesion: 0.04
Nodes (45): dependencies, axios, js-cookie, lucide-react, next, react, react-dom, zod (+37 more)

### Community 88 - "test_report_api.py"
Cohesion: 0.19
Nodes (21): _client(), _db_override(), TestClient, Contract tests for the report endpoints. Beyond the usual status/shape…, ADR-006 decision 6: sign-off gates the report., AGENTS.md 8.2: not in the schema, not in API field naming., _report(), _snapshot() (+13 more)

### Community 89 - "get_triage_queue"
Cohesion: 0.06
Nodes (36): get_triage_service(), Provide the configured triage service., get_triage_queue(), Depends, ge, get, le, Query (+28 more)

### Community 90 - "NeuroOne Login Neurons Artwork v1"
Cohesion: 0.38
Nodes (10): NeuroOne Login Neurons Artwork v1, Dark Indigo Gradient Background, Decorative Non-Informational Asset Role, Dual Neuron Diagonal Composition, Neural Brand Identity Signal, Parked Login Design Reference, Portrait Split-Panel Login Slot, Golden Synapse Spark Focal Point (+2 more)

### Community 91 - "ValidationApplicationError"
Cohesion: 0.23
Nodes (15): Analysis persistence operations., Persist an analysis and advance the visit status in one transaction. Both…, ApplicationError, AuthenticationError, AuthorizationError, ConflictError, DatabaseError, InternalServerError (+7 more)

### Community 92 - "ReportFindingSnapshot"
Cohesion: 0.28
Nodes (12): _build_story(), _draw_footer(), _finding_label(), _p(), Render a ReportSnapshot into a complete clinical report PDF (ADR-004). A pure…, Escape Platypus markup and fall back for characters base14 can't render.…, _render_finding(), _safe() (+4 more)

### Community 93 - "neural-network.tsx"
Cohesion: 0.33
Nodes (6): Edge, EDGES, findNode(), NeuralNetwork(), Node, NODES

### Community 94 - "2. Color system"
Cohesion: 0.50
Nodes (4): 2. Color system, Brand (login screen, decorative panel, marketing surfaces), Product (dashboard, forms, tables, reports), Status colors (diagnosis output, case flags)

### Community 95 - "test_scan_service.py"
Cohesion: 0.34
Nodes (16): _deny_visit(), Unit tests for ScanService (ADR-006). Mirrors test_report_service.py's shape:…, ADR-006 decision 2: one scan per visit., _service(), test_a_second_scan_on_the_same_visit_is_a_conflict_and_cleans_up_storage(), test_an_empty_file_is_rejected(), test_an_oversized_file_is_rejected(), test_get_scan_on_a_scanless_visit_is_a_missing_scan() (+8 more)

### Community 96 - ".get_by_patient"
Cohesion: 0.26
Nodes (7): Session, UUID, Eager-load each visit's live symptoms in one extra query. selectinload rather…, Return an active visit with its live symptoms loaded., Return a patient's active visits, newest first., Count a patient's active visits., Return a patient's visit history ordered for trend comparison. This is the…

### Community 97 - "FR-07 Clinical Report"
Cohesion: 0.29
Nodes (8): pypdf, reportlab, FR-07 Clinical Report, Sign-Off Is a Gate, Not a Status, ReportResponse, Clinician Sign-off to PDF Report, Report Preview Page Has No API, Reports Screens

### Community 99 - "NeuroONE Frontend Redesign (parked)"
Cohesion: 0.25
Nodes (7): Sign in via OTP Button Replaces Google Sign-In, Account-flow handoff, Design implementation, Files in this change, NeuroONE Frontend Redesign (parked), Parked state, Preview

### Community 100 - "register_exception_handlers"
Cohesion: 0.19
Nodes (19): ErrorResponse, The standard shape returned for API errors., _application_handler(), _error_response(), http_exception_handler(), Exception, Global translation of domain exceptions into HTTP responses., Register every centralized domain-to-HTTP mapping. (+11 more)

### Community 101 - "UserService"
Cohesion: 0.14
Nodes (12): Enum, UserUpdate, BaseService, Shared service-layer infrastructure., Base service providing access to the repository., Public service-layer exports., Session, User (+4 more)

### Community 102 - ".verify_credentials"
Cohesion: 0.21
Nodes (7): Token, User, Authenticate a user and issue an access token directly (no OTP step)., Verify a plaintext password against a stored hash., Create an access token for a user., Verify credentials and OTP together, then issue an access token. This flow…, Validates username/email + password and returns the User, without issuing a…

### Community 103 - "test_deleted_at_timezone_migration.py"
Cohesion: 0.43
Nodes (6): _load_migration(), Regression tests for the deleted_at timezone migration., test_downgrade_restores_naive_timestamps(), test_migration_chains_from_case_01(), test_upgrade_uses_implicit_timezone_cast(), ModuleType

### Community 104 - "test_triage_api.py"
Cohesion: 0.27
Nodes (11): _client(), _db_override(), _entry(), TestClient, TriageEntry, Contract tests for the triage endpoint (ADR-006)., FR-04: no stat tile, no aggregate confidence number., test_an_entry_carries_no_field_that_frames_output_as_a_measurement() (+3 more)

### Community 105 - "likelihood_band_for"
Cohesion: 0.33
Nodes (5): likelihood_band_for(), Confidence-tiered output (section 8.3). This is what UI copy and the PDF should…, Derived from confidence, never read from the row., Tier a confidence value (AGENTS.md section 8.3). Derived, never stored: a…, computed_field

### Community 106 - "14056b8ec27d_create_scans.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create the scans table (ADR-006). No image bytes column: only the storage…, Drop the scans table., upgrade()

### Community 107 - "1f74d19af1b8_widen_patient_email_and_promote_phone_.py"
Cohesion: 0.40
Nodes (4): downgrade(), Widen patients.email to 255 chars and give patient_phones the standard…, Restore the legacy integer-keyed patient_phones and 20-char email., upgrade()

### Community 108 - "7544ad0b1ed6_add_analysis_sign_off.py"
Cohesion: 0.40
Nodes (4): downgrade(), Add clinician sign-off columns to analyses (ADR-006 decision 6). Both nullable…, Drop the sign-off columns., upgrade()

### Community 109 - "8e72c1f4a9b0_replace_legacy_user_roles.py"
Cohesion: 0.40
Nodes (4): downgrade(), Rename DOCTOR and remove the deferred RECEPTIONIST role safely., Restore the legacy role enum., upgrade()

### Community 110 - "a3c7be51d904_create_visits_and_symptoms.py"
Cohesion: 0.40
Nodes (4): downgrade(), Drop the symptom and visit tables, and the enum type they created., Create the clinical case (visit) and symptom tables. The composite (patient_id,…, upgrade()

### Community 111 - "b2b31bad27df_add_symptom_observation.py"
Cohesion: 0.40
Nodes (4): downgrade(), Add the clinician-entered observation field (FR-03). Nullable, so every…, Drop the observation column., upgrade()

### Community 112 - "b8d41e2f7c53_make_deleted_at_timezone_aware.py"
Cohesion: 0.40
Nodes (4): downgrade(), Widen deleted_at from timestamp to timestamptz. No USING clause, deliberately.…, Narrow deleted_at back to a naive timestamp. Symmetric with upgrade(): the…, upgrade()

### Community 113 - "c4e19a7b6d20_create_analyses_findings_and_evidence.py"
Cohesion: 0.40
Nodes (4): downgrade(), Drop the analysis tables and the enum type they created., Create the AI analysis tables. No drops. The abandoned Diagnosis and Rag stubs…, upgrade()

### Community 114 - "dcfbc7d5b2c9_create_reports.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create the reports table (ADR-004). No pdf_path and no binary PDF column: only…, Drop the reports table., upgrade()

### Community 116 - "scripts"
Cohesion: 0.29
Nodes (7): scripts, build, dev, lint, start, test, typecheck

### Community 117 - "ADR-007: Curated Retrieval Corpus Behind the AI-01 Seam"
Cohesion: 0.15
Nodes (13): ADR-007: Curated Retrieval Corpus Behind the AI-01 Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 118 - "web-page/src/lib/validation.ts"
Cohesion: 0.40
Nodes (4): LoginFormData, loginSchema, OtpFormData, otpSchema

### Community 119 - "Q: How are Alembic migrations and backend tests configured, and where should PR CI run pytest?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: How are Alembic migrations and backend tests configured, and where should PR CI run pytest?, Source Nodes

### Community 120 - "Q: The parallel AI-01 work is committed and pulled; plan our next work"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: The parallel AI-01 work is committed and pulled; plan our next work, Source Nodes

### Community 121 - "frontend/src/app/layout.tsx"
Cohesion: 0.25
Nodes (6): body, display, metadata, mono, ThemeProvider(), next-themes

### Community 124 - "17. Implementation Tasks"
Cohesion: 0.18
Nodes (11): 17. Implementation Tasks, TASK AI-02b-10 — Documentation reconciliation and graph refresh, TASK AI-02b-1 — Accept ADR-007, TASK AI-02b-2 — Corpus source schema and ingestion policy, TASK AI-02b-3 — `corpus_documents` model and migration, TASK AI-02b-4 — Corpus repository and search adapter, TASK AI-02b-5 — `CorpusEvidenceRetriever` and `CorpusSearch` protocol, TASK AI-02b-6 — Configuration, registry, orchestrator note, wiring, prompt (+3 more)

### Community 125 - "RAG Requirements"
Cohesion: 1.00
Nodes (3): RAG Requirements, FR-05 Literature Retrieval, FR-06 Explainability

### Community 130 - "get_user_service"
Cohesion: 0.40
Nodes (5): get_user_service(), Provide the configured user service., main(), Create NeuroONE's first administrator without a public endpoint., _value()

### Community 132 - "api service (FastAPI backend)"
Cohesion: 0.67
Nodes (3): api service (FastAPI backend), db service (postgres:16-alpine), Health-Gated Service Startup

### Community 133 - "Clinician Review Flow"
Cohesion: 0.67
Nodes (3): Evidence Flow (Retrieval → Ranking → Citation), Report Flow (Report Builder → PDF), Clinician Review Flow

### Community 154 - "app/main.py"
Cohesion: 0.25
Nodes (5): health(), get, root(), Compatibility entry point for running ``uvicorn main:app``., Regenerate backend-routes.json from the live FastAPI application. The file is…

### Community 155 - "FastAPI"
Cohesion: 0.29
Nodes (8): Top-level API router., Tests for soft-delete semantics and transactional failure handling., RepositoryRecord, _session(), test_create_rolls_back_and_raises_controlled_database_error(), test_mid_write_failure_persists_nothing_and_translates_database_error(), test_soft_deleted_records_are_hidden_unless_explicitly_requested(), FastAPI

### Community 156 - "AI-01 Contract-Real Provider-Mocked"
Cohesion: 0.25
Nodes (9): AI-01 Contract-Real Provider-Mocked, AI / RAG Pipeline, Locked Roadmap and Sequencing, httpx, ADR-005 Live LLM Provider, AI-02a Live LLM Provider, AI Phasing Decision, Investor/Stakeholder Demo Purpose (+1 more)

### Community 157 - "Error Handling Contract"
Cohesion: 0.25
Nodes (8): AI Failure Safety, Centralized Error Handling Rules, Non-Functional Requirements, 404 Ownership Masking, ApiError, Baseline Finding: Mostly New Pages, Error Handling Contract, extractApiError

### Community 159 - "vocabulary.test.ts"
Cohesion: 0.29
Nodes (5): EXCLUDED, ROOTS, RULES, SRC, ADR-0006

### Community 160 - "scan_repository.py"
Cohesion: 0.33
Nodes (4): Session, UUID, Scan persistence operations., Return the active scan attached to a visit, if any.

### Community 161 - "schemas/patient.py"
Cohesion: 0.40
Nodes (5): PatientBase, PatientResponse, Patient request and response schemas., Fields shared by patient request and response schemas., Public patient data returned by the API.

### Community 183 - "proxy.ts"
Cohesion: 0.40
Nodes (3): AUTH_PAGES, config, PROTECTED_PREFIXES

## Ambiguous Edges - Review These
- `Standard API Response Envelope` → `Assumed Backend API Contract`  [AMBIGUOUS]
  frontend/README.md · relation: conceptually_related_to
- `V1 Exclusions` → `MRI Upload + Prediction Polling`  [AMBIGUOUS]
  frontend/README.md · relation: conceptually_related_to
- `httpx` → `AI-02a Live LLM Provider`  [AMBIGUOUS]
  backend/requirements.txt · relation: conceptually_related_to
- `Golden Synapse Spark Focal Point` → `Neural Brand Identity Signal`  [AMBIGUOUS]
  frontend/web-page/public/images/neuroone-login-neurons-v1.png · relation: conceptually_related_to
- `Teal and Violet Accent Pair` → `Neural Brand Identity Signal`  [AMBIGUOUS]
  frontend/web-page/public/images/neuroone-login-neurons-v1.png · relation: conceptually_related_to

## Knowledge Gaps
- **514 isolated node(s):** `$schema`, `style`, `rsc`, `tsx`, `config` (+509 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1210 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **45 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Standard API Response Envelope` and `Assumed Backend API Contract`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `V1 Exclusions` and `MRI Upload + Prediction Polling`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `httpx` and `AI-02a Live LLM Provider`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Golden Synapse Spark Focal Point` and `Neural Brand Identity Signal`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Teal and Violet Accent Pair` and `Neural Brand Identity Signal`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `BaseModel` connect `BaseModel` to `EntityNotFoundError`, `UserRole`, `test_ai_orchestrator.py`, `visits.py`, `test_report_renderer.py`, `v1/analysis.py`, `DiagnosisCandidate`, `test_ai_live_llm.py`, `AuthService`, `test_ai_staging.py`, `Analysis`, `PatientService`, `User`, `StagingRequest`, `Patient`, `v1/auth.py`, `Visit`, `FastAPI`, `ReasoningRequest`, `schemas/patient.py`, `patient_visits.py`, `BaseRepository`, `Base`, `test_report_service.py`, `ScanResponse`, `UserResponse`, `ReportService`, `AnalysisOrchestrator`, `get_triage_queue`, `ReportFindingSnapshot`, `register_exception_handlers`, `UserService`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `EntityNotFoundError`, `UserRole`, `visits.py`, `v1/analysis.py`, `get_db`, `AuthService`, `test_visits_api.py`, `Analysis`, `test_analysis_api.py`, `v1/auth.py`, `Visit`, `LocalScanStorage`, `patient_visits.py`, `BaseModel`, `test_scan_api.py`, `test_report_service.py`, `test_auth_api.py`, `ReportService`, `UserRepository`, `ScanService`, `reports.py`, `test_patients_api.py`, `test_report_api.py`, `get_triage_queue`, `test_scan_service.py`, `UserService`, `test_triage_api.py`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._