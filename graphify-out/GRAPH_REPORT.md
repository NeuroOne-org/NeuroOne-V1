# Graph Report - vigorous-haslett-64122c  (2026-09-13)

## Corpus Check
- 284 files · ~194,068 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2987 nodes · 6996 edges · 186 communities (133 shown, 46 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 650 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7abfb9e1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- EntityNotFoundError
- UserRole
- AnalysisRepository
- AnalysisOrchestrator
- RetrievedDocument
- get_db
- report_service.py
- v1/analysis.py
- DiagnosisCandidate
- test_ai_live_llm.py
- patients.py
- AuthService
- reset-password/page.tsx
- build_providers
- test_visits_api.py
- AnalysisService
- test_analysis_api.py
- types.ts
- index.ts
- build_backend_architecture_report.py
- auth-provider.tsx
- PatientService
- User
- frontend/package.json
- test_ai_staging.py
- Report
- Patient
- BaseModel
- models/__init__.py
- detect_trends
- LocalScanStorage
- new/page.tsx
- ReasoningRequest
- r3f-canvas-scene.tsx
- NeuroOne Design System
- patient_visits.py
- BaseRepository
- components.json
- NeuroOne Frontend — Design System
- schemas/symptom.py
- Clinician Sign-Off Gates the Report
- .get_by_visit
- compilerOptions
- VisitService
- dashboard/page.tsx
- PLAN — AI-02b: Curated Retrieval Corpus
- build_clinical_context
- test_report_service.py
- Symptom
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
- ReportService
- web-page/src/lib/api.ts
- AI-01 Contract-Real Provider-Mocked
- test_otp_service.py
- MVP Acceptance Journey
- FindingCategory
- create_access_token
- Per-Record Ownership Check
- interactive-pipeline-demo.tsx
- ClinicalContext
- cn
- ADR-003: AI Analysis Contract and the Mocked-Provider Seam
- REPORT-01D — Frontend Requirements & Backend Mapping Checklist
- AI Output Contract
- UserRepository
- test_ai_mock_providers.py
- ADR-004: Clinical Report Snapshot and Rendering
- ADR-005: Live LLM Provider Behind the AI-01 Seam
- Current Development Status Table
- Analysis
- devDependencies
- Triage Queue Contract
- get_current_user
- Design boundaries
- web-page/package.json
- test_report_api.py
- FastAPI
- NeuroOne Login Neurons Artwork v1
- ValidationApplicationError
- ReportFindingSnapshot
- neural-network.tsx
- 2. Color system
- test_scan_service.py
- frontend/.eslintrc.json
- FR-07 Clinical Report
- web-page/next-env.d.ts
- NeuroONE Frontend Redesign (parked)
- handlers.py
- UserService
- Token
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
- test_patients_api.py
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
- test_scan_api.py
- ADR-007: Curated Retrieval Corpus Behind the AI-01 Seam
- Visit
- register_exception_handlers
- ADR-006-mri-primary-with-symptoms-as-context.md
- Three Provenance States and pipeline_note
- ADR-006 MRI Primary With Symptoms as Context
- FR-01 Authentication
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
- vocabulary.test.ts
- web-page/src/app/login/page.tsx
- NeuroONE Agent Operating Contract

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

### Community 0 - "EntityNotFoundError"
Cohesion: 0.07
Nodes (96): str, Lifecycle of a clinical case. ANALYZED is written by the AI pipeline (AI-01),…, VisitStatus, Payload used to record a symptom against a visit., Payload used to partially update a symptom., SymptomCreate, SymptomUpdate, _as_utc() (+88 more)

### Community 1 - "UserRole"
Cohesion: 0.24
Nodes (28): str, UserRole, PhoneNumber, A patient phone number., _create_payload(), _patient(), PatientCreate, Unit tests for PatientService ownership and doctor_id resolution rules. (+20 more)

### Community 2 - "AnalysisRepository"
Cohesion: 0.23
Nodes (28): AnalysisFinding, One ranked candidate condition. Decision support, never a definitive diagnosis:…, AnalysisRepository, Provide analysis-specific queries in addition to common CRUD., _analysis(), _engine(), _finding(), Real-database tests for analysis persistence. Run against SQLite because the… (+20 more)

### Community 3 - "AnalysisOrchestrator"
Cohesion: 0.09
Nodes (49): AnalysisOrchestrator, Re-attach evidence from the orchestrator's own retrieved set. A provider names…, Drop uncited candidates, then rank and trim. A ranked condition without a…, Describe what actually produced this analysis. Derived from every provider that…, Execute the pipeline and return validated, ranked output., Runs the pipeline for one clinical context., Run imaging staging for the current visit, and a trend across it. Symptoms…, What the LLM provider returns. Validated at the seam, so a real provider in… (+41 more)

### Community 4 - "RetrievedDocument"
Cohesion: 0.09
Nodes (25): _document(), Deterministic stand-in for a retrieval corpus and a reasoning model. Everything…, Return documents relevant to the query, most relevant first. Returning an empty…, MockEvidenceRetriever, _normalize(), Deterministic stand-in for a literature retriever. Matches the query against a…, Keyword retriever over the frozen mock corpus., Return matching documents, most relevant first. An empty result is a legitimate… (+17 more)

### Community 5 - "get_db"
Cohesion: 0.09
Nodes (55): get_analysis_service(), get_current_active_user(), get_db(), get_visit_service(), Provide the configured analysis service., Return the current user only when the account is active., Provide a database session and always close it after the request., Provide the configured visit service. (+47 more)

### Community 6 - "report_service.py"
Cohesion: 0.12
Nodes (34): Render a complete, multi-page clinical report PDF. Raises whatever ReportLab…, render(), Clinical report contract (FR-07, ADR-004). ``ReportSnapshot`` is exactly what…, The patient/case identification FR-07 requires a report to carry., One clinical input as recorded for the visit (FR-03)., The clinical case the analysis was run against., A citation as it must appear in the PDF (FR-05/06)., Everything the renderer may draw on. Nothing else reaches the PDF. (+26 more)

### Community 7 - "v1/analysis.py"
Cohesion: 0.10
Nodes (33): get_report_service(), Provide the configured report service., create_report(), get_analysis(), list_reports(), Depends, ge, get (+25 more)

### Community 8 - "DiagnosisCandidate"
Cohesion: 0.10
Nodes (36): AnalysisResult, DiagnosisCandidate, Structured differential-diagnosis contract (AGENTS.md section 8.2). Decision…, An early-watch flag must point at the patient's own history. Note the…, Validated pipeline output, before persistence., A pointer into the patient's OWN visit history. Distinct from ``EvidenceRef``,…, One ranked possible condition. ``extra="forbid"`` is deliberate: a model that…, TrendBasisRef (+28 more)

### Community 9 - "test_ai_live_llm.py"
Cohesion: 0.09
Nodes (70): _analyze(), _candidates(), _context(), _evidence(), _llm(), Tests for the live reasoning provider (AI-02 slice 1, ADR-005). A live model is…, A client whose model always answers with ``content``., One well-formed candidate payload, JSON-encoded as a model would. (+62 more)

### Community 10 - "patients.py"
Cohesion: 0.11
Nodes (34): get_patient_service(), Provide the configured patient service., create_patient(), delete_patient(), get_patient(), list_patients(), _paginated_response(), delete (+26 more)

### Community 11 - "AuthService"
Cohesion: 0.13
Nodes (23): TokenPayload, AuthService, Hash a plaintext password., Validate an access token and return its payload., Validate the reset code and set a new password., Business logic for authentication operations., InvalidCredentialsError, InvalidOtpError (+15 more)

### Community 12 - "reset-password/page.tsx"
Cohesion: 0.09
Nodes (28): ForgotPasswordPage(), LoginForm(), handleOtpLogin(), handleSubmit(), validate(), ResetPasswordForm(), SignupPage(), VerifyOtpForm() (+20 more)

### Community 13 - "build_providers"
Cohesion: 0.14
Nodes (18): AI orchestration. Layering rule: nothing in this package imports a repository…, EvidenceRetriever, ImagingStager, LLMClient, Protocol, The provider seam. This module is the entire surface AI-02 replaces. Everything…, Retrieves candidate literature for a clinical context. Implementations must…, Produces ranked candidate conditions from context plus evidence. The return… (+10 more)

### Community 14 - "test_visits_api.py"
Cohesion: 0.15
Nodes (34): _client(), _db_override(), TestClient, Contract tests for the clinical case (visit) and symptom endpoints. Extends…, Only patient_id is exposed, so no endpoint can lazy-load per row., _symptom(), test_a_whitespace_only_observation_is_rejected(), test_add_symptom_returns_201() (+26 more)

### Community 15 - "AnalysisService"
Cohesion: 0.14
Nodes (14): AnalysisEvidence, One citation supporting one ranked finding. Scoped to a finding rather than to…, AnalysisService, Analysis, Session, UUID, Business logic for AI analysis of a clinical case. The ordering in…, Run the AI pipeline for a visit and persist the result. Ownership violations… (+6 more)

### Community 16 - "test_analysis_api.py"
Cohesion: 0.15
Nodes (31): _analysis(), _client(), _db_override(), _evidence(), _finding(), TestClient, Contract tests for the analysis endpoints. Beyond the usual status/shape…, A consumer must be able to tell simulated evidence from live evidence. (+23 more)

### Community 17 - "types.ts"
Cohesion: 0.04
Nodes (54): AnalysisFindings(), BAND_TONE, BAR_TONE, PointList(), AnalysisProvenance(), ADR-0006, ChevronDown(), IconProps (+46 more)

### Community 18 - "index.ts"
Cohesion: 0.03
Nodes (55): ArrowRight(), IconProps, Bell(), IconProps, Calendar(), IconProps, ChevronRight(), IconProps (+47 more)

### Community 19 - "build_backend_architecture_report.py"
Cohesion: 0.18
Nodes (31): Document, RGBColor, add_body(), add_bullets(), add_callout(), add_code(), add_cover(), add_field() (+23 more)

### Community 20 - "auth-provider.tsx"
Cohesion: 0.11
Nodes (25): VisitAnalysis(), downloadReport(), runAnalysis(), signOff(), onSubmit(), AuthContext, AuthContextValue, AuthProvider() (+17 more)

### Community 21 - "PatientService"
Cohesion: 0.15
Nodes (20): PhoneNumber, PatientCreate, Payload used to create a patient., PatientService, Patient, Session, User, UUID (+12 more)

### Community 22 - "User"
Cohesion: 0.09
Nodes (30): User model definitions., User, Session, Symptom, UUID, Visit, Open a clinical case for a patient the caller owns. The patient id came from…, Retrieve a visit by ID. Ownership violations read as 404. (+22 more)

### Community 23 - "frontend/package.json"
Cohesion: 0.06
Nodes (29): autoprefixer, axios, eslint, eslint-config-next, js-cookie, lucide-react, next, postcss (+21 more)

### Community 24 - "test_ai_staging.py"
Cohesion: 0.13
Nodes (32): MockImagingStager, Deterministic stand-in for an MRI staging model (ADR-006). The stage estimate…, Deterministic stage estimate derived from the scan's checksum., Derive a stage, confidence and region breakdown from the checksum., The MRI scan attached to a visit, as the AI layer sees it. PHI-minimal like the…, ScanSummary, Imaging staging contract (ADR-006). A third provider seam alongside the…, One anatomical region's weight in a staging estimate. Descriptive detail only.… (+24 more)

### Community 25 - "Report"
Cohesion: 0.16
Nodes (21): One generated PDF report, snapshotting its source analysis. Never mutated after…, Report, Session, UUID, Report persistence operations., Provide report-specific queries in addition to common CRUD., Return an analysis's reports, newest first., Count an analysis's active reports. (+13 more)

### Community 26 - "Patient"
Cohesion: 0.14
Nodes (15): Patient, Patient model definitions., PatientRepository, Session, UUID, Patient persistence operations., Count active patients assigned to a doctor., Return the active patient with the given phone number, if any. (+7 more)

### Community 27 - "BaseModel"
Cohesion: 0.13
Nodes (31): LiveReasoningPayload, The model's whole response. ``extra="forbid"`` is the structural half of the…, get_auth_service(), Provide the configured authentication service., forgot_password(), login(), Depends, get (+23 more)

### Community 28 - "models/__init__.py"
Cohesion: 0.11
Nodes (14): Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), Database engine and session configuration., Enum, Persisted AI analysis, its ranked findings, and their citations. Naming is…, Base (+6 more)

