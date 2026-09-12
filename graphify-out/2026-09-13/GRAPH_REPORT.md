# Graph Report - NeuroOne-V1  (2026-09-12)

## Corpus Check
- 269 files · ~183,236 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2831 nodes · 6675 edges · 175 communities (123 shown, 45 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 603 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9ab89749`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_visit_service.py
- EntityNotFoundError
- test_analysis_repository.py
- test_ai_orchestrator.py
- RetrievedDocument
- get_db
- report_service.py
- v1/analysis.py
- DiagnosisCandidate
- test_ai_live_llm.py
- patients.py
- AuthService
- reset-password/page.tsx
- ReasoningRequest
- cn
- Analysis
- test_analysis_api.py
- endpoints.ts
- index.ts
- build_backend_architecture_report.py
- upload/page.tsx
- PatientService
- User
- frontend/package.json
- test_ai_staging.py
- Report
- Patient
- BaseModel
- Visit
- detect_trends
- LocalScanStorage
- test_analysis_service.py
- trends.py
- r3f-canvas-scene.tsx
- NeuroOne Design System
- patient_visits.py
- BaseRepository
- components.json
- NeuroOne Frontend — Design System
- build_clinical_context
- Clinician Sign-Off Gates the Report
- AnalysisRepository
- compilerOptions
- dependencies.py
- dashboard/page.tsx
- Base
- Symptom
- test_report_service.py
- VisitRepository
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
- VisitStatus
- Ownership Violations Return 404, Not 403
- dependencies
- [id]/page.tsx
- ReportService
- web-page/src/lib/api.ts
- AI Output Contract
- test_otp_service.py
- MVP Acceptance Journey
- FindingCategory
- create_access_token
- Per-Record Ownership Check
- interactive-pipeline-demo.tsx
- AnalysisOrchestrator
- dashboard/layout.tsx
- ADR-003: AI Analysis Contract and the Mocked-Provider Seam
- REPORT-01D — Frontend Requirements & Backend Mapping Checklist
- ADR-006-mri-primary-with-symptoms-as-context.md
- UserRepository
- test_scan_api.py
- ADR-004: Clinical Report Snapshot and Rendering
- ADR-005: Live LLM Provider Behind the AI-01 Seam
- Current Development Status Table
- reports.py
- devDependencies
- Triage Queue Contract
- get_current_user
- Design boundaries
- web-page/package.json
- FR-01 Authentication
- TriageService
- NeuroOne Login Neurons Artwork v1
- AI-01 Contract-Real Provider-Mocked
- ReportFindingSnapshot
- neural-network.tsx
- 2. Color system
- Three Provenance States and pipeline_note
- frontend/.eslintrc.json
- FR-07 Clinical Report
- web-page/next-env.d.ts
- NeuroONE Frontend Redesign (parked)
- ADR-006 MRI Primary With Symptoms as Context
- UserService
- .verify_credentials
- test_deleted_at_timezone_migration.py
- web-page/.eslintrc.json
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
- middleware.ts
- web-page/src/lib/validation.ts
- Q: How are Alembic migrations and backend tests configured, and where should PR CI run pytest?
- Q: The parallel AI-01 work is committed and pulled; plan our next work
- frontend/src/app/layout.tsx
- web-page/src/app/layout.tsx
- Password-strength
- seed
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
- TokenPayload
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

## God Nodes (most connected - your core abstractions)
1. `User` - 123 edges
2. `EntityNotFoundError` - 92 edges
3. `UserRole` - 82 edges
4. `BaseModel` - 81 edges
5. `Visit` - 57 edges
6. `VisitService` - 56 edges
7. `cn()` - 54 edges
8. `get_db()` - 53 edges
9. `AnalysisOrchestrator` - 52 edges
10. `VisitStatus` - 50 edges

## Surprising Connections (you probably didn't know these)
- `MAX_CONFIDENCE 0.92 Ceiling` --semantically_similar_to--> `Clinical Safety Boundary`  [INFERRED] [semantically similar]
  docs/REPORT-01D-frontend-checklist.md → AGENTS.md
- `MRI Upload + Prediction Polling` --conceptually_related_to--> `V1 Exclusions`  [AMBIGUOUS]
  frontend/README.md → docs/PRD.md
- `Parked Design Reference (frontend/web-page)` --conceptually_related_to--> `Intake Splits Into New Patient and New Visit`  [INFERRED]
  frontend/web-page/README.md → docs/decisions/ADR-006-mri-primary-with-symptoms-as-context.md
- `404 Ownership Masking` --semantically_similar_to--> `Security and Privacy Rules`  [INFERRED] [semantically similar]
  docs/REPORT-01D-frontend-checklist.md → AGENTS.md
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

## Communities (175 total, 45 thin omitted)

### Community 0 - "test_visit_service.py"
Cohesion: 0.06
Nodes (74): MessageResponse, PaginatedResponse, Schemas shared across application features., Generic response wrapper for paginated collection endpoints., A simple response containing a human-readable message., Public schema exports., field_validator, Symptom request and response schemas. (+66 more)

### Community 1 - "EntityNotFoundError"
Cohesion: 0.05
Nodes (102): Enum, str, UserRole, PatientUpdate, PhoneNumber, A patient phone number., Payload used to partially update a patient., EntityNotFoundError (+94 more)

### Community 2 - "test_analysis_repository.py"
Cohesion: 0.23
Nodes (26): AnalysisEvidence, One citation supporting one ranked finding. Scoped to a finding rather than to…, _analysis(), _engine(), _evidence(), _finding(), Real-database tests for analysis persistence. Run against SQLite because the…, AGENTS.md 8.5: a failure must not leave the record partly changed. (+18 more)

### Community 3 - "test_ai_orchestrator.py"
Cohesion: 0.11
Nodes (42): What the LLM provider returns. Validated at the seam, so a real provider in…, ReasoningResult, AIError, _candidate(), _context(), _document(), _orchestrator(), Pipeline tests covering the AI test category (AGENTS.md section 10, TRD 12).… (+34 more)

### Community 4 - "RetrievedDocument"
Cohesion: 0.08
Nodes (24): _document(), MockCondition, Deterministic stand-in for a retrieval corpus and a reasoning model. Everything…, A rule mapping clinical findings to a candidate condition., Return documents relevant to the query, most relevant first. Returning an empty…, MockLLMClient, Fold a staging estimate into the same cited candidate shape. The stage never…, Rank the condition rules against the supplied context and evidence. (+16 more)

### Community 5 - "get_db"
Cohesion: 0.09
Nodes (53): get_analysis_service(), get_current_active_user(), get_db(), Provide the configured analysis service., Return the current user only when the account is active., Provide a database session and always close it after the request., add_symptom(), _analysis_page() (+45 more)

### Community 6 - "report_service.py"
Cohesion: 0.12
Nodes (34): Render a complete, multi-page clinical report PDF. Raises whatever ReportLab…, render(), Clinical report contract (FR-07, ADR-004). ``ReportSnapshot`` is exactly what…, The patient/case identification FR-07 requires a report to carry., One clinical input as recorded for the visit (FR-03)., The clinical case the analysis was run against., A citation as it must appear in the PDF (FR-05/06)., Everything the renderer may draw on. Nothing else reaches the PDF. (+26 more)

### Community 7 - "v1/analysis.py"
Cohesion: 0.09
Nodes (30): Top-level API router., create_report(), get_analysis(), list_reports(), Depends, ge, get, le (+22 more)

### Community 8 - "DiagnosisCandidate"
Cohesion: 0.10
Nodes (35): AnalysisResult, DiagnosisCandidate, An early-watch flag must point at the patient's own history. Note the…, Validated pipeline output, before persistence., A pointer into the patient's OWN visit history. Distinct from ``EvidenceRef``,…, One ranked possible condition. ``extra="forbid"`` is deliberate: a model that…, TrendBasisRef, _candidate() (+27 more)

### Community 9 - "test_ai_live_llm.py"
Cohesion: 0.05
Nodes (101): MockEvidenceRetriever, _normalize(), Deterministic stand-in for a literature retriever. Matches the query against a…, Keyword retriever over the frozen mock corpus., Return matching documents, most relevant first. An empty result is a legitimate…, What the orchestrator asks the retriever for., RetrievalQuery, _analyze() (+93 more)

### Community 10 - "patients.py"
Cohesion: 0.11
Nodes (34): get_patient_service(), Provide the configured patient service., create_patient(), delete_patient(), get_patient(), list_patients(), _paginated_response(), delete (+26 more)

### Community 11 - "AuthService"
Cohesion: 0.10
Nodes (32): Administrator-only endpoints., User request and response schemas., UserBase, UserCreate, UserResponse, AuthService, Session, Hash a plaintext password. (+24 more)

### Community 12 - "reset-password/page.tsx"
Cohesion: 0.09
Nodes (28): ForgotPasswordPage(), LoginForm(), handleOtpLogin(), handleSubmit(), validate(), ResetPasswordForm(), SignupPage(), VerifyOtpForm() (+20 more)

### Community 13 - "ReasoningRequest"
Cohesion: 0.07
Nodes (37): AI orchestration. Layering rule: nothing in this package imports a repository…, The AI pipeline (TRD section 8, APP-FLOW section 5). Clinical Case -> Normalize…, EvidenceRetriever, ImagingStager, LLMClient, Protocol, The provider seam. This module is the entire surface AI-02 replaces. Everything…, Retrieves candidate literature for a clinical context. Implementations must… (+29 more)

### Community 14 - "cn"
Cohesion: 0.08
Nodes (26): Signal(), AnalysisFindings(), BAND_TONE, BAR_TONE, FindingRow(), PointList(), ConfidenceDial(), ConfidenceDialProps (+18 more)

### Community 15 - "Analysis"
Cohesion: 0.12
Nodes (19): Analysis, One run of the AI pipeline against one clinical case. Re-running creates a new…, AnalysisService, Analysis, Session, UUID, Business logic for AI analysis of a clinical case. The ordering in…, Run the AI pipeline for a visit and persist the result. Ownership violations… (+11 more)

### Community 16 - "test_analysis_api.py"
Cohesion: 0.15
Nodes (31): _analysis(), _client(), _db_override(), _evidence(), _finding(), TestClient, Contract tests for the analysis endpoints. Beyond the usual status/shape…, A consumer must be able to tell simulated evidence from live evidence. (+23 more)

### Community 17 - "endpoints.ts"
Cohesion: 0.09
Nodes (35): ADR-0006, AuthContext, AuthContextValue, AuthProvider(), persistToken(), NOTE: the backend exposes no public registration route -- accounts, api, TOKEN_COOKIE (+27 more)

### Community 18 - "index.ts"
Cohesion: 0.03
Nodes (57): ArrowRight(), IconProps, Bell(), IconProps, Calendar(), IconProps, ChevronRight(), IconProps (+49 more)

### Community 19 - "build_backend_architecture_report.py"
Cohesion: 0.18
Nodes (31): Document, RGBColor, add_body(), add_bullets(), add_callout(), add_code(), add_cover(), add_field() (+23 more)

### Community 20 - "upload/page.tsx"
Cohesion: 0.06
Nodes (39): VisitAnalysis(), downloadReport(), runAnalysis(), signOff(), IntakeInput, intakeSchema, splitList(), StepKey (+31 more)

### Community 21 - "PatientService"
Cohesion: 0.16
Nodes (17): PhoneNumber, PatientService, Patient, Session, User, UUID, Business logic for patient management., List patients, scoped to the caller's role. CLINICIAN always sees only their… (+9 more)

### Community 22 - "User"
Cohesion: 0.14
Nodes (21): User model definitions., User, Session, Symptom, UUID, Visit, Open a clinical case for a patient the caller owns. The patient id came from…, Retrieve a visit by ID. Ownership violations read as 404. (+13 more)

### Community 23 - "frontend/package.json"
Cohesion: 0.08
Nodes (23): autoprefixer, axios, eslint, eslint-config-next, js-cookie, lucide-react, next, postcss (+15 more)

### Community 24 - "test_ai_staging.py"
Cohesion: 0.10
Nodes (39): Normalize Input + Build Clinical Context (TRD section 8, stages 1-2). This is…, Map a Visit and its live symptoms into the AI-facing shape., _to_context_visit(), MockImagingStager, Deterministic stand-in for an MRI staging model (ADR-006). The stage estimate…, Deterministic stage estimate derived from the scan's checksum., Derive a stage, confidence and region breakdown from the checksum., ContextSymptom (+31 more)

### Community 25 - "Report"
Cohesion: 0.16
Nodes (21): One generated PDF report, snapshotting its source analysis. Never mutated after…, Report, Session, UUID, Report persistence operations., Provide report-specific queries in addition to common CRUD., Return an analysis's reports, newest first., Count an analysis's active reports. (+13 more)

### Community 26 - "Patient"
Cohesion: 0.14
Nodes (15): Patient, Patient model definitions., PatientRepository, Session, UUID, Patient persistence operations., Count active patients assigned to a doctor., Return the active patient with the given phone number, if any. (+7 more)

### Community 27 - "BaseModel"
Cohesion: 0.13
Nodes (32): LiveReasoningPayload, The model's whole response. ``extra="forbid"`` is the structural half of the…, get_auth_service(), Provide the configured authentication service., forgot_password(), login(), Depends, get (+24 more)

### Community 28 - "Visit"
Cohesion: 0.21
Nodes (10): AnalysisFinding, Enum, Persisted AI analysis, its ranked findings, and their citations. Naming is…, One ranked candidate condition. Decision support, never a definitive diagnosis:…, Immutable snapshot of a generated clinical report (ADR-004)., MRI scan metadata for a visit (ADR-006). The scan's bytes are not a column here…, Symptom model definitions., Clinical case / visit model definitions. (+2 more)

### Community 29 - "detect_trends"
Cohesion: 0.15
Nodes (26): detect_trends(), normalize_symptom_name(), Normalized names of symptoms that are getting worse across visits. This is the…, Group key for a symptom, so "Tremor" and "tremor " are one series., Detect per-symptom severity trends across a patient's visits. ``visits`` must…, worsening_symptom_names(), Tests for cross-visit trend detection. A trend is what an early_watch flag…, symptoms: (name, severity) tuples. (+18 more)

### Community 30 - "LocalScanStorage"
Cohesion: 0.13
Nodes (14): Storage backends for artifacts that do not belong in the database., LocalScanStorage, Path, UUID, Storage for MRI scan bytes, outside the database (ADR-006 decision 5). A PDF…, Persist ``content`` and return its storage key., Filesystem-backed storage under a configured base directory. The concrete…, Tests for LocalScanStorage (ADR-006 decision 5). (+6 more)

### Community 31 - "test_analysis_service.py"
Cohesion: 0.21
Nodes (32): _candidate(), _deny_visit(), _evidence(), Unit tests for AnalysisService. Two properties carry the weight here: that a…, AGENTS.md 8.4.4: source metadata must survive to persistence., The masked 404 must not disclose the visit or the patient behind it., Idempotent: no amendment flow exists yet to revoke a prior sign-off., _result() (+24 more)

### Community 32 - "trends.py"
Cohesion: 0.11
Nodes (24): detect_stage_trend(), _direction(), datetime, UUID, Cross-visit symptom trend detection. This is the mechanism behind AGENTS.md…, Build history references for the matched worsening symptoms. Every reference…, Detect how an imaging-derived stage moved across a patient's visits. Mirrors…, Build history references for a worsening imaging-derived stage trend. Mirrors… (+16 more)

### Community 33 - "r3f-canvas-scene.tsx"
Cohesion: 0.14
Nodes (10): R3fCanvasScene, FloatingParticles(), Particle, PARTICLES, StoryCard3D(), StoryCardProps, framer-motion, @react-three/drei (+2 more)

### Community 34 - "NeuroOne Design System"
Cohesion: 0.12
Nodes (20): 1. Brand identity, 3. Typography, 4. Login screen, 5. Open items, Brand Color Palette, Cormorant Garamond Fallback, IBM Plex Sans UI Font, Login Screen Spec (+12 more)

### Community 35 - "patient_visits.py"
Cohesion: 0.15
Nodes (23): alias, get_visit_service(), Provide the configured visit service., create_visit(), get_visit_history(), list_patient_visits(), Depends, ge (+15 more)

### Community 36 - "BaseRepository"
Cohesion: 0.05
Nodes (73): health(), get, root(), BaseRepository, Session, UUID, Generic repository providing reusable CRUD operations. This base repository…, Soft-delete an entity. Marks the entity as deleted by setting the `is_deleted`… (+65 more)

### Community 37 - "components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, registries (+11 more)

### Community 38 - "NeuroOne Frontend — Design System"
Cohesion: 0.09
Nodes (21): 10. Data layer, 11. Writing, 1. The idea, 2. Color, 3. Typography, 4. Shape and spacing, 5. Components, 6. Icons (+13 more)

### Community 39 - "build_clinical_context"
Cohesion: 0.21
Nodes (21): _age_years(), build_clinical_context(), date, Whole years, so a date of birth never reaches the reasoning layer., Assemble the context the AI pipeline reasons over. ``prior_visits`` must be…, _patient(), Tests for the ORM -> ClinicalContext normalize stage. The PHI-minimization…, The current severity is part of the trajectory, not outside it. (+13 more)

### Community 40 - "Clinician Sign-Off Gates the Report"
Cohesion: 0.15
Nodes (14): ClinicalContext, Database-Free app/ai Package, Re-Running Analysis Creates a New Row, Multiple Immutable Reports per Analysis, Render Before Persist, ReportLab (Platypus) Renderer, ReportService, Clinical Context Leaves the Machine (+6 more)

### Community 41 - "AnalysisRepository"
Cohesion: 0.16
Nodes (13): AnalysisRepository, Session, UUID, Analysis persistence operations., Return the most recent analysis for a visit, if any., Return each patient's most recent analysis, across all their visits. The triage…, Provide analysis-specific queries in addition to common CRUD., Eager-load findings and their citations in two extra queries. Every read path… (+5 more)

### Community 42 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+13 more)

### Community 43 - "dependencies.py"
Cohesion: 0.09
Nodes (23): get_scan_service(), Reusable FastAPI dependencies for database and access control., Provide the configured scan service., One MRI scan attached to a visit. Attaches to the Visit, not the Patient…, Scan, Session, UUID, Scan persistence operations. (+15 more)

### Community 44 - "dashboard/page.tsx"
Cohesion: 0.09
Nodes (24): DashboardPage(), filterEyebrow(), matchesFilter(), QueueRow(), summarise(), Clock(), IconProps, IconProps (+16 more)

### Community 45 - "Base"
Cohesion: 0.22
Nodes (7): Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), Database engine and session configuration., Base, DeclarativeBase

### Community 46 - "Symptom"
Cohesion: 0.12
Nodes (15): A neurological symptom recorded against a clinical case., Symptom, Session, UUID, Symptom persistence operations., Provide symptom-specific queries in addition to common CRUD operations., Return a visit's active symptoms in recording order., Count a visit's active symptoms. (+7 more)

### Community 47 - "test_report_service.py"
Cohesion: 0.20
Nodes (25): _analysis(), _evidence(), _finding(), _patient(), Unit tests for ReportService. Two properties carry the weight, mirroring…, ADR-006 decision 6: sign-off gates the report., The masked 404 must not disclose the analysis behind it., _service() (+17 more)

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

### Community 52 - "FR-04 Differential Diagnosis"
Cohesion: 0.27
Nodes (10): Early-Detection Design, python-multipart, Early-Detection Design (confirmed), FR-04 Differential Diagnosis, FR-08 Scan Intake and Staging, MAX_CONFIDENCE 0.92 Ceiling, Stage Estimate as Top-Ranked Candidate Only, REPORT-01D Verification Criteria (+2 more)

### Community 53 - "test_auth_api.py"
Cohesion: 0.22
Nodes (16): _client(), _db_override(), TestClient, Integration-style contract tests for authentication endpoints., test_admin_can_create_user_without_returning_password(), test_clinician_cannot_create_users(), test_duplicate_user_is_conflict(), test_expired_token_returns_controlled_401() (+8 more)

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

### Community 59 - "VisitStatus"
Cohesion: 0.17
Nodes (12): Enum, str, Lifecycle of a clinical case. ANALYZED is written by the AI pipeline (AI-01),…, VisitStatus, Session, UUID, Clinical case / visit persistence operations., Eager-load each visit's live symptoms in one extra query. selectinload rather… (+4 more)

### Community 60 - "Ownership Violations Return 404, Not 403"
Cohesion: 0.14
Nodes (14): Enumeration Resistance for PHI-Adjacent Resources, Ownership Violations Return 404, Not 403, Server-Side Audit Logging of the Real Reason, 404 Re-Labelling / Identifier Masking, Symptom-Belongs-To-Visit Verification, AnalysisRepository.create_with_status, Failure Precedes the First Write, MAX_CONFIDENCE Ceiling of 0.92 (+6 more)

### Community 61 - "dependencies"
Cohesion: 0.11
Nodes (18): dependencies, axios, clsx, framer-motion, @hookform/resolvers, js-cookie, lucide-react, next (+10 more)

### Community 62 - "[id]/page.tsx"
Cohesion: 0.11
Nodes (29): PatientDetailPage(), VisitButton(), PatientsPage(), ChevronLeft(), IconProps, Card(), CardBody(), CardHeader() (+21 more)

### Community 63 - "ReportService"
Cohesion: 0.18
Nodes (12): Report, Session, UUID, Build, render, and persist a new report for an analysis. Render-before-persist…, Retrieve one report by ID. The caller named only the report, so an…, List an analysis's reports, newest first., Re-render a report's PDF bytes from its immutable snapshot., Builds report snapshots, renders them, and persists the metadata. (+4 more)

### Community 64 - "web-page/src/lib/api.ts"
Cohesion: 0.15
Nodes (8): api, ApiClient, ApiError, ApiResponse, extractApiError(), LoginResponse, OtpResponse, OtpVerifyResponse

### Community 65 - "AI Output Contract"
Cohesion: 0.13
Nodes (16): AI Output Contract, Clinical Safety Boundary, Definition of Done, Document Precedence, Sources of Truth, trend_basis Distinct from evidence, MVP Definition (locked), USP Framing as Vision Narrative (+8 more)

### Community 66 - "test_otp_service.py"
Cohesion: 0.26
Nodes (13): generate_and_send_otp(), _OtpEntry, Generates a 6-digit OTP, stores it, and emails it via Gmail SMTP., Checks a submitted OTP against the stored one. The code is only consumed…, verify_otp(), Tests for the OTP generation/verification helpers behind password reset., _stub_smtp(), test_code_is_burned_after_max_attempts() (+5 more)

### Community 67 - "MVP Acceptance Journey"
Cohesion: 0.15
Nodes (13): Demo-Ready Definition, Definition of Demo-Ready MVP, FR-02 Patient Management, FR-03 Clinical Input, MVP Acceptance Journey, Product Goal Clinician Journey, AI-Owned analyzed Visit Status, Patient Endpoint Contract (+5 more)

### Community 68 - "FindingCategory"
Cohesion: 0.34
Nodes (15): FindingCategory, str, Whether a ranked condition sits in the differential or is flagged early.…, _analysis(), _finding(), _patient(), Unit tests for TriageService (ADR-006 decision 7). The ranking order is the…, ADR-006: the scan-derived trend has no column of its own -- it is read back… (+7 more)

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
Cohesion: 0.13
Nodes (15): AnalysisOrchestrator, Re-attach evidence from the orchestrator's own retrieved set. A provider names…, Drop uncited candidates, then rank and trim. A ranked condition without a…, Describe what actually produced this analysis. Derived from every provider that…, Execute the pipeline and return validated, ranked output., Runs the pipeline for one clinical context., Run imaging staging for the current visit, and a trend across it. Symptoms…, Return a stage estimate for the supplied scan metadata. (+7 more)

### Community 73 - "dashboard/layout.tsx"
Cohesion: 0.13
Nodes (12): DashboardLayout(), NAV_ITEMS, Activity(), IconProps, IconProps, Plus(), IconProps, Users() (+4 more)

### Community 74 - "ADR-003: AI Analysis Contract and the Mocked-Provider Seam"
Cohesion: 0.14
Nodes (14): Addendum: evidence-resolution correction (pre-`REPORT-01`), ADR-003: AI Analysis Contract and the Mocked-Provider Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact (+6 more)

### Community 75 - "REPORT-01D — Frontend Requirements & Backend Mapping Checklist"
Cohesion: 0.22
Nodes (14): 0. Baseline finding: this is not a "reconcile," it's mostly new pages, 1. Auth, 1A. Triage queue — the dashboard (ADR-006 decision 7), 2. Patients, 3. Clinical Case (Visit) + Symptoms, 3A. Scan intake (ADR-006 decisions 1, 2, 5), 4. AI Analysis + Differential Diagnosis + Evidence, 5. Clinician Sign-off → PDF Report (+6 more)

### Community 76 - "ADR-006-mri-primary-with-symptoms-as-context.md"
Cohesion: 0.26
Nodes (6): NeuroONE Agent Operating Contract, BUILD Mode, DEBUG Mode, PLAN Mode, TEST Mode, ADR-002 — Visit Ownership Derives From Parent Patient

### Community 78 - "test_scan_api.py"
Cohesion: 0.33
Nodes (11): _client(), _db_override(), TestClient, Contract tests for the scan endpoints (ADR-006)., _scan(), test_getting_a_scan_on_a_scanless_visit_is_404(), test_getting_a_visits_scan_succeeds(), test_uploading_a_scan_returns_201_with_metadata() (+3 more)

### Community 79 - "ADR-004: Clinical Report Snapshot and Rendering"
Cohesion: 0.15
Nodes (13): ADR-004: Clinical Report Snapshot and Rendering, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 80 - "ADR-005: Live LLM Provider Behind the AI-01 Seam"
Cohesion: 0.15
Nodes (13): ADR-005: Live LLM Provider Behind the AI-01 Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 81 - "Current Development Status Table"
Cohesion: 0.17
Nodes (13): Repository Inspection Rules, REPORT-01D Contract Map, AI Pipeline Contract Complete, Providers Simulated, Authentication Complete, Backend APIs Complete (35 endpoints, 400 tests), Dashboard Not Started Against Real Data, Explainable AI in the API, Not the UI, Current Development Status Table (+5 more)

### Community 82 - "reports.py"
Cohesion: 0.24
Nodes (12): get_report_service(), Provide the configured report service., download_report_pdf(), get_report(), Depends, get, Session, UUID (+4 more)

### Community 83 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, autoprefixer, eslint, eslint-config-next, postcss, tailwindcss, @types/js-cookie, @types/node (+4 more)

### Community 84 - "Triage Queue Contract"
Cohesion: 0.18
Nodes (14): Graphify Knowledge Graph Convention, Suggested Build Order, seed_demo_case.py Predates ADR-006, TriageEntry, Triage Queue Contract, Generate API Types From openapi.json, Triage Queue Screen, backend-routes.json OpenAPI Dump (+6 more)

### Community 85 - "get_current_user"
Cohesion: 0.11
Nodes (20): get_current_user(), Depends, Session, User, Validate the bearer token and return its associated user., Create a dependency that permits only the supplied user roles., Require the current user to have the administrator role., Require the current user to have the clinician role. (+12 more)

### Community 86 - "Design boundaries"
Cohesion: 0.32
Nodes (8): pipeline_note Provenance Label, provider_mode, HYBRID_PIPELINE_NOTE, provider_mode Is Not Widened to hybrid, Clinical Safety Boundary (NeuroONE assists, never autonomously diagnoses), Provenance Stated per Analysis, Not per Environment, Stage Estimate as Top-Ranked Candidate, Never a Lone Verdict, Design boundaries

### Community 87 - "web-page/package.json"
Cohesion: 0.04
Nodes (45): dependencies, axios, js-cookie, lucide-react, next, react, react-dom, zod (+37 more)

### Community 88 - "FR-01 Authentication"
Cohesion: 0.33
Nodes (7): bcrypt, passlib, python-jose, FR-01 Authentication, Auth Endpoint Contract, No Self-Registration, Auth Screens

### Community 89 - "TriageService"
Cohesion: 0.08
Nodes (30): get_triage_service(), Provide the configured triage service., get_triage_queue(), Depends, ge, get, le, Query (+22 more)

### Community 90 - "NeuroOne Login Neurons Artwork v1"
Cohesion: 0.38
Nodes (10): NeuroOne Login Neurons Artwork v1, Dark Indigo Gradient Background, Decorative Non-Informational Asset Role, Dual Neuron Diagonal Composition, Neural Brand Identity Signal, Parked Login Design Reference, Portrait Split-Panel Login Slot, Golden Synapse Spark Focal Point (+2 more)

### Community 91 - "AI-01 Contract-Real Provider-Mocked"
Cohesion: 0.13
Nodes (16): AI-01 Contract-Real Provider-Mocked, AI / RAG Pipeline, Locked Roadmap and Sequencing, httpx, ADR-005 Live LLM Provider, AI-02a Live LLM Provider, AI-02b Real Retrieval Corpus (deferred), AI Phasing Decision (+8 more)

### Community 92 - "ReportFindingSnapshot"
Cohesion: 0.28
Nodes (12): _build_story(), _draw_footer(), _finding_label(), _p(), Render a ReportSnapshot into a complete clinical report PDF (ADR-004). A pure…, Escape Platypus markup and fall back for characters base14 can't render.…, _render_finding(), _safe() (+4 more)

### Community 93 - "neural-network.tsx"
Cohesion: 0.33
Nodes (6): Edge, EDGES, findNode(), NeuralNetwork(), Node, NODES

### Community 94 - "2. Color system"
Cohesion: 0.50
Nodes (4): 2. Color system, Brand (login screen, decorative panel, marketing surfaces), Product (dashboard, forms, tables, reports), Status colors (diagnosis output, case flags)

### Community 95 - "Three Provenance States and pipeline_note"
Cohesion: 0.38
Nodes (7): Three Provenance States and pipeline_note, Scan Staging Provider Seam (SCAN-02), Mocked AI Credibility Risk, Analysis and Evidence Contract, AnalysisResponse, Contributing Regions Visualization Has No API, Mocked Staging Model Reads as Measurement

### Community 97 - "FR-07 Clinical Report"
Cohesion: 0.29
Nodes (8): pypdf, reportlab, FR-07 Clinical Report, Sign-Off Is a Gate, Not a Status, ReportResponse, Clinician Sign-off to PDF Report, Report Preview Page Has No API, Reports Screens

### Community 99 - "NeuroONE Frontend Redesign (parked)"
Cohesion: 0.25
Nodes (7): Sign in via OTP Button Replaces Google Sign-In, Account-flow handoff, Design implementation, Files in this change, NeuroONE Frontend Redesign (parked), Parked state, Preview

### Community 100 - "ADR-006 MRI Primary With Symptoms as Context"
Cohesion: 0.38
Nodes (7): V1 Scope Guard, APP-FLOW V1 Boundary, ADR-006 MRI Primary With Symptoms as Context, Revised Exclusions, V1 Exclusions, Explicit Frontend Non-Goals, MRI Upload + Prediction Polling

### Community 101 - "UserService"
Cohesion: 0.28
Nodes (6): UserUpdate, Session, User, UUID, Business logic for user management., UserService

### Community 102 - ".verify_credentials"
Cohesion: 0.21
Nodes (7): Token, User, Authenticate a user and issue an access token directly (no OTP step)., Verify a plaintext password against a stored hash., Create an access token for a user., Verify credentials and OTP together, then issue an access token. This flow…, Validates username/email + password and returns the User, without issuing a…

### Community 103 - "test_deleted_at_timezone_migration.py"
Cohesion: 0.43
Nodes (6): _load_migration(), Regression tests for the deleted_at timezone migration., test_downgrade_restores_naive_timestamps(), test_migration_chains_from_case_01(), test_upgrade_uses_implicit_timezone_cast(), ModuleType

### Community 104 - "web-page/.eslintrc.json"
Cohesion: 0.50
Nodes (3): extends, next/core-web-vitals, root

### Community 105 - "likelihood_band_for"
Cohesion: 0.25
Nodes (7): FindingResponse, likelihood_band_for(), Confidence-tiered output (section 8.3). This is what UI copy and the PDF should…, A ranked candidate as returned by the API., Derived from confidence, never read from the row., Tier a confidence value (AGENTS.md section 8.3). Derived, never stored: a…, computed_field

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
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

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

### Community 124 - "seed"
Cohesion: 0.67
Nodes (3): main(), Seed a demo patient whose history contains a multi-visit trend. AGENTS.md…, seed()

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

## Ambiguous Edges - Review These
- `V1 Exclusions` → `MRI Upload + Prediction Polling`  [AMBIGUOUS]
  frontend/README.md · relation: conceptually_related_to
- `Standard API Response Envelope` → `Assumed Backend API Contract`  [AMBIGUOUS]
  frontend/README.md · relation: conceptually_related_to
- `Golden Synapse Spark Focal Point` → `Neural Brand Identity Signal`  [AMBIGUOUS]
  frontend/web-page/public/images/neuroone-login-neurons-v1.png · relation: conceptually_related_to
- `Teal and Violet Accent Pair` → `Neural Brand Identity Signal`  [AMBIGUOUS]
  frontend/web-page/public/images/neuroone-login-neurons-v1.png · relation: conceptually_related_to
- `httpx` → `AI-02a Live LLM Provider`  [AMBIGUOUS]
  backend/requirements.txt · relation: conceptually_related_to

## Knowledge Gaps
- **438 isolated node(s):** `extends`, `next/core-web-vitals`, `$schema`, `style`, `rsc` (+433 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1115 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **45 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `V1 Exclusions` and `MRI Upload + Prediction Polling`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Standard API Response Envelope` and `Assumed Backend API Contract`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Golden Synapse Spark Focal Point` and `Neural Brand Identity Signal`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Teal and Violet Accent Pair` and `Neural Brand Identity Signal`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `httpx` and `AI-02a Live LLM Provider`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `BaseModel` connect `BaseModel` to `test_visit_service.py`, `EntityNotFoundError`, `test_analysis_repository.py`, `test_ai_orchestrator.py`, `RetrievedDocument`, `get_db`, `report_service.py`, `v1/analysis.py`, `DiagnosisCandidate`, `test_ai_live_llm.py`, `patients.py`, `AuthService`, `ReasoningRequest`, `Analysis`, `PatientService`, `User`, `test_ai_staging.py`, `Report`, `TokenPayload`, `Patient`, `Visit`, `trends.py`, `patient_visits.py`, `BaseRepository`, `dependencies.py`, `Base`, `Symptom`, `ScanResponse`, `AnalysisOrchestrator`, `TriageService`, `ReportFindingSnapshot`, `UserService`, `likelihood_band_for`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `test_visit_service.py`, `EntityNotFoundError`, `get_db`, `report_service.py`, `v1/analysis.py`, `patients.py`, `AuthService`, `Analysis`, `test_analysis_api.py`, `BaseModel`, `Visit`, `test_analysis_service.py`, `patient_visits.py`, `BaseRepository`, `dependencies.py`, `Symptom`, `test_report_service.py`, `test_auth_api.py`, `ReportService`, `FindingCategory`, `UserRepository`, `test_scan_api.py`, `reports.py`, `TriageService`, `seed`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._