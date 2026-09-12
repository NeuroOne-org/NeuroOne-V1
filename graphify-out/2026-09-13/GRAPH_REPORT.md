# Graph Report - NeuroOne-V1  (2026-09-13)

## Corpus Check
- 286 files · ~196,445 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3041 nodes · 7116 edges · 186 communities (133 shown, 46 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 656 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5d391b1c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_visit_service.py
- UserRole
- AnalysisRepository
- test_ai_orchestrator.py
- new/page.tsx
- get_current_active_user
- ReportService
- v1/analysis.py
- BaseModel
- test_ai_live_llm.py
- patients.py
- User
- reset-password/page.tsx
- build_providers
- EntityNotFoundError
- ReportRepository
- test_analysis_api.py
- types.ts
- index.ts
- build_backend_architecture_report.py
- auth-provider.tsx
- PatientService
- VisitService
- frontend/package.json
- test_ai_staging.py
- test_report_service.py
- Patient
- v1/auth.py
- Visit
- detect_trends
- dependencies.py
- test_report_renderer.py
- RetrievedDocument
- r3f-canvas-scene.tsx
- NeuroOne Design System
- patient_visits.py
- BaseRepository
- components.json
- NeuroOne Frontend — Design System
- PLAN — AI-02b: Curated Retrieval Corpus
- Clinician Sign-Off Gates the Report
- .create_with_status
- compilerOptions
- LocalScanStorage
- queue-filter-cards.tsx
- Base
- SymptomRepository
- seed_demo_case.py
- VisitStatus
- ReportSnapshot (typed JSONB snapshot)
- NeuroOne Frontend — Redesign Checklist
- compilerOptions
- FR-04 Differential Diagnosis
- test_auth_api.py
- ADR-006: MRI Becomes a Primary Input, With Symptoms as Context
- Two Narrow Protocol Provider Seam
- Backend Tests Workflow
- Security and Privacy Rules
- ScanResponse
- UserResponse
- Ownership Violations Return 404, Not 403
- dependencies
- [id]/page.tsx
- TriageService
- web-page/src/lib/api.ts
- AI-01 Contract-Real Provider-Mocked
- test_otp_service.py
- MVP Acceptance Journey
- test_triage_service.py
- create_access_token
- Per-Record Ownership Check
- interactive-pipeline-demo.tsx
- AnalysisOrchestrator
- RateLimitedError
- ADR-003: AI Analysis Contract and the Mocked-Provider Seam
- REPORT-01D — Frontend Requirements & Backend Mapping Checklist
- ADR-006-mri-primary-with-symptoms-as-context.md
- Analysis
- test_ai_mock_providers.py
- ADR-004: Clinical Report Snapshot and Rendering
- ADR-005: Live LLM Provider Behind the AI-01 Seam
- Current Development Status Table
- FastAPI
- devDependencies
- Triage Queue Contract
- get_db
- Design boundaries
- web-page/package.json
- test_report_api.py
- test_triage_api.py
- NeuroOne Login Neurons Artwork v1
- register_exception_handlers
- ReportFindingSnapshot
- neural-network.tsx
- 2. Color system
- UserRepository
- frontend/.eslintrc.json
- FR-07 Clinical Report
- web-page/next-env.d.ts
- NeuroONE Frontend Redesign (parked)
- _error_response
- UserService
- .verify_credentials
- test_deleted_at_timezone_migration.py
- web-page/.eslintrc.json
- get_triage_queue
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
- middleware.ts
- web-page/src/lib/validation.ts
- Q: How are Alembic migrations and backend tests configured, and where should PR CI run pytest?
- Q: The parallel AI-01 work is committed and pulled; plan our next work
- frontend/src/app/layout.tsx
- web-page/src/app/layout.tsx
- Password-strength
- test_patients_api.py
- RAG Requirements
- vocabulary.test.ts
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
- _clear_rate_limit_buckets
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
- AI Output Contract
- reports.py
- FindingCategory
- .__init__
- ADR-007: Curated Retrieval Corpus Behind the AI-01 Seam
- likelihood_band_for
- NeuroONE Agent Operating Contract
- Three Provenance States and pipeline_note
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
- ADR-006 MRI Primary With Symptoms as Context
- FR-01 Authentication
- web-page/src/app/login/page.tsx

## God Nodes (most connected - your core abstractions)
1. `User` - 129 edges
2. `EntityNotFoundError` - 92 edges
3. `UserRole` - 86 edges
4. `BaseModel` - 82 edges
5. `Visit` - 61 edges
6. `VisitService` - 58 edges
7. `cn()` - 54 edges
8. `AnalysisOrchestrator` - 53 edges
9. `get_db()` - 53 edges
10. `VisitStatus` - 52 edges

## Surprising Connections (you probably didn't know these)
- `MAX_CONFIDENCE 0.92 Ceiling` --semantically_similar_to--> `Clinical Safety Boundary`  [INFERRED] [semantically similar]
  docs/REPORT-01D-frontend-checklist.md → AGENTS.md
- `Contributing Regions Visualization Has No API` --semantically_similar_to--> `Mocked Staging Model Reads as Measurement`  [INFERRED] [semantically similar]
  frontend-checklist.md → reports/PROGRESS_REPORT.md
- `Mocked AI Credibility Risk` --semantically_similar_to--> `Mocked Staging Model Reads as Measurement`  [INFERRED] [semantically similar]
  docs/NEUROONE-MVP-SCOPE.md → reports/PROGRESS_REPORT.md
- `MRI Upload + Prediction Polling` --conceptually_related_to--> `V1 Exclusions`  [AMBIGUOUS]
  frontend/README.md → docs/PRD.md
- `Parked Design Reference (frontend/web-page)` --conceptually_related_to--> `Intake Splits Into New Patient and New Visit`  [INFERRED]
  frontend/web-page/README.md → docs/decisions/ADR-006-mri-primary-with-symptoms-as-context.md

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

## Communities (186 total, 46 thin omitted)

### Community 0 - "test_visit_service.py"
Cohesion: 0.08
Nodes (66): field_validator, Symptom request and response schemas., A whitespace-only observation is the same as no observation, rejected rather…, Fields shared by symptom request and response schemas., Payload used to record a symptom against a visit., Payload used to partially update a symptom., Public symptom data returned by the API., _reject_blank() (+58 more)

### Community 1 - "UserRole"
Cohesion: 0.22
Nodes (30): str, UserRole, PatientUpdate, PhoneNumber, A patient phone number., Payload used to partially update a patient., _create_payload(), _patient() (+22 more)

### Community 2 - "AnalysisRepository"
Cohesion: 0.25
Nodes (26): AnalysisRepository, Provide analysis-specific queries in addition to common CRUD., _analysis(), _engine(), _finding(), Real-database tests for analysis persistence. Run against SQLite because the…, AGENTS.md 8.5: a failure must not leave the record partly changed., Proves the .with_variant(JSON(), "sqlite") columns work as intended. (+18 more)

### Community 3 - "test_ai_orchestrator.py"
Cohesion: 0.11
Nodes (42): What the LLM provider returns. Validated at the seam, so a real provider in…, ReasoningResult, AIError, _candidate(), _context(), _document(), _orchestrator(), Pipeline tests covering the AI test category (AGENTS.md section 10, TRD 12).… (+34 more)

### Community 4 - "new/page.tsx"
Cohesion: 0.06
Nodes (46): EMPTY_SYMPTOM, StepKey, STEPS, ADR-0006, IntakeInput, intakeSchema, splitList(), StepKey (+38 more)

### Community 5 - "get_current_active_user"
Cohesion: 0.10
Nodes (49): get_current_active_user(), get_scan_service(), get_visit_service(), Provide the configured scan service., Return the current user only when the account is active., Provide the configured visit service., add_symptom(), _analysis_page() (+41 more)

### Community 6 - "ReportService"
Cohesion: 0.11
Nodes (23): Clinical report contract (FR-07, ADR-004). ``ReportSnapshot`` is exactly what…, One clinical input as recorded for the visit (FR-03)., The clinical case the analysis was run against., Everything the renderer may draw on. Nothing else reaches the PDF., ReportSnapshot, ReportSymptomSnapshot, ReportVisitSnapshot, _age_years() (+15 more)

### Community 7 - "v1/analysis.py"
Cohesion: 0.13
Nodes (25): get_analysis_service(), get_report_service(), Provide the configured analysis service., Provide the configured report service., create_report(), get_analysis(), list_reports(), Depends (+17 more)

### Community 8 - "BaseModel"
Cohesion: 0.05
Nodes (59): LiveReasoningPayload, The model's whole response. ``extra="forbid"`` is the structural half of the…, BaseModel, Base model definition., AnalysisCreateRequest, AnalysisResponse, AnalysisResult, DiagnosisCandidate (+51 more)

### Community 9 - "test_ai_live_llm.py"
Cohesion: 0.07
Nodes (82): MockEvidenceRetriever, Keyword retriever over the frozen mock corpus., model_validator, Settings, _analyze(), _candidates(), _context(), _evidence() (+74 more)

### Community 10 - "patients.py"
Cohesion: 0.11
Nodes (34): get_patient_service(), Provide the configured patient service., create_patient(), delete_patient(), get_patient(), list_patients(), _paginated_response(), delete (+26 more)

### Community 11 - "User"
Cohesion: 0.14
Nodes (24): User model definitions., User, TokenPayload, AuthService, Hash a plaintext password., Validate an access token and return its payload., Business logic for authentication operations., Validate the reset code and set a new password. Accepts only a code issued for… (+16 more)

### Community 12 - "reset-password/page.tsx"
Cohesion: 0.09
Nodes (28): ForgotPasswordPage(), LoginForm(), handleOtpLogin(), handleSubmit(), validate(), ResetPasswordForm(), SignupPage(), VerifyOtpForm() (+20 more)

### Community 13 - "build_providers"
Cohesion: 0.16
Nodes (16): EvidenceRetriever, ImagingStager, LLMClient, Protocol, The provider seam. This module is the entire surface AI-02 replaces. Everything…, Retrieves candidate literature for a clinical context. Implementations must…, Return documents relevant to the query, most relevant first. Returning an empty…, Produces ranked candidate conditions from context plus evidence. The return… (+8 more)

### Community 14 - "EntityNotFoundError"
Cohesion: 0.06
Nodes (95): EntityNotFoundError, Raised when a requested entity does not exist., _candidate(), _deny_visit(), _evidence(), Unit tests for AnalysisService. Two properties carry the weight here: that a…, AGENTS.md 8.4.4: source metadata must survive to persistence., The masked 404 must not disclose the visit or the patient behind it. (+87 more)

### Community 15 - "ReportRepository"
Cohesion: 0.17
Nodes (19): Session, UUID, Report persistence operations., Provide report-specific queries in addition to common CRUD., Return an analysis's reports, newest first., Count an analysis's active reports., ReportRepository, _engine() (+11 more)

### Community 16 - "test_analysis_api.py"
Cohesion: 0.15
Nodes (31): _analysis(), _client(), _db_override(), _evidence(), _finding(), TestClient, Contract tests for the analysis endpoints. Beyond the usual status/shape…, A consumer must be able to tell simulated evidence from live evidence. (+23 more)

### Community 17 - "types.ts"
Cohesion: 0.04
Nodes (57): AnalysisFindings(), BAND_TONE, BAR_TONE, FindingRow(), PointList(), AnalysisProvenance(), ADR-0006, ChevronDown() (+49 more)

### Community 18 - "index.ts"
Cohesion: 0.03
Nodes (69): NAV_ITEMS, Activity(), IconProps, IconProps, Bell(), IconProps, Calendar(), IconProps (+61 more)

### Community 19 - "build_backend_architecture_report.py"
Cohesion: 0.18
Nodes (31): Document, RGBColor, add_body(), add_bullets(), add_callout(), add_code(), add_cover(), add_field() (+23 more)

### Community 20 - "auth-provider.tsx"
Cohesion: 0.13
Nodes (22): VisitAnalysis(), downloadReport(), runAnalysis(), signOff(), onSubmit(), AuthContext, AuthContextValue, AuthProvider() (+14 more)

### Community 21 - "PatientService"
Cohesion: 0.11
Nodes (24): PhoneNumber, BaseService, Shared service-layer infrastructure., Base service providing access to the repository., Public service-layer exports., PatientService, Patient, Session (+16 more)

### Community 22 - "VisitService"
Cohesion: 0.13
Nodes (19): Session, Symptom, UUID, Visit, Open a clinical case for a patient the caller owns. The patient id came from…, Retrieve a visit by ID. Ownership violations read as 404., List a patient's visits, newest first., Return a patient's visit history ordered for trend comparison. This is the in-… (+11 more)

### Community 23 - "frontend/package.json"
Cohesion: 0.07
Nodes (27): autoprefixer, axios, eslint, eslint-config-next, js-cookie, lucide-react, next, postcss (+19 more)

### Community 24 - "test_ai_staging.py"
Cohesion: 0.12
Nodes (32): MockImagingStager, Deterministic stand-in for an MRI staging model (ADR-006). The stage estimate…, Deterministic stage estimate derived from the scan's checksum., Derive a stage, confidence and region breakdown from the checksum., Imaging staging contract (ADR-006). A third provider seam alongside the…, One anatomical region's weight in a staging estimate. Descriptive detail only.…, What the orchestrator hands the imaging staging provider. Deliberately narrow:…, RegionContribution (+24 more)

### Community 25 - "test_report_service.py"
Cohesion: 0.19
Nodes (27): One generated PDF report, snapshotting its source analysis. Never mutated after…, Report, _analysis(), _evidence(), _finding(), _patient(), Unit tests for ReportService. Two properties carry the weight, mirroring…, ADR-006 decision 6: sign-off gates the report. (+19 more)

### Community 26 - "Patient"
Cohesion: 0.09
Nodes (36): _age_years(), build_clinical_context(), date, Whole years, so a date of birth never reaches the reasoning layer., Assemble the context the AI pipeline reasons over. ``prior_visits`` must be…, Patient, Patient model definitions., PatientRepository (+28 more)

### Community 27 - "v1/auth.py"
Cohesion: 0.14
Nodes (29): get_auth_service(), Provide the configured authentication service., forgot_password(), login(), BackgroundTasks, Depends, get, post (+21 more)

### Community 28 - "Visit"
Cohesion: 0.14
Nodes (13): Immutable snapshot of a generated clinical report (ADR-004)., MRI scan metadata for a visit (ADR-006). The scan's bytes are not a column here…, One MRI scan attached to a visit. Attaches to the Visit, not the Patient…, Scan, Symptom model definitions., Clinical case / visit model definitions., A clinical case / visit belonging to a patient. Ownership is derived from the…, Visit (+5 more)

### Community 29 - "detect_trends"
Cohesion: 0.11
Nodes (33): Normalize Input + Build Clinical Context (TRD section 8, stages 1-2). This is…, Map a Visit and its live symptoms into the AI-facing shape., _to_context_visit(), detect_trends(), Normalized names of symptoms that are getting worse across visits. This is the…, Detect per-symptom severity trends across a patient's visits. ``visits`` must…, worsening_symptom_names(), ContextSymptom (+25 more)

### Community 30 - "dependencies.py"
Cohesion: 0.09
Nodes (21): Reusable FastAPI dependencies for database and access control., Session, UUID, Scan persistence operations., Provide scan-specific queries in addition to common CRUD., Return the active scan attached to a visit, if any., ScanRepository, Scan (+13 more)

### Community 31 - "test_report_renderer.py"
Cohesion: 0.19
Nodes (23): Render a complete, multi-page clinical report PDF. Raises whatever ReportLab…, render(), The patient/case identification FR-07 requires a report to carry., A citation as it must appear in the PDF (FR-05/06)., ReportEvidenceSnapshot, ReportPatientSnapshot, _evidence(), _finding() (+15 more)

### Community 32 - "RetrievedDocument"
Cohesion: 0.06
Nodes (38): _document(), MockCondition, Deterministic stand-in for a retrieval corpus and a reasoning model. Everything…, A rule mapping clinical findings to a candidate condition., Reason over the supplied context and evidence., LiveCandidatePayload, LiveLLMClient, Any (+30 more)

### Community 33 - "r3f-canvas-scene.tsx"
Cohesion: 0.14
Nodes (10): R3fCanvasScene, FloatingParticles(), Particle, PARTICLES, StoryCard3D(), StoryCardProps, framer-motion, @react-three/drei (+2 more)

### Community 34 - "NeuroOne Design System"
Cohesion: 0.12
Nodes (20): 1. Brand identity, 3. Typography, 4. Login screen, 5. Open items, Brand Color Palette, Cormorant Garamond Fallback, IBM Plex Sans UI Font, Login Screen Spec (+12 more)

### Community 35 - "patient_visits.py"
Cohesion: 0.11
Nodes (27): alias, create_visit(), get_visit_history(), list_patient_visits(), Depends, ge, get, le (+19 more)

### Community 36 - "BaseRepository"
Cohesion: 0.16
Nodes (12): BaseRepository, Session, UUID, Generic repository providing reusable CRUD operations. This base repository…, Soft-delete an entity. Marks the entity as deleted by setting the `is_deleted`…, Check whether a record exists. Returns True if an active record with the given…, Create a new database record and persist it. Adds the model instance to the…, Retrieve a single record by its unique identifier. Returns the entity if it… (+4 more)

### Community 37 - "components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, registries (+11 more)

### Community 38 - "NeuroOne Frontend — Design System"
Cohesion: 0.09
Nodes (21): 10. Data layer, 11. Writing, 1. The idea, 2. Color, 3. Typography, 4. Shape and spacing, 5. Components, 6. Icons (+13 more)

### Community 39 - "PLAN — AI-02b: Curated Retrieval Corpus"
Cohesion: 0.06
Nodes (34): 10. Recommended Design, 11. Data / Schema Impact, 12. API / Contract Impact, 13. AI / RAG Impact, 14. Security / Privacy Impact, 15. Clinical Safety Impact, 16. Failure / Recovery Behavior, 17. Implementation Tasks (+26 more)

### Community 40 - "Clinician Sign-Off Gates the Report"
Cohesion: 0.15
Nodes (14): ClinicalContext, Database-Free app/ai Package, Re-Running Analysis Creates a New Row, Multiple Immutable Reports per Analysis, Render Before Persist, ReportLab (Platypus) Renderer, ReportService, Clinical Context Leaves the Machine (+6 more)

### Community 41 - ".create_with_status"
Cohesion: 0.19
Nodes (9): Session, UUID, Return the most recent analysis for a visit, if any., Return each patient's most recent analysis, across all their visits. The triage…, Eager-load findings and their citations in two extra queries. Every read path…, Persist an analysis and advance the visit status in one transaction. Both…, Return an active analysis with its findings and citations loaded., Return a visit's analyses, newest first. (+1 more)

### Community 42 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+13 more)

### Community 43 - "LocalScanStorage"
Cohesion: 0.13
Nodes (14): Storage backends for artifacts that do not belong in the database., LocalScanStorage, Path, UUID, Storage for MRI scan bytes, outside the database (ADR-006 decision 5). A PDF…, Persist ``content`` and return its storage key., Filesystem-backed storage under a configured base directory. The concrete…, Tests for LocalScanStorage (ADR-006 decision 5). (+6 more)

### Community 44 - "queue-filter-cards.tsx"
Cohesion: 0.18
Nodes (8): Card(), CardProps, FilterCard, GLOW_SPRING, QueueFilter, QueueFilterCards(), TILT_SPRING, tint()

### Community 45 - "Base"
Cohesion: 0.22
Nodes (7): Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), Database engine and session configuration., Base, DeclarativeBase