### Community 29 - "detect_trends"
Cohesion: 0.08
Nodes (42): Normalize Input + Build Clinical Context (TRD section 8, stages 1-2). This is…, Map a Visit and its live symptoms into the AI-facing shape., _to_context_visit(), detect_trends(), _direction(), Cross-visit symptom trend detection. This is the mechanism behind AGENTS.md…, Normalized names of symptoms that are getting worse across visits. This is the…, Classify a severity series ordered oldest-first. (+34 more)

### Community 30 - "LocalScanStorage"
Cohesion: 0.07
Nodes (39): Storage backends for artifacts that do not belong in the database., LocalScanStorage, Path, UUID, Storage for MRI scan bytes, outside the database (ADR-006 decision 5). A PDF…, Persist ``content`` and return its storage key., Filesystem-backed storage under a configured base directory. The concrete…, Tests for LocalScanStorage (ADR-006 decision 5). (+31 more)

### Community 31 - "new/page.tsx"
Cohesion: 0.07
Nodes (41): EMPTY_SYMPTOM, StepKey, STEPS, ADR-0006, IntakeInput, intakeSchema, splitList(), StepKey (+33 more)

### Community 32 - "ReasoningRequest"
Cohesion: 0.13
Nodes (16): Reason over the supplied context and evidence., LiveCandidatePayload, LiveLLMClient, Any, Client, Live reasoning over an OpenAI-compatible chat-completions endpoint. The AI-02…, Reasoner backed by a real model behind ``LLMClient``., Serialize the case as JSON. JSON rather than prose deliberately: clinician free… (+8 more)