### Community 46 - "SymptomRepository"
Cohesion: 0.23
Nodes (7): Session, UUID, Symptom persistence operations., Provide symptom-specific queries in addition to common CRUD operations., Return a visit's active symptoms in recording order., Count a visit's active symptoms., SymptomRepository

### Community 47 - "seed_demo_case.py"
Cohesion: 0.17
Nodes (19): DemoClinician, DemoPatient, DemoSymptom, DemoVisit, _flag_line(), Flags, main(), datetime (+11 more)

### Community 48 - "VisitStatus"
Cohesion: 0.12
Nodes (31): A neurological symptom recorded against a clinical case., Symptom, Enum, str, Lifecycle of a clinical case. ANALYZED is written by the AI pipeline (AI-01),…, VisitStatus, Session, UUID (+23 more)

### Community 49 - "ReportSnapshot (typed JSONB snapshot)"
Cohesion: 0.13
Nodes (19): Alembic Migration Policy, Team Repository Ownership Matrix, AIError Controlled Failure, analyses / analysis_findings / analysis_evidence Tables, Evidence Scoped to a Finding, Not a Report, EvidenceRef (narrowed wire shape), _resolve_evidence Orchestrator Stage, RetrievedDocument (+11 more)

### Community 50 - "NeuroOne Frontend — Redesign Checklist"
Cohesion: 0.11
Nodes (19): Confirmed Roles ADMIN and CLINICIAN, Users: Clinician and Administrator, Account & Settings, Admin, Admin Screens, Auth, Frontend Redesign Build Checklist, Clinical Input (+11 more)

### Community 51 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 52 - "FR-04 Differential Diagnosis"
Cohesion: 0.27
Nodes (10): Early-Detection Design, python-multipart, Early-Detection Design (confirmed), FR-04 Differential Diagnosis, FR-08 Scan Intake and Staging, MAX_CONFIDENCE 0.92 Ceiling, Stage Estimate as Top-Ranked Candidate Only, REPORT-01D Verification Criteria (+2 more)

### Community 53 - "test_auth_api.py"
Cohesion: 0.13
Nodes (28): LoginResponse, /auth/login's response. Either a token (AUTH_REQUIRE_OTP=false, or OTP already…, InvalidCredentialsError, Raised when supplied login credentials are invalid., _client(), _db_override(), TestClient, Integration-style contract tests for authentication endpoints. (+20 more)

### Community 54 - "ADR-006: MRI Becomes a Primary Input, With Symptoms as Context"
Cohesion: 0.18
Nodes (11): ADR-006: MRI Becomes a Primary Input, With Symptoms as Context, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Problem (+3 more)

### Community 55 - "Two Narrow Protocol Provider Seam"
Cohesion: 0.11
Nodes (22): DiagnosisCandidate, early_watch Category Derived From Trend Evidence, EvidenceRetriever Protocol, LLMClient Protocol, ReasoningResult, registry.build_providers(), trend_basis as a JSON Column, Two Narrow Protocol Provider Seam (+14 more)