### Community 33 - "r3f-canvas-scene.tsx"
Cohesion: 0.14
Nodes (12): R3fCanvasScene, FloatingParticles(), Particle, PARTICLES, createNeuralMesh(), NeuralMesh3D(), StoryCard3D(), StoryCardProps (+4 more)

### Community 34 - "NeuroOne Design System"
Cohesion: 0.12
Nodes (20): 1. Brand identity, 3. Typography, 4. Login screen, 5. Open items, Brand Color Palette, Cormorant Garamond Fallback, IBM Plex Sans UI Font, Login Screen Spec (+12 more)

### Community 35 - "patient_visits.py"
Cohesion: 0.14
Nodes (23): alias, create_visit(), get_visit_history(), list_patient_visits(), Depends, ge, get, le (+15 more)

### Community 36 - "BaseRepository"
Cohesion: 0.14
Nodes (16): Analysis persistence operations., Persist an analysis and advance the visit status in one transaction. Both…, BaseRepository, Session, UUID, Generic repository providing reusable CRUD operations. This base repository…, Soft-delete an entity. Marks the entity as deleted by setting the `is_deleted`…, Check whether a record exists. Returns True if an active record with the given… (+8 more)

### Community 37 - "components.json"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, registries (+11 more)

### Community 38 - "NeuroOne Frontend — Design System"
Cohesion: 0.09
Nodes (21): 10. Data layer, 11. Writing, 1. The idea, 2. Color, 3. Typography, 4. Shape and spacing, 5. Components, 6. Icons (+13 more)

### Community 39 - "schemas/symptom.py"
Cohesion: 0.24
Nodes (8): field_validator, Symptom request and response schemas., A whitespace-only observation is the same as no observation, rejected rather…, Fields shared by symptom request and response schemas., Public symptom data returned by the API., _reject_blank(), SymptomBase, SymptomResponse

### Community 40 - "Clinician Sign-Off Gates the Report"
Cohesion: 0.15
Nodes (14): ClinicalContext, Database-Free app/ai Package, Re-Running Analysis Creates a New Row, Multiple Immutable Reports per Analysis, Render Before Persist, ReportLab (Platypus) Renderer, ReportService, Clinical Context Leaves the Machine (+6 more)

### Community 41 - ".get_by_visit"
Cohesion: 0.23
Nodes (8): Session, UUID, Return the most recent analysis for a visit, if any., Return each patient's most recent analysis, across all their visits. The triage…, Eager-load findings and their citations in two extra queries. Every read path…, Return an active analysis with its findings and citations loaded., Return a visit's analyses, newest first., Count a visit's active analyses.

### Community 42 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+13 more)

### Community 43 - "VisitService"
Cohesion: 0.09
Nodes (25): get_scan_service(), Reusable FastAPI dependencies for database and access control., Provide the configured scan service., One MRI scan attached to a visit. Attaches to the Visit, not the Patient…, Scan, Session, UUID, Scan persistence operations. (+17 more)

### Community 44 - "dashboard/page.tsx"
Cohesion: 0.07
Nodes (31): DashboardPage(), filterEyebrow(), formatToday(), matchesFilter(), QueueRow(), REASON_STYLE, subscribeNever(), summarise() (+23 more)

### Community 45 - "PLAN — AI-02b: Curated Retrieval Corpus"
Cohesion: 0.06
Nodes (34): 10. Recommended Design, 11. Data / Schema Impact, 12. API / Contract Impact, 13. AI / RAG Impact, 14. Security / Privacy Impact, 15. Clinical Safety Impact, 16. Failure / Recovery Behavior, 17. Implementation Tasks (+26 more)

### Community 46 - "build_clinical_context"
Cohesion: 0.21
Nodes (21): _age_years(), build_clinical_context(), date, Whole years, so a date of birth never reaches the reasoning layer., Assemble the context the AI pipeline reasons over. ``prior_visits`` must be…, _patient(), Tests for the ORM -> ClinicalContext normalize stage. The PHI-minimization…, The current severity is part of the trajectory, not outside it. (+13 more)

### Community 47 - "test_report_service.py"
Cohesion: 0.20
Nodes (25): _analysis(), _evidence(), _finding(), _patient(), Unit tests for ReportService. Two properties carry the weight, mirroring…, ADR-006 decision 6: sign-off gates the report., The masked 404 must not disclose the analysis behind it., _service() (+17 more)

### Community 48 - "Symptom"
Cohesion: 0.09
Nodes (34): A neurological symptom recorded against a clinical case., Symptom, Session, UUID, Symptom persistence operations., Provide symptom-specific queries in addition to common CRUD operations., Return a visit's active symptoms in recording order., Count a visit's active symptoms. (+26 more)

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

### Community 59 - "UserResponse"
Cohesion: 0.12
Nodes (18): Require the current user to have the administrator role., require_admin(), create_user(), Depends, post, Session, User, Administrator-only endpoints. (+10 more)

### Community 60 - "Ownership Violations Return 404, Not 403"
Cohesion: 0.14
Nodes (14): Enumeration Resistance for PHI-Adjacent Resources, Ownership Violations Return 404, Not 403, Server-Side Audit Logging of the Real Reason, 404 Re-Labelling / Identifier Masking, Symptom-Belongs-To-Visit Verification, AnalysisRepository.create_with_status, Failure Precedes the First Write, MAX_CONFIDENCE Ceiling of 0.92 (+6 more)

### Community 61 - "dependencies"
Cohesion: 0.11
Nodes (18): dependencies, axios, clsx, framer-motion, @hookform/resolvers, js-cookie, lucide-react, next (+10 more)

### Community 62 - "[id]/page.tsx"
Cohesion: 0.12
Nodes (25): PatientDetailPage(), VisitButton(), NewVisitPage(), PatientsPage(), ChevronLeft(), IconProps, IconProps, Plus() (+17 more)

### Community 63 - "ReportService"
Cohesion: 0.21
Nodes (10): Report, Session, UUID, Build, render, and persist a new report for an analysis. Render-before-persist…, Retrieve one report by ID. The caller named only the report, so an…, List an analysis's reports, newest first., Re-render a report's PDF bytes from its immutable snapshot., Builds report snapshots, renders them, and persists the metadata. (+2 more)

### Community 64 - "web-page/src/lib/api.ts"
Cohesion: 0.15
Nodes (8): api, ApiClient, ApiError, ApiResponse, extractApiError(), LoginResponse, OtpResponse, OtpVerifyResponse

### Community 65 - "AI-01 Contract-Real Provider-Mocked"
Cohesion: 0.13
Nodes (16): AI-01 Contract-Real Provider-Mocked, AI / RAG Pipeline, Locked Roadmap and Sequencing, httpx, ADR-005 Live LLM Provider, AI-02a Live LLM Provider, AI-02b Real Retrieval Corpus (deferred), AI Phasing Decision (+8 more)

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

### Community 72 - "ClinicalContext"
Cohesion: 0.08
Nodes (33): MockCondition, A rule mapping clinical findings to a candidate condition., The AI pipeline (TRD section 8, APP-FLOW section 5). Clinical Case -> Normalize…, MockLLMClient, Deterministic stand-in for the reasoning model. Scores the frozen condition…, Fold a staging estimate into the same cited candidate shape. The stage never…, Rank the condition rules against the supplied context and evidence., Rule-based reasoner over the frozen condition table. (+25 more)

### Community 73 - "cn"
Cohesion: 0.08
Nodes (29): DashboardLayout(), NAV_ITEMS, Signal(), FindingRow(), ConfidenceDial(), ConfidenceDialProps, Activity(), IconProps (+21 more)

### Community 74 - "ADR-003: AI Analysis Contract and the Mocked-Provider Seam"
Cohesion: 0.14
Nodes (14): Addendum: evidence-resolution correction (pre-`REPORT-01`), ADR-003: AI Analysis Contract and the Mocked-Provider Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact (+6 more)

### Community 75 - "REPORT-01D — Frontend Requirements & Backend Mapping Checklist"
Cohesion: 0.22
Nodes (14): 0. Baseline finding: this is not a "reconcile," it's mostly new pages, 1. Auth, 1A. Triage queue — the dashboard (ADR-006 decision 7), 2. Patients, 3. Clinical Case (Visit) + Symptoms, 3A. Scan intake (ADR-006 decisions 1, 2, 5), 4. AI Analysis + Differential Diagnosis + Evidence, 5. Clinician Sign-off → PDF Report (+6 more)

### Community 76 - "AI Output Contract"
Cohesion: 0.13
Nodes (16): AI Output Contract, Clinical Safety Boundary, Definition of Done, Document Precedence, Sources of Truth, trend_basis Distinct from evidence, MVP Definition (locked), USP Framing as Vision Narrative (+8 more)

### Community 78 - "test_ai_mock_providers.py"
Cohesion: 0.14
Nodes (23): _analyze(), _context(), Tests for the mocked retriever and reasoner. Two properties matter most here.…, A stage estimate with no resolvable citation would be silently dropped., The fixture must not read as real literature., AGENTS.md 8.2: confidence is likelihood, never certainty., The property a seeded RNG or a canned fixture would not have., AGENTS.md 8.1: schema-valid deterministic results. (+15 more)

### Community 79 - "ADR-004: Clinical Report Snapshot and Rendering"
Cohesion: 0.15
Nodes (13): ADR-004: Clinical Report Snapshot and Rendering, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 80 - "ADR-005: Live LLM Provider Behind the AI-01 Seam"
Cohesion: 0.15
Nodes (13): ADR-005: Live LLM Provider Behind the AI-01 Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 81 - "Current Development Status Table"
Cohesion: 0.17
Nodes (13): Repository Inspection Rules, REPORT-01D Contract Map, AI Pipeline Contract Complete, Providers Simulated, Authentication Complete, Backend APIs Complete (35 endpoints, 400 tests), Dashboard Not Started Against Real Data, Explainable AI in the API, Not the UI, Current Development Status Table (+5 more)

### Community 82 - "Analysis"
Cohesion: 0.18
Nodes (14): Analysis, One run of the AI pipeline against one clinical case. Re-running creates a new…, One patient's position in the triage queue. Not an ORM-backed response: there…, TriageEntry, _awaiting_sign_off(), _has_open_early_watch(), _has_worsening_trend(), Session (+6 more)

### Community 83 - "devDependencies"
Cohesion: 0.11
Nodes (18): devDependencies, autoprefixer, eslint, eslint-config-next, jsdom, postcss, tailwindcss, @testing-library/dom (+10 more)

### Community 84 - "Triage Queue Contract"
Cohesion: 0.18
Nodes (14): Graphify Knowledge Graph Convention, Suggested Build Order, seed_demo_case.py Predates ADR-006, TriageEntry, Triage Queue Contract, Generate API Types From openapi.json, Triage Queue Screen, backend-routes.json OpenAPI Dump (+6 more)

### Community 85 - "get_current_user"
Cohesion: 0.20
Nodes (11): get_current_user(), Depends, Session, User, Validate the bearer token and return its associated user., Create a dependency that permits only the supplied user roles., Require the current user to have the clinician role., require_clinician() (+3 more)

### Community 86 - "Design boundaries"
Cohesion: 0.32
Nodes (8): pipeline_note Provenance Label, provider_mode, HYBRID_PIPELINE_NOTE, provider_mode Is Not Widened to hybrid, Clinical Safety Boundary (NeuroONE assists, never autonomously diagnoses), Provenance Stated per Analysis, Not per Environment, Stage Estimate as Top-Ranked Candidate, Never a Lone Verdict, Design boundaries

### Community 87 - "web-page/package.json"
Cohesion: 0.04
Nodes (45): dependencies, axios, js-cookie, lucide-react, next, react, react-dom, zod (+37 more)

### Community 88 - "test_report_api.py"
Cohesion: 0.17
Nodes (23): AnalysisNotReviewedError, Raised when a report is requested for an unreviewed analysis. ADR-006 decision…, _client(), _db_override(), TestClient, Contract tests for the report endpoints. Beyond the usual status/shape…, ADR-006 decision 6: sign-off gates the report., AGENTS.md 8.2: not in the schema, not in API field naming. (+15 more)

### Community 89 - "FastAPI"
Cohesion: 0.07
Nodes (27): get_triage_service(), Provide the configured triage service., Top-level API router., get_triage_queue(), Depends, ge, get, le (+19 more)

### Community 90 - "NeuroOne Login Neurons Artwork v1"
Cohesion: 0.38
Nodes (10): NeuroOne Login Neurons Artwork v1, Dark Indigo Gradient Background, Decorative Non-Informational Asset Role, Dual Neuron Diagonal Composition, Neural Brand Identity Signal, Parked Login Design Reference, Portrait Split-Panel Login Slot, Golden Synapse Spark Focal Point (+2 more)

### Community 91 - "ValidationApplicationError"
Cohesion: 0.24
Nodes (12): ApplicationError, AuthenticationError, ExternalServiceError, InternalServerError, NotFoundError, Any, Exception, HTTP-agnostic application exception hierarchy. (+4 more)

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

### Community 97 - "FR-07 Clinical Report"
Cohesion: 0.29
Nodes (8): pypdf, reportlab, FR-07 Clinical Report, Sign-Off Is a Gate, Not a Status, ReportResponse, Clinician Sign-off to PDF Report, Report Preview Page Has No API, Reports Screens

### Community 99 - "NeuroONE Frontend Redesign (parked)"
Cohesion: 0.25
Nodes (7): Sign in via OTP Button Replaces Google Sign-In, Account-flow handoff, Design implementation, Files in this change, NeuroONE Frontend Redesign (parked), Parked state, Preview

### Community 100 - "handlers.py"
Cohesion: 0.25
Nodes (14): ErrorResponse, The standard shape returned for API errors., _error_response(), http_exception_handler(), Exception, Global translation of domain exceptions into HTTP responses., request_validation_error_handler(), unhandled_error_handler() (+6 more)

### Community 101 - "UserService"
Cohesion: 0.16
Nodes (11): UserUpdate, BaseService, Shared service-layer infrastructure., Base service providing access to the repository., Public service-layer exports., Session, User, UUID (+3 more)

### Community 102 - "Token"
Cohesion: 0.15
Nodes (11): Token, Session, Token, User, Authenticate a user and issue an access token directly (no OTP step)., Verify a plaintext password against a stored hash., Create an access token for a user., Email a reset code if the address belongs to an active account. Always returns… (+3 more)

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
Cohesion: 0.30
Nodes (14): _client(), _db_override(), _patient(), TestClient, Integration-style contract tests for patient endpoints. Covers the ownership-…, test_clinician_cannot_create_patient_for_another_doctor(), test_delete_on_other_doctors_patient_is_404(), test_delete_own_patient_returns_204() (+6 more)

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

### Community 155 - "test_scan_api.py"
Cohesion: 0.33
Nodes (11): _client(), _db_override(), TestClient, Contract tests for the scan endpoints (ADR-006)., _scan(), test_getting_a_scan_on_a_scanless_visit_is_404(), test_getting_a_visits_scan_succeeds(), test_uploading_a_scan_returns_201_with_metadata() (+3 more)

### Community 156 - "ADR-007: Curated Retrieval Corpus Behind the AI-01 Seam"
Cohesion: 0.15
Nodes (13): ADR-007: Curated Retrieval Corpus Behind the AI-01 Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 157 - "Visit"
Cohesion: 0.23
Nodes (7): A clinical case / visit belonging to a patient. Ownership is derived from the…, Visit, parametrize, The demo seed's scenarios produce the triage flags they claim to. The seed's…, test_scenario_lands_in_its_stated_queue_state(), test_synthetic_scan_stages_as_requested_and_is_deterministic(), _visit()

### Community 158 - "register_exception_handlers"
Cohesion: 0.23
Nodes (11): _application_handler(), Register every centralized domain-to-HTTP mapping., register_exception_handlers(), Tests for soft-delete semantics and transactional failure handling., RepositoryRecord, _session(), test_create_rolls_back_and_raises_controlled_database_error(), test_mid_write_failure_persists_nothing_and_translates_database_error() (+3 more)

### Community 160 - "Three Provenance States and pipeline_note"
Cohesion: 0.38
Nodes (7): Three Provenance States and pipeline_note, Scan Staging Provider Seam (SCAN-02), Mocked AI Credibility Risk, Analysis and Evidence Contract, AnalysisResponse, Contributing Regions Visualization Has No API, Mocked Staging Model Reads as Measurement

### Community 161 - "ADR-006 MRI Primary With Symptoms as Context"
Cohesion: 0.38
Nodes (7): V1 Scope Guard, APP-FLOW V1 Boundary, ADR-006 MRI Primary With Symptoms as Context, Revised Exclusions, V1 Exclusions, Explicit Frontend Non-Goals, MRI Upload + Prediction Polling

### Community 162 - "FR-01 Authentication"
Cohesion: 0.33
Nodes (7): bcrypt, passlib, python-jose, FR-01 Authentication, Auth Endpoint Contract, No Self-Registration, Auth Screens

### Community 183 - "vocabulary.test.ts"
Cohesion: 0.29
Nodes (5): EXCLUDED, ROOTS, RULES, SRC, ADR-0006

### Community 185 - "NeuroONE Agent Operating Contract"
Cohesion: 0.70
Nodes (5): NeuroONE Agent Operating Contract, BUILD Mode, DEBUG Mode, PLAN Mode, TEST Mode

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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1210 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
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
- **Why does `BaseModel` connect `BaseModel` to `EntityNotFoundError`, `UserRole`, `AnalysisRepository`, `AnalysisOrchestrator`, `RetrievedDocument`, `get_db`, `report_service.py`, `v1/analysis.py`, `DiagnosisCandidate`, `patients.py`, `AuthService`, `AnalysisService`, `PatientService`, `User`, `test_ai_staging.py`, `Report`, `Patient`, `models/__init__.py`, `Visit`, `detect_trends`, `register_exception_handlers`, `ReasoningRequest`, `patient_visits.py`, `BaseRepository`, `schemas/symptom.py`, `VisitService`, `Symptom`, `ScanResponse`, `UserResponse`, `ClinicalContext`, `Analysis`, `FastAPI`, `ReportFindingSnapshot`, `handlers.py`, `UserService`, `Token`, `likelihood_band_for`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `EntityNotFoundError`, `UserRole`, `get_db`, `report_service.py`, `v1/analysis.py`, `patients.py`, `AuthService`, `test_visits_api.py`, `AnalysisService`, `test_analysis_api.py`, `PatientService`, `BaseModel`, `models/__init__.py`, `test_scan_api.py`, `Visit`, `LocalScanStorage`, `patient_visits.py`, `VisitService`, `test_report_service.py`, `test_auth_api.py`, `UserResponse`, `ReportService`, `FindingCategory`, `UserRepository`, `Analysis`, `test_report_api.py`, `FastAPI`, `test_scan_service.py`, `test_patients_api.py`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._