### Community 56 - "Backend Tests Workflow"
Cohesion: 0.15
Nodes (14): Alembic Heads Check, Backend Tests Workflow, Pytest Run, Architectural Decision Records, Client to API to Service to Repository Layering, Transaction Boundary Ownership (open convention), alembic, pytest (+6 more)

### Community 57 - "Security and Privacy Rules"
Cohesion: 0.13
Nodes (16): AI Failure Safety, Centralized Error Handling Rules, Security and Privacy Rules, Non-Functional Requirements, 404 Ownership Masking, ApiError, Baseline Finding: Mostly New Pages, Error Handling Contract (+8 more)

### Community 58 - "ScanResponse"
Cohesion: 0.50
Nodes (3): Scan wire schema (ADR-006). No storage_key: that is an internal reference into…, A persisted scan's metadata, as returned by the API., ScanResponse

### Community 59 - "UserResponse"
Cohesion: 0.08
Nodes (27): Require the current user to have the administrator role., require_admin(), create_user(), Depends, post, Session, User, Administrator-only endpoints. (+19 more)

### Community 60 - "Ownership Violations Return 404, Not 403"
Cohesion: 0.14
Nodes (14): Enumeration Resistance for PHI-Adjacent Resources, Ownership Violations Return 404, Not 403, Server-Side Audit Logging of the Real Reason, 404 Re-Labelling / Identifier Masking, Symptom-Belongs-To-Visit Verification, AnalysisRepository.create_with_status, Failure Precedes the First Write, MAX_CONFIDENCE Ceiling of 0.92 (+6 more)

### Community 61 - "dependencies"
Cohesion: 0.11
Nodes (18): dependencies, axios, clsx, framer-motion, @hookform/resolvers, js-cookie, lucide-react, next (+10 more)

### Community 62 - "[id]/page.tsx"
Cohesion: 0.07
Nodes (53): DashboardLayout(), DashboardPage(), filterEyebrow(), matchesFilter(), QueueRow(), REASON_STYLE, Signal(), summarise() (+45 more)

### Community 63 - "TriageService"
Cohesion: 0.15
Nodes (13): Triage queue wire schema (ADR-006). No stat tiles: this is a ranked queue, not…, One patient's position in the triage queue. Not an ORM-backed response: there…, TriageEntry, _awaiting_sign_off(), _has_open_early_watch(), _has_worsening_trend(), Session, TriageEntry (+5 more)

### Community 64 - "web-page/src/lib/api.ts"
Cohesion: 0.15
Nodes (8): api, ApiClient, ApiError, ApiResponse, extractApiError(), LoginResponse, OtpResponse, OtpVerifyResponse

### Community 65 - "AI-01 Contract-Real Provider-Mocked"
Cohesion: 0.13
Nodes (16): AI-01 Contract-Real Provider-Mocked, AI / RAG Pipeline, Locked Roadmap and Sequencing, httpx, ADR-005 Live LLM Provider, AI-02a Live LLM Provider, AI-02b Real Retrieval Corpus (deferred), AI Phasing Decision (+8 more)

### Community 66 - "test_otp_service.py"
Cohesion: 0.18
Nodes (25): generate_and_send_otp(), _OtpEntry, OtpPurpose, Checks a submitted OTP against the one stored for this identity and purpose.…, Generates a 6-digit OTP scoped to `purpose`, stores it, and delivers it via…, Fire-and-forget wrapper meant for BackgroundTasks.add_task. Swallows delivery…, send_otp_background(), _store_key() (+17 more)

### Community 67 - "MVP Acceptance Journey"
Cohesion: 0.15
Nodes (13): Demo-Ready Definition, Definition of Demo-Ready MVP, FR-02 Patient Management, FR-03 Clinical Input, MVP Acceptance Journey, Product Goal Clinician Journey, AI-Owned analyzed Visit Status, Patient Endpoint Contract (+5 more)

### Community 68 - "test_triage_service.py"
Cohesion: 0.45
Nodes (12): _analysis(), _finding(), _patient(), Unit tests for TriageService (ADR-006 decision 7). The ranking order is the…, ADR-006: the scan-derived trend has no column of its own -- it is read back…, _service(), test_a_patient_with_no_analysis_sorts_last(), test_a_reviewed_analysis_is_not_awaiting_sign_off() (+4 more)

### Community 69 - "create_access_token"
Cohesion: 0.21
Nodes (13): create_access_token(), decode_access_token(), hash_password(), Any, Password hashing and JSON Web Token helpers., Hash a plaintext password using the configured password context., Verify a plaintext password against a stored hash., Create a signed access token from the supplied claims. (+5 more)

### Community 70 - "Per-Record Ownership Check"
Cohesion: 0.13
Nodes (15): Coding Standards (type hints, PEP 8, services own business logic), Feature → API → Service → Repository → Model → Schema Flow, EntityNotFoundError, PatientService._authorize_access, Per-Record Ownership Check, require_roles Role-Level 403 Signaling, detect_trends Must Be Extended for Scan Metrics, Intake Splits Into New Patient and New Visit (+7 more)

### Community 71 - "interactive-pipeline-demo.tsx"
Cohesion: 0.26
Nodes (9): ConfidenceDial(), ConfidenceDialProps, CASESHOTS, InteractivePipelineDemo(), SampleCase, DemoDiseaseLabel, DemoDiseaseStage, DemoRegion (+1 more)

### Community 72 - "AnalysisOrchestrator"
Cohesion: 0.07
Nodes (39): AI orchestration. Layering rule: nothing in this package imports a repository…, AnalysisOrchestrator, The AI pipeline (TRD section 8, APP-FLOW section 5). Clinical Case -> Normalize…, Re-attach evidence from the orchestrator's own retrieved set. A provider names…, Drop uncited candidates, then rank and trim. A ranked condition without a…, Describe what actually produced this analysis. Derived from every provider that…, Execute the pipeline and return validated, ranked output., Runs the pipeline for one clinical context. (+31 more)

### Community 73 - "RateLimitedError"
Cohesion: 0.15
Nodes (13): RateLimitedError, Raised when a caller exceeds an endpoint's request-rate limit., client_ip(), enforce(), Request, Records one attempt under `key` and raises RateLimitedError if that puts it…, Best-effort source IP for keying per-IP limits. Reads only…, _Window (+5 more)

### Community 74 - "ADR-003: AI Analysis Contract and the Mocked-Provider Seam"
Cohesion: 0.14
Nodes (14): Addendum: evidence-resolution correction (pre-`REPORT-01`), ADR-003: AI Analysis Contract and the Mocked-Provider Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact (+6 more)

### Community 75 - "REPORT-01D — Frontend Requirements & Backend Mapping Checklist"
Cohesion: 0.22
Nodes (14): 0. Baseline finding: this is not a "reconcile," it's mostly new pages, 1. Auth, 1A. Triage queue — the dashboard (ADR-006 decision 7), 2. Patients, 3. Clinical Case (Visit) + Symptoms, 3A. Scan intake (ADR-006 decisions 1, 2, 5), 4. AI Analysis + Differential Diagnosis + Evidence, 5. Clinician Sign-off → PDF Report (+6 more)

### Community 77 - "Analysis"
Cohesion: 0.14
Nodes (16): Analysis, AnalysisFinding, One ranked candidate condition. Decision support, never a definitive diagnosis:…, One run of the AI pipeline against one clinical case. Re-running creates a new…, Analysis persistence operations., AnalysisService, Analysis, Session (+8 more)

### Community 78 - "test_ai_mock_providers.py"
Cohesion: 0.10
Nodes (32): What the orchestrator asks the retriever for., RetrievalQuery, _analyze(), _context(), Tests for the mocked retriever and reasoner. Two properties matter most here.…, A stage estimate with no resolvable citation would be silently dropped., The fixture must not read as real literature., An empty result is a legitimate outcome, not an exception. (+24 more)

### Community 79 - "ADR-004: Clinical Report Snapshot and Rendering"
Cohesion: 0.15
Nodes (13): ADR-004: Clinical Report Snapshot and Rendering, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 80 - "ADR-005: Live LLM Provider Behind the AI-01 Seam"
Cohesion: 0.15
Nodes (13): ADR-005: Live LLM Provider Behind the AI-01 Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 81 - "Current Development Status Table"
Cohesion: 0.17
Nodes (13): Repository Inspection Rules, REPORT-01D Contract Map, AI Pipeline Contract Complete, Providers Simulated, Authentication Complete, Backend APIs Complete (35 endpoints, 400 tests), Dashboard Not Started Against Real Data, Explainable AI in the API, Not the UI, Current Development Status Table (+5 more)

### Community 82 - "FastAPI"
Cohesion: 0.29
Nodes (8): Top-level API router., Tests for soft-delete semantics and transactional failure handling., RepositoryRecord, _session(), test_create_rolls_back_and_raises_controlled_database_error(), test_mid_write_failure_persists_nothing_and_translates_database_error(), test_soft_deleted_records_are_hidden_unless_explicitly_requested(), FastAPI

### Community 83 - "devDependencies"
Cohesion: 0.11
Nodes (18): devDependencies, autoprefixer, eslint, eslint-config-next, jsdom, postcss, tailwindcss, @testing-library/dom (+10 more)

### Community 84 - "Triage Queue Contract"
Cohesion: 0.18
Nodes (14): Graphify Knowledge Graph Convention, Suggested Build Order, seed_demo_case.py Predates ADR-006, TriageEntry, Triage Queue Contract, Generate API Types From openapi.json, Triage Queue Screen, backend-routes.json OpenAPI Dump (+6 more)

### Community 85 - "get_db"
Cohesion: 0.18
Nodes (13): get_current_user(), get_db(), Depends, Session, User, Validate the bearer token and return its associated user., Create a dependency that permits only the supplied user roles., Require the current user to have the clinician role. (+5 more)

### Community 86 - "Design boundaries"
Cohesion: 0.32
Nodes (8): pipeline_note Provenance Label, provider_mode, HYBRID_PIPELINE_NOTE, provider_mode Is Not Widened to hybrid, Clinical Safety Boundary (NeuroONE assists, never autonomously diagnoses), Provenance Stated per Analysis, Not per Environment, Stage Estimate as Top-Ranked Candidate, Never a Lone Verdict, Design boundaries

### Community 87 - "web-page/package.json"
Cohesion: 0.04
Nodes (45): dependencies, axios, js-cookie, lucide-react, next, react, react-dom, zod (+37 more)

### Community 88 - "test_report_api.py"
Cohesion: 0.19
Nodes (21): _client(), _db_override(), TestClient, Contract tests for the report endpoints. Beyond the usual status/shape…, ADR-006 decision 6: sign-off gates the report., AGENTS.md 8.2: not in the schema, not in API field naming., _report(), _snapshot() (+13 more)

### Community 89 - "test_triage_api.py"
Cohesion: 0.27
Nodes (11): _client(), _db_override(), _entry(), TestClient, TriageEntry, Contract tests for the triage endpoint (ADR-006)., FR-04: no stat tile, no aggregate confidence number., test_an_entry_carries_no_field_that_frames_output_as_a_measurement() (+3 more)

### Community 90 - "NeuroOne Login Neurons Artwork v1"
Cohesion: 0.38
Nodes (10): NeuroOne Login Neurons Artwork v1, Dark Indigo Gradient Background, Decorative Non-Informational Asset Role, Dual Neuron Diagonal Composition, Neural Brand Identity Signal, Parked Login Design Reference, Portrait Split-Panel Login Slot, Golden Synapse Spark Focal Point (+2 more)

### Community 91 - "register_exception_handlers"
Cohesion: 0.23
Nodes (20): ErrorResponse, The standard shape returned for API errors., ApplicationError, AuthenticationError, ConflictError, DatabaseError, ExternalServiceError, InternalServerError (+12 more)

### Community 92 - "ReportFindingSnapshot"
Cohesion: 0.28
Nodes (12): _build_story(), _draw_footer(), _finding_label(), _p(), Render a ReportSnapshot into a complete clinical report PDF (ADR-004). A pure…, Escape Platypus markup and fall back for characters base14 can't render.…, _render_finding(), _safe() (+4 more)

### Community 93 - "neural-network.tsx"
Cohesion: 0.33
Nodes (6): Edge, EDGES, findNode(), NeuralNetwork(), Node, NODES

### Community 94 - "2. Color system"
Cohesion: 0.50
Nodes (4): 2. Color system, Brand (login screen, decorative panel, marketing surfaces), Product (dashboard, forms, tables, reports), Status colors (diagnosis output, case flags)

### Community 97 - "FR-07 Clinical Report"
Cohesion: 0.29
Nodes (8): pypdf, reportlab, FR-07 Clinical Report, Sign-Off Is a Gate, Not a Status, ReportResponse, Clinician Sign-off to PDF Report, Report Preview Page Has No API, Reports Screens

### Community 99 - "NeuroONE Frontend Redesign (parked)"
Cohesion: 0.25
Nodes (7): Sign in via OTP Button Replaces Google Sign-In, Account-flow handoff, Design implementation, Files in this change, NeuroONE Frontend Redesign (parked), Parked state, Preview

### Community 100 - "_error_response"
Cohesion: 0.30
Nodes (12): _error_response(), http_exception_handler(), Exception, Request, rate_limited_handler(), request_validation_error_handler(), unhandled_error_handler(), validation_error_handler() (+4 more)

### Community 101 - "UserService"
Cohesion: 0.23
Nodes (8): get_user_service(), Provide the configured user service., UserUpdate, Session, User, UUID, Business logic for user management., UserService

### Community 102 - ".verify_credentials"
Cohesion: 0.16
Nodes (9): Token, LoginResponse, Token, User, Authenticate a user and, per AUTH_REQUIRE_OTP, either issue a token directly or…, Verify a plaintext password against a stored hash., Create an access token for a user., Verify credentials and OTP together, then issue an access token. Accepts only a… (+1 more)

### Community 103 - "test_deleted_at_timezone_migration.py"
Cohesion: 0.43
Nodes (6): _load_migration(), Regression tests for the deleted_at timezone migration., test_downgrade_restores_naive_timestamps(), test_migration_chains_from_case_01(), test_upgrade_uses_implicit_timezone_cast(), ModuleType

### Community 104 - "web-page/.eslintrc.json"
Cohesion: 0.50
Nodes (3): extends, next/core-web-vitals, root

### Community 105 - "get_triage_queue"
Cohesion: 0.16
Nodes (13): get_triage_service(), Provide the configured triage service., get_triage_queue(), Depends, ge, get, le, Query (+5 more)

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

### Community 117 - "middleware.ts"
Cohesion: 0.40
Nodes (3): AUTH_PAGES, config, PROTECTED_PREFIXES

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

### Community 124 - "test_patients_api.py"
Cohesion: 0.28
Nodes (15): AuthorizationError, _client(), _db_override(), _patient(), TestClient, Integration-style contract tests for patient endpoints. Covers the ownership-…, test_clinician_cannot_create_patient_for_another_doctor(), test_delete_on_other_doctors_patient_is_404() (+7 more)

### Community 125 - "RAG Requirements"
Cohesion: 1.00
Nodes (3): RAG Requirements, FR-05 Literature Retrieval, FR-06 Explainability

### Community 130 - "vocabulary.test.ts"
Cohesion: 0.29
Nodes (5): EXCLUDED, ROOTS, RULES, SRC, ADR-0006

### Community 132 - "api service (FastAPI backend)"
Cohesion: 0.67
Nodes (3): api service (FastAPI backend), db service (postgres:16-alpine), Health-Gated Service Startup

### Community 133 - "Clinician Review Flow"
Cohesion: 0.67
Nodes (3): Evidence Flow (Retrieval → Ranking → Citation), Report Flow (Report Builder → PDF), Clinician Review Flow

### Community 141 - "_clear_rate_limit_buckets"
Cohesion: 0.40
Nodes (4): _clear_rate_limit_buckets(), Shared pytest configuration., The rate limiter (app/utils/rate_limit.py) is a process-global dict, so without…, fixture

### Community 154 - "app/main.py"
Cohesion: 0.25
Nodes (5): health(), get, root(), Compatibility entry point for running ``uvicorn main:app``., Regenerate backend-routes.json from the live FastAPI application. The file is…

### Community 155 - "AI Output Contract"
Cohesion: 0.13
Nodes (16): AI Output Contract, Clinical Safety Boundary, Definition of Done, Document Precedence, Sources of Truth, trend_basis Distinct from evidence, MVP Definition (locked), USP Framing as Vision Narrative (+8 more)

### Community 156 - "reports.py"
Cohesion: 0.27
Nodes (10): download_report_pdf(), get_report(), Depends, get, Session, UUID, Report item endpoints. Flat rather than nested under the analysis: a report id…, Retrieve one report's metadata. Ownership violations read as 404. (+2 more)

### Community 157 - "FindingCategory"
Cohesion: 0.25
Nodes (8): AnalysisEvidence, FindingCategory, Enum, str, Persisted AI analysis, its ranked findings, and their citations. Naming is…, One citation supporting one ranked finding. Scoped to a finding rather than to…, Whether a ranked condition sits in the differential or is flagged early.…, _evidence()

### Community 159 - "ADR-007: Curated Retrieval Corpus Behind the AI-01 Seam"
Cohesion: 0.15
Nodes (13): ADR-007: Curated Retrieval Corpus Behind the AI-01 Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 160 - "likelihood_band_for"
Cohesion: 0.33
Nodes (5): likelihood_band_for(), Confidence-tiered output (section 8.3). This is what UI copy and the PDF should…, Derived from confidence, never read from the row., Tier a confidence value (AGENTS.md section 8.3). Derived, never stored: a…, computed_field

### Community 161 - "NeuroONE Agent Operating Contract"
Cohesion: 0.70
Nodes (5): NeuroONE Agent Operating Contract, BUILD Mode, DEBUG Mode, PLAN Mode, TEST Mode

### Community 162 - "Three Provenance States and pipeline_note"
Cohesion: 0.38
Nodes (7): Three Provenance States and pipeline_note, Scan Staging Provider Seam (SCAN-02), Mocked AI Credibility Risk, Analysis and Evidence Contract, AnalysisResponse, Contributing Regions Visualization Has No API, Mocked Staging Model Reads as Measurement

### Community 183 - "ADR-006 MRI Primary With Symptoms as Context"
Cohesion: 0.38
Nodes (7): V1 Scope Guard, APP-FLOW V1 Boundary, ADR-006 MRI Primary With Symptoms as Context, Revised Exclusions, V1 Exclusions, Explicit Frontend Non-Goals, MRI Upload + Prediction Polling

### Community 184 - "FR-01 Authentication"
Cohesion: 0.33
Nodes (7): bcrypt, passlib, python-jose, FR-01 Authentication, Auth Endpoint Contract, No Self-Registration, Auth Screens

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
- **519 isolated node(s):** `extends`, `next/core-web-vitals`, `$schema`, `style`, `rsc` (+514 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1233 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **46 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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
- **Why does `BaseModel` connect `BaseModel` to `test_visit_service.py`, `UserRole`, `test_ai_orchestrator.py`, `ReportService`, `v1/analysis.py`, `patients.py`, `User`, `PatientService`, `test_ai_staging.py`, `test_report_service.py`, `Patient`, `v1/auth.py`, `Visit`, `detect_trends`, `FindingCategory`, `test_report_renderer.py`, `RetrievedDocument`, `patient_visits.py`, `BaseRepository`, `Base`, `VisitStatus`, `test_auth_api.py`, `ScanResponse`, `UserResponse`, `TriageService`, `AnalysisOrchestrator`, `Analysis`, `test_ai_mock_providers.py`, `FastAPI`, `register_exception_handlers`, `ReportFindingSnapshot`, `UserService`, `.verify_credentials`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `test_visit_service.py`, `UserRole`, `get_current_active_user`, `ReportService`, `v1/analysis.py`, `BaseModel`, `patients.py`, `EntityNotFoundError`, `test_analysis_api.py`, `PatientService`, `VisitService`, `test_report_service.py`, `v1/auth.py`, `Visit`, `reports.py`, `dependencies.py`, `patient_visits.py`, `seed_demo_case.py`, `test_auth_api.py`, `UserResponse`, `TriageService`, `test_triage_service.py`, `Analysis`, `test_report_api.py`, `test_triage_api.py`, `UserRepository`, `get_triage_queue`, `test_patients_api.py`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._