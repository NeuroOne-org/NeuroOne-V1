# Graph Report - NeuroOne-V1  (2026-09-11)

## Corpus Check
- 221 files · ~168,246 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2411 nodes · 5973 edges · 146 communities (113 shown, 26 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 583 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d3dd2644`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- User
- ValidationApplicationError
- EntityNotFoundError
- build_providers
- patients.py
- Patient
- UserRole
- test_ai_staging.py
- cn
- reset-password/page.tsx
- get_current_active_user
- build_backend_architecture_report.py
- dependencies.py
- test_report_service.py
- patient_visits.py
- UserService
- dashboard/page.tsx
- interactive-pipeline-demo.tsx
- web-page/package.json
- extractApiError
- compilerOptions
- frontend/package.json
- dependencies
- test_auth_api.py
- auth-provider.tsx
- create_access_token
- AnalysisOrchestrator
- ScanService
- ADR-006-mri-primary-with-symptoms-as-context.md
- AI Pipeline (Normalize → Context → Retrieve → Rank → LLM → Validate → Persist)
- Security and Privacy Rules
- test_ai_live_llm.py
- Confirmed Roles (ADMIN, CLINICIAN; RECEPTIONIST deferred)
- test_analysis_service.py
- ReportRepository
- Standard API Response Envelope
- JWT Authentication Flow
- r3f-canvas-scene.tsx
- CASE-01 — Clinical Case / Symptom Domain
- Clinical Safety Boundary (non-negotiable)
- RetrievedDocument
- Mode Transition State Machine
- DiagnosisCandidate
- test_report_api.py
- 1f74d19af1b8_widen_patient_email_and_promote_phone_.py
- 8e72c1f4a9b0_replace_legacy_user_roles.py
- a3c7be51d904_create_visits_and_symptoms.py
- b8d41e2f7c53_make_deleted_at_timezone_aware.py
- test_otp_service.py
- test_analysis_api.py
- visits.py
- middleware.ts
- BaseRepository
- test_health.py
- frontend/.eslintrc.json
- frontend/next.config.mjs
- PatientService
- constants.py
- conftest.py
- docker-compose.yml — Local Dev Stack
- next-env.d.ts
- backup.py
- build_embeddings.py
- ingest_documents.py
- seed_database.py
- Commit Message Convention
- Authentication Flow
- Frontend README — Next.js 14 Client
- README — NeuroOne Vision
- LocalScanStorage
- detect_trends
- test_ai_mock_providers.py
- get_db
- build_clinical_context
- VisitRepository
- AuthService
- ADR-003: AI Analysis Contract and the Mocked-Provider Seam
- report_service.py
- REPORT-01D — Frontend Requirements & Backend Mapping Checklist
- test_deleted_at_timezone_migration.py
- Visit
- test_patients_api.py
- corpus/__init__.py
- CLAUDE.md
- UserResponse
- Analysis
- compilerOptions
- ADR-005: Live LLM Provider Behind the AI-01 Seam
- get_triage_queue
- ADR-004: Clinical Report Snapshot and Rendering
- VisitStatus
- BaseModel
- b2b31bad27df_add_symptom_observation.py
- c4e19a7b6d20_create_analyses_findings_and_evidence.py
- dcfbc7d5b2c9_create_reports.py
- UserRepository
- Q: How are Alembic migrations and backend tests configured, and where should PR CI run pytest?
- Q: The parallel AI-01 work is committed and pulled; plan our next work
- reports/__init__.py
- reports.py
- Base
- seed
- NeuroOne Frontend — Redesign Checklist
- test_scan_service.py
- devDependencies
- web-page/src/lib/api.ts
- ReportService
- get_user_service
- test_scan_api.py
- NeuroOne — Design System
- ReportFindingSnapshot
- NeuroONE Frontend Redesign
- Symptom
- verify-otp/page.tsx
- scripts
- web-page/src/lib/validation.ts
- useAuth
- web-page/.eslintrc.json
- web-page/src/components/password-strength.tsx
- DashboardPage
- PLAN.md
- NeuroOne login artwork v1
- web-page/src/app/layout.tsx
- frontend/tailwind.config.ts
- web-page/next-env.d.ts
- fonts/README.md
- web-page/tailwind.config.ts
- frontend/src/lib/validation.ts
- FastAPI
- test_triage_api.py
- _error_response
- ADR-006: MRI Becomes a Primary Input, With Symptoms as Context
- likelihood_band_for
- schemas/symptom.py
- common.py
- app/main.py
- 14056b8ec27d_create_scans.py
- 7544ad0b1ed6_add_analysis_sign_off.py
- ScanResponse

## God Nodes (most connected - your core abstractions)
1. `User` - 123 edges
2. `EntityNotFoundError` - 92 edges
3. `UserRole` - 82 edges
4. `BaseModel` - 81 edges
5. `Visit` - 57 edges
6. `VisitService` - 56 edges
7. `get_db()` - 53 edges
8. `AnalysisOrchestrator` - 52 edges
9. `VisitStatus` - 50 edges
10. `get_current_active_user()` - 49 edges

## Surprising Connections (you probably didn't know these)
- `Assumed Backend API Contract` --conceptually_related_to--> `Standard API Response Envelope`  [AMBIGUOUS]
  frontend/README.md → CONTRIBUTING.md
- `TRD Layered Architecture` --semantically_similar_to--> `Feature → API → Service → Repository → Model → Schema Flow`  [INFERRED] [semantically similar]
  docs/TRD.md → CONTRIBUTING.md
- `Milestone 2 — Deliver One Vertical Feature` --semantically_similar_to--> `PAT-01 — Authorized Patient CRUD Vertical Slice`  [INFERRED] [semantically similar]
  reports/PROGRESS_REPORT.md → docs/NEUROONE-MVP-SCOPE.md
- `MRI Upload + Prediction Polling` --semantically_similar_to--> `MRI-Based Neurodegenerative Disease Analysis (marketing claim)`  [INFERRED] [semantically similar]
  frontend/README.md → README.md
- `Agent Definition of Done Checklist` --semantically_similar_to--> `Contributing Definition of Done`  [INFERRED] [semantically similar]
  AGENTS.md → CONTRIBUTING.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **AI/RAG Evidence Traceability Chain** — docs_trd_ai_pipeline, docs_trd_rag_rules, docs_trd_ai_output_contract, docs_app_flow_evidence_flow, docs_prd_fr_06_explainability, docs_neuroone_mvp_scope_trend_basis [EXTRACTED 1.00]
- **MVP Acceptance Journey — Same Path Across Four Documents** — docs_prd_mvp_acceptance_journey, docs_app_flow_primary_flow, docs_neuroone_mvp_scope_demo_ready_definition, agents_test_mode, docs_trd_implementation_sequence [EXTRACTED 1.00]
- **Per-Record Ownership Enforcement Pattern (404 masking, derived one hop up)** — docs_decisions_adr_001_ownership_violation_status_code_enumeration_resistance, docs_decisions_adr_001_ownership_violation_status_code_role_vs_record_gating, docs_decisions_adr_002_visit_ownership_derivation_single_ownership_rule, docs_decisions_adr_002_visit_ownership_derivation_404_relabelling, docs_decisions_adr_002_visit_ownership_derivation_symptom_parent_check, docs_trd_error_handling [EXTRACTED 1.00]

## Communities (146 total, 26 thin omitted)

### Community 0 - "User"
Cohesion: 0.15
Nodes (19): User model definitions., User, Session, UUID, Open a clinical case for a patient the caller owns. The patient id came from…, Retrieve a visit by ID. Ownership violations read as 404., List a patient's visits, newest first., Return a patient's visit history ordered for trend comparison. This is the in-… (+11 more)

### Community 1 - "ValidationApplicationError"
Cohesion: 0.23
Nodes (21): Persist an analysis and advance the visit status in one transaction. Both…, ErrorResponse, The standard shape returned for API errors., ApplicationError, AuthenticationError, AuthorizationError, ConflictError, DatabaseError (+13 more)

### Community 2 - "EntityNotFoundError"
Cohesion: 0.07
Nodes (85): Payload used to record a symptom against a visit., Payload used to partially update a symptom., SymptomCreate, SymptomUpdate, Vital signs recorded at a visit. Persisted as JSON, so this schema is the only…, Payload used to partially update a visit. Deliberately has no ``symptoms``…, VisitUpdate, Vitals (+77 more)

### Community 3 - "build_providers"
Cohesion: 0.10
Nodes (26): AI orchestration. Layering rule: nothing in this package imports a repository…, The AI pipeline (TRD section 8, APP-FLOW section 5). Clinical Case -> Normalize…, EvidenceRetriever, ImagingStager, LLMClient, Protocol, The provider seam. This module is the entire surface AI-02 replaces. Everything…, Retrieves candidate literature for a clinical context. Implementations must… (+18 more)

### Community 4 - "patients.py"
Cohesion: 0.11
Nodes (34): get_patient_service(), Provide the configured patient service., create_patient(), delete_patient(), get_patient(), list_patients(), _paginated_response(), delete (+26 more)

### Community 5 - "Patient"
Cohesion: 0.14
Nodes (15): Patient, Patient model definitions., PatientRepository, Session, UUID, Patient persistence operations., Count active patients assigned to a doctor., Return the active patient with the given phone number, if any. (+7 more)

### Community 6 - "UserRole"
Cohesion: 0.24
Nodes (29): str, UserRole, PatientUpdate, PhoneNumber, A patient phone number., Payload used to partially update a patient., _create_payload(), _patient() (+21 more)

### Community 7 - "test_ai_staging.py"
Cohesion: 0.10
Nodes (41): Return a stage estimate for the supplied scan metadata., MockImagingStager, Deterministic stand-in for an MRI staging model (ADR-006). The stage estimate…, Deterministic stage estimate derived from the scan's checksum., Derive a stage, confidence and region breakdown from the checksum., detect_stage_trend(), datetime, UUID (+33 more)

### Community 8 - "cn"
Cohesion: 0.12
Nodes (23): PatientDetailPage(), ClinicianTrustCard(), InteractiveMriViewer(), RegionInfo, REGIONS, InteractivePipelineDemo(), ACCEPTED, MriDropzone() (+15 more)

### Community 9 - "reset-password/page.tsx"
Cohesion: 0.18
Nodes (15): AuthShell(), PasswordStrength(), Rule, RULES, Button, ButtonProps, Size, sizeClasses (+7 more)

### Community 10 - "get_current_active_user"
Cohesion: 0.13
Nodes (33): get_current_active_user(), get_scan_service(), get_visit_service(), Provide the configured scan service., Return the current user only when the account is active., Provide the configured visit service., add_symptom(), create_analysis() (+25 more)

### Community 11 - "build_backend_architecture_report.py"
Cohesion: 0.18
Nodes (31): Document, RGBColor, add_body(), add_bullets(), add_callout(), add_code(), add_cover(), add_field() (+23 more)

### Community 12 - "dependencies.py"
Cohesion: 0.19
Nodes (12): get_current_user(), Depends, Session, User, Reusable FastAPI dependencies for database and access control., Validate the bearer token and return its associated user., Create a dependency that permits only the supplied user roles., Require the current user to have the clinician role. (+4 more)

### Community 13 - "test_report_service.py"
Cohesion: 0.19
Nodes (27): One generated PDF report, snapshotting its source analysis. Never mutated after…, Report, _analysis(), _evidence(), _finding(), _patient(), Unit tests for ReportService. Two properties carry the weight, mirroring…, ADR-006 decision 6: sign-off gates the report. (+19 more)

### Community 14 - "patient_visits.py"
Cohesion: 0.09
Nodes (34): alias, create_visit(), get_visit_history(), list_patient_visits(), Depends, ge, get, le (+26 more)

### Community 15 - "UserService"
Cohesion: 0.15
Nodes (12): UserUpdate, Business logic for AI analysis of a clinical case. The ordering in…, BaseService, Shared service-layer infrastructure., Base service providing access to the repository., Public service-layer exports., Session, User (+4 more)

### Community 16 - "dashboard/page.tsx"
Cohesion: 0.11
Nodes (12): ACCENTS, AVATAR_PALETTES, hexToRgb01(), NeuralBackground(), PatientRow, PATIENTS, RadialGauge(), SCAN_VOLUME (+4 more)

### Community 17 - "interactive-pipeline-demo.tsx"
Cohesion: 0.13
Nodes (18): ConfidenceDial(), ConfidenceDialProps, CASESHOTS, SampleCase, Edge, EDGES, findNode(), NeuralNetwork() (+10 more)

### Community 18 - "web-page/package.json"
Cohesion: 0.04
Nodes (45): dependencies, axios, js-cookie, lucide-react, next, react, react-dom, zod (+37 more)

### Community 19 - "extractApiError"
Cohesion: 0.13
Nodes (16): load(), UploadPage(), onSubmit(), usePatients(), api, extractApiError(), TOKEN_COOKIE, loginSchema (+8 more)

### Community 20 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 21 - "frontend/package.json"
Cohesion: 0.08
Nodes (24): autoprefixer, axios, eslint, eslint-config-next, js-cookie, lucide-react, next, postcss (+16 more)

### Community 22 - "dependencies"
Cohesion: 0.12
Nodes (17): dependencies, axios, clsx, framer-motion, @hookform/resolvers, js-cookie, lucide-react, next (+9 more)

### Community 23 - "test_auth_api.py"
Cohesion: 0.19
Nodes (18): Raised when a unique user identity is already registered., UserAlreadyExistsError, _client(), _db_override(), TestClient, Integration-style contract tests for authentication endpoints., test_admin_can_create_user_without_returning_password(), test_clinician_cannot_create_users() (+10 more)

### Community 24 - "auth-provider.tsx"
Cohesion: 0.18
Nodes (12): body, display, metadata, mono, AuthContext, AuthContextValue, AuthProvider(), AuthTokens (+4 more)

### Community 25 - "create_access_token"
Cohesion: 0.21
Nodes (13): create_access_token(), decode_access_token(), hash_password(), Any, Password hashing and JSON Web Token helpers., Hash a plaintext password using the configured password context., Verify a plaintext password against a stored hash., Create a signed access token from the supplied claims. (+5 more)

### Community 26 - "AnalysisOrchestrator"
Cohesion: 0.08
Nodes (49): AnalysisOrchestrator, Re-attach evidence from the orchestrator's own retrieved set. A provider names…, Drop uncited candidates, then rank and trim. A ranked condition without a…, Describe what actually produced this analysis. Derived from every provider that…, Execute the pipeline and return validated, ranked output., Runs the pipeline for one clinical context., Run imaging staging for the current visit, and a trend across it. Symptoms…, ClinicalContext (+41 more)

### Community 27 - "ScanService"
Cohesion: 0.11
Nodes (17): Session, UUID, Scan persistence operations., Provide scan-specific queries in addition to common CRUD., Return the active scan attached to a visit, if any., ScanRepository, Session, UUID (+9 more)

### Community 28 - "ADR-006-mri-primary-with-symptoms-as-context.md"
Cohesion: 0.22
Nodes (10): AGENTS.md — NeuroONE Agent Operating Contract, Decision Record (ADR) Policy, Source-of-Truth Precedence, APP-FLOW — Application Flow, ADR-001 — Ownership Violations Return 404, Not 403, ADR-002 — Visit Ownership Derives From Parent Patient, NEUROONE-MVP-SCOPE — Locked Scope Definition, PRD — Product Definition & Requirements (+2 more)

### Community 29 - "AI Pipeline (Normalize → Context → Retrieve → Rank → LLM → Validate → Persist)"
Cohesion: 0.12
Nodes (16): Structured Clinical Input Contract, TEST Mode, backend/requirements.txt — Pinned Runtime Dependencies, backend/requirements-dev.txt — Test Dependencies (pytest, pytest-asyncio, httpx), AI Flow, Case Flow, Primary Flow (Login → Dashboard → … → Report), Demo-Ready MVP Definition (+8 more)

### Community 30 - "Security and Privacy Rules"
Cohesion: 0.17
Nodes (12): Security and Privacy Rules, api service (FastAPI backend), db service (postgres:16-alpine), Health-Gated Service Startup, Enumeration-Resistant 404 for PHI-Adjacent Records, 404 Re-Labelling / Identifier Masking, Symptom-Belongs-To-Visit Verification, Demo Data Assumption (synthetic, not real PHI) (+4 more)

### Community 31 - "test_ai_live_llm.py"
Cohesion: 0.07
Nodes (84): MockEvidenceRetriever, _normalize(), Deterministic stand-in for a literature retriever. Matches the query against a…, Keyword retriever over the frozen mock corpus., Return matching documents, most relevant first. An empty result is a legitimate…, What the orchestrator asks the retriever for., RetrievalQuery, _analyze() (+76 more)

### Community 32 - "Confirmed Roles (ADMIN, CLINICIAN; RECEPTIONIST deferred)"
Cohesion: 0.17
Nodes (13): V1 Scope Guard, Auth/Crypto Dependency Set (passlib, bcrypt, python-jose, cryptography, email-validator), Role-Level 403 vs Per-Record 404 Split, AI-02 — Real LLM + RAG Swap-In, Confirmed Roles (ADMIN, CLINICIAN; RECEPTIONIST deferred), Administrator (user/role manager), Clinician (primary user), FR-01 Authentication (+5 more)

### Community 33 - "test_analysis_service.py"
Cohesion: 0.19
Nodes (34): A pointer into the patient's OWN visit history. Distinct from ``EvidenceRef``,…, TrendBasisRef, _candidate(), _deny_visit(), _evidence(), Unit tests for AnalysisService. Two properties carry the weight here: that a…, AGENTS.md 8.4.4: source metadata must survive to persistence., The masked 404 must not disclose the visit or the patient behind it. (+26 more)

### Community 34 - "ReportRepository"
Cohesion: 0.17
Nodes (19): Session, UUID, Report persistence operations., Provide report-specific queries in addition to common CRUD., Return an analysis's reports, newest first., Count an analysis's active reports., ReportRepository, _engine() (+11 more)

### Community 35 - "Standard API Response Envelope"
Cohesion: 0.25
Nodes (8): Centralized Error Handling Rules, CONTRIBUTING — NeuroONE Contributing Guide, Standard API Response Envelope, Coding Standards (type hints, PEP 8, services own business logic), Feature → API → Service → Repository → Model → Schema Flow, Centralized Error Translation, TRD Layered Architecture, PROGRESS_REPORT — NeuroONE Progress Report

### Community 36 - "JWT Authentication Flow"
Cohesion: 0.13
Nodes (15): Overridable Auth Service Providers, Open Convention — Transaction Boundary Ownership, Alembic Migration Policy, Team Repository Ownership Matrix, JWT Environment Configuration (HS256, 30-min access token), Single-Source Ownership Rule via Service Composition, Patient Soft-Delete Does Not Cascade to Visits, FR-02 Patient Management (+7 more)

### Community 37 - "r3f-canvas-scene.tsx"
Cohesion: 0.14
Nodes (10): R3fCanvasScene, FloatingParticles(), Particle, PARTICLES, StoryCard3D(), StoryCardProps, framer-motion, @react-three/drei (+2 more)

### Community 38 - "CASE-01 — Clinical Case / Symptom Domain"
Cohesion: 0.24
Nodes (10): Agent Definition of Done Checklist, Feature Branch Strategy, Contributing Definition of Done, Patient Flow (Patient Profile → Cases / History), AI-01 — Structured AI Contract with Mocked Providers, AUTH-01 — Real Auth Endpoints and Soft-Delete Fix, CASE-01 — Clinical Case / Symptom Domain, Early-Detection Design (+2 more)

### Community 39 - "Clinical Safety Boundary (non-negotiable)"
Cohesion: 0.11
Nodes (22): Extended AI Output Contract (Diagnosis with category and trend_basis), Clinical Safety Boundary (non-negotiable), MVP as Investor/Stakeholder Demo, Never Represent Output as Definitive Diagnosis, Report Completeness Contract, Evidence Flow (Retrieval → Ranking → Citation), Report Flow (Report Builder → PDF), Clinician Review Flow (+14 more)

### Community 40 - "RetrievedDocument"
Cohesion: 0.06
Nodes (44): _document(), MockCondition, Deterministic stand-in for a retrieval corpus and a reasoning model. Everything…, A rule mapping clinical findings to a candidate condition., Reason over the supplied context and evidence., LiveCandidatePayload, LiveLLMClient, Any (+36 more)

### Community 41 - "Mode Transition State Machine"
Cohesion: 0.14
Nodes (14): AI/RAG Failure Safety Rule, Layered Architecture Rules (Client → API → Service → Repository → PostgreSQL), BUILD Mode, DEBUG Mode, Mode Transition State Machine, PLAN Mode, Repository Inspection Rules, Task Planning Format (+6 more)

### Community 42 - "DiagnosisCandidate"
Cohesion: 0.11
Nodes (33): AnalysisResult, DiagnosisCandidate, An early-watch flag must point at the patient's own history. Note the…, Validated pipeline output, before persistence., One ranked possible condition. ``extra="forbid"`` is deliberate: a model that…, _candidate(), _evidence(), parametrize (+25 more)

### Community 43 - "test_report_api.py"
Cohesion: 0.19
Nodes (21): _client(), _db_override(), TestClient, Contract tests for the report endpoints. Beyond the usual status/shape…, ADR-006 decision 6: sign-off gates the report., AGENTS.md 8.2: not in the schema, not in API field naming., _report(), _snapshot() (+13 more)

### Community 44 - "1f74d19af1b8_widen_patient_email_and_promote_phone_.py"
Cohesion: 0.40
Nodes (4): downgrade(), Widen patients.email to 255 chars and give patient_phones the standard…, Restore the legacy integer-keyed patient_phones and 20-char email., upgrade()

### Community 45 - "8e72c1f4a9b0_replace_legacy_user_roles.py"
Cohesion: 0.40
Nodes (4): downgrade(), Rename DOCTOR and remove the deferred RECEPTIONIST role safely., Restore the legacy role enum., upgrade()

### Community 46 - "a3c7be51d904_create_visits_and_symptoms.py"
Cohesion: 0.40
Nodes (4): downgrade(), Drop the symptom and visit tables, and the enum type they created., Create the clinical case (visit) and symptom tables. The composite (patient_id,…, upgrade()

### Community 47 - "b8d41e2f7c53_make_deleted_at_timezone_aware.py"
Cohesion: 0.40
Nodes (4): downgrade(), Widen deleted_at from timestamp to timestamptz. No USING clause, deliberately.…, Narrow deleted_at back to a naive timestamp. Symmetric with upgrade(): the…, upgrade()

### Community 48 - "test_otp_service.py"
Cohesion: 0.26
Nodes (13): generate_and_send_otp(), _OtpEntry, Generates a 6-digit OTP, stores it, and emails it via Gmail SMTP., Checks a submitted OTP against the stored one. The code is only consumed…, verify_otp(), Tests for the OTP generation/verification helpers behind password reset., _stub_smtp(), test_code_is_burned_after_max_attempts() (+5 more)

### Community 49 - "test_analysis_api.py"
Cohesion: 0.15
Nodes (31): _analysis(), _client(), _db_override(), _evidence(), _finding(), TestClient, Contract tests for the analysis endpoints. Beyond the usual status/shape…, A consumer must be able to tell simulated evidence from live evidence. (+23 more)

### Community 50 - "visits.py"
Cohesion: 0.15
Nodes (20): _analysis_page(), list_analyses(), list_symptoms(), ge, le, Query, Visit endpoints. Item-level operations are flat rather than nested under the…, List the symptoms recorded against a visit. (+12 more)

### Community 51 - "middleware.ts"
Cohesion: 0.40
Nodes (3): AUTH_PAGES, config, PROTECTED_PREFIXES

### Community 56 - "BaseRepository"
Cohesion: 0.16
Nodes (12): BaseRepository, Session, UUID, Generic repository providing reusable CRUD operations. This base repository…, Soft-delete an entity. Marks the entity as deleted by setting the `is_deleted`…, Check whether a record exists. Returns True if an active record with the given…, Create a new database record and persist it. Adds the model instance to the…, Retrieve a single record by its unique identifier. Returns the entity if it… (+4 more)

### Community 60 - "PatientService"
Cohesion: 0.18
Nodes (16): PhoneNumber, PatientService, Patient, Session, User, UUID, List patients, scoped to the caller's role. CLINICIAN always sees only their…, Return every patient the caller may triage, unpaginated. Mirrors list_patients'… (+8 more)

### Community 74 - "LocalScanStorage"
Cohesion: 0.13
Nodes (14): Storage backends for artifacts that do not belong in the database., LocalScanStorage, Path, UUID, Storage for MRI scan bytes, outside the database (ADR-006 decision 5). A PDF…, Persist ``content`` and return its storage key., Filesystem-backed storage under a configured base directory. The concrete…, Tests for LocalScanStorage (ADR-006 decision 5). (+6 more)

### Community 75 - "detect_trends"
Cohesion: 0.08
Nodes (42): Normalize Input + Build Clinical Context (TRD section 8, stages 1-2). This is…, Map a Visit and its live symptoms into the AI-facing shape., _to_context_visit(), detect_trends(), _direction(), Cross-visit symptom trend detection. This is the mechanism behind AGENTS.md…, Normalized names of symptoms that are getting worse across visits. This is the…, Classify a severity series ordered oldest-first. (+34 more)

### Community 76 - "test_ai_mock_providers.py"
Cohesion: 0.14
Nodes (23): _analyze(), _context(), Tests for the mocked retriever and reasoner. Two properties matter most here.…, A stage estimate with no resolvable citation would be silently dropped., The fixture must not read as real literature., AGENTS.md 8.2: confidence is likelihood, never certainty., The property a seeded RNG or a canned fixture would not have., AGENTS.md 8.1: schema-valid deterministic results. (+15 more)

### Community 77 - "get_db"
Cohesion: 0.11
Nodes (31): get_analysis_service(), get_db(), get_report_service(), Provide the configured analysis service., Provide the configured report service., Provide a database session and always close it after the request., create_report(), get_analysis() (+23 more)

### Community 78 - "build_clinical_context"
Cohesion: 0.21
Nodes (21): _age_years(), build_clinical_context(), date, Whole years, so a date of birth never reaches the reasoning layer., Assemble the context the AI pipeline reasons over. ``prior_visits`` must be…, _patient(), Tests for the ORM -> ClinicalContext normalize stage. The PHI-minimization…, The current severity is part of the trajectory, not outside it. (+13 more)

### Community 79 - "VisitRepository"
Cohesion: 0.28
Nodes (17): Provide visit-specific queries in addition to common CRUD operations., VisitRepository, _engine(), Real-database tests for cross-visit history retrieval. These run against SQLite…, The loader criteria, not just the read path, must filter soft deletes., Regression guard for the N+1 the selectinload exists to prevent. One SELECT for…, test_get_by_patient_paginates_and_filters_by_status(), test_get_with_symptoms_hides_soft_deleted_visits() (+9 more)

### Community 80 - "AuthService"
Cohesion: 0.10
Nodes (27): TokenPayload, AuthService, User, Authenticate a user and issue an access token directly (no OTP step)., Verify a plaintext password against a stored hash., Hash a plaintext password., Create an access token for a user., Validate an access token and return its payload. (+19 more)

### Community 81 - "ADR-003: AI Analysis Contract and the Mocked-Provider Seam"
Cohesion: 0.14
Nodes (14): Addendum: evidence-resolution correction (pre-`REPORT-01`), ADR-003: AI Analysis Contract and the Mocked-Provider Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact (+6 more)

### Community 82 - "report_service.py"
Cohesion: 0.12
Nodes (34): Render a complete, multi-page clinical report PDF. Raises whatever ReportLab…, render(), Clinical report contract (FR-07, ADR-004). ``ReportSnapshot`` is exactly what…, The patient/case identification FR-07 requires a report to carry., One clinical input as recorded for the visit (FR-03)., The clinical case the analysis was run against., A citation as it must appear in the PDF (FR-05/06)., Everything the renderer may draw on. Nothing else reaches the PDF. (+26 more)

### Community 83 - "REPORT-01D — Frontend Requirements & Backend Mapping Checklist"
Cohesion: 0.12
Nodes (17): 0. Baseline finding: this is not a "reconcile," it's mostly new pages, 1. Auth — smaller surface than the current pages assume, 2. Patients, 3. Clinical Case (Visit) + Symptoms, 4. AI Analysis + Differential Diagnosis + Evidence, 5. Clinician Review → PDF Report, 6. Cross-cutting: error handling contract, 7. Explicit non-goals (do not build these) (+9 more)

### Community 84 - "test_deleted_at_timezone_migration.py"
Cohesion: 0.43
Nodes (6): _load_migration(), Regression tests for the deleted_at timezone migration., test_downgrade_restores_naive_timestamps(), test_migration_chains_from_case_01(), test_upgrade_uses_implicit_timezone_cast(), ModuleType

### Community 85 - "Visit"
Cohesion: 0.27
Nodes (7): Persisted AI analysis, its ranked findings, and their citations. Naming is…, Immutable snapshot of a generated clinical report (ADR-004)., MRI scan metadata for a visit (ADR-006). The scan's bytes are not a column here…, Symptom model definitions., Clinical case / visit model definitions., A clinical case / visit belonging to a patient. Ownership is derived from the…, Visit

### Community 86 - "test_patients_api.py"
Cohesion: 0.30
Nodes (14): _client(), _db_override(), _patient(), TestClient, Integration-style contract tests for patient endpoints. Covers the ownership-…, test_clinician_cannot_create_patient_for_another_doctor(), test_delete_on_other_doctors_patient_is_404(), test_delete_own_patient_returns_204() (+6 more)

### Community 89 - "UserResponse"
Cohesion: 0.11
Nodes (20): Require the current user to have the administrator role., require_admin(), create_user(), Depends, post, Session, User, Administrator-only endpoints. (+12 more)

### Community 90 - "Analysis"
Cohesion: 0.05
Nodes (76): Analysis, AnalysisEvidence, AnalysisFinding, FindingCategory, Enum, str, One ranked candidate condition. Decision support, never a definitive diagnosis:…, One citation supporting one ranked finding. Scoped to a finding rather than to… (+68 more)

### Community 91 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+13 more)

### Community 92 - "ADR-005: Live LLM Provider Behind the AI-01 Seam"
Cohesion: 0.15
Nodes (13): ADR-005: Live LLM Provider Behind the AI-01 Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 93 - "get_triage_queue"
Cohesion: 0.13
Nodes (16): get_triage_service(), Provide the configured triage service., get_triage_queue(), Depends, ge, get, le, Query (+8 more)

### Community 94 - "ADR-004: Clinical Report Snapshot and Rendering"
Cohesion: 0.15
Nodes (13): ADR-004: Clinical Report Snapshot and Rendering, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 95 - "VisitStatus"
Cohesion: 0.17
Nodes (12): Enum, str, Lifecycle of a clinical case. ANALYZED is written by the AI pipeline (AI-01),…, VisitStatus, Session, UUID, Clinical case / visit persistence operations., Eager-load each visit's live symptoms in one extra query. selectinload rather… (+4 more)

### Community 96 - "BaseModel"
Cohesion: 0.13
Nodes (32): LiveReasoningPayload, The model's whole response. ``extra="forbid"`` is the structural half of the…, get_auth_service(), Provide the configured authentication service., forgot_password(), login(), Depends, get (+24 more)

### Community 97 - "b2b31bad27df_add_symptom_observation.py"
Cohesion: 0.40
Nodes (4): downgrade(), Add the clinician-entered observation field (FR-03). Nullable, so every…, Drop the observation column., upgrade()

### Community 98 - "c4e19a7b6d20_create_analyses_findings_and_evidence.py"
Cohesion: 0.40
Nodes (4): downgrade(), Drop the analysis tables and the enum type they created., Create the AI analysis tables. No drops. The abandoned Diagnosis and Rag stubs…, upgrade()

### Community 99 - "dcfbc7d5b2c9_create_reports.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create the reports table (ADR-004). No pdf_path and no binary PDF column: only…, Drop the reports table., upgrade()

### Community 100 - "UserRepository"
Cohesion: 0.17
Nodes (4): Enum, Session, UserRepository, Business logic for patient management.

### Community 101 - "Q: How are Alembic migrations and backend tests configured, and where should PR CI run pytest?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: How are Alembic migrations and backend tests configured, and where should PR CI run pytest?, Source Nodes

### Community 102 - "Q: The parallel AI-01 work is committed and pulled; plan our next work"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: The parallel AI-01 work is committed and pulled; plan our next work, Source Nodes

### Community 104 - "reports.py"
Cohesion: 0.27
Nodes (10): download_report_pdf(), get_report(), Depends, get, Session, UUID, Report item endpoints. Flat rather than nested under the analysis: a report id…, Retrieve one report's metadata. Ownership violations read as 404. (+2 more)

### Community 105 - "Base"
Cohesion: 0.22
Nodes (7): Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), Database engine and session configuration., Base, DeclarativeBase

### Community 106 - "seed"
Cohesion: 0.67
Nodes (3): main(), Seed a demo patient whose history contains a multi-visit trend. AGENTS.md…, seed()

### Community 107 - "NeuroOne Frontend — Redesign Checklist"
Cohesion: 0.14
Nodes (13): Account & Settings, Admin, Auth, Clinical Input, Design Foundations, Diagnosis & Explainability, Engineering & Cross-Cutting, Information Architecture & Nav (+5 more)

### Community 108 - "test_scan_service.py"
Cohesion: 0.34
Nodes (16): _deny_visit(), Unit tests for ScanService (ADR-006). Mirrors test_report_service.py's shape:…, ADR-006 decision 2: one scan per visit., _service(), test_a_second_scan_on_the_same_visit_is_a_conflict_and_cleans_up_storage(), test_an_empty_file_is_rejected(), test_an_oversized_file_is_rejected(), test_get_scan_on_a_scanless_visit_is_a_missing_scan() (+8 more)

### Community 109 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, autoprefixer, eslint, eslint-config-next, postcss, tailwindcss, @types/js-cookie, @types/node (+4 more)

### Community 110 - "web-page/src/lib/api.ts"
Cohesion: 0.15
Nodes (8): api, ApiClient, ApiError, ApiResponse, extractApiError(), LoginResponse, OtpResponse, OtpVerifyResponse

### Community 111 - "ReportService"
Cohesion: 0.20
Nodes (11): Session, UUID, Build, render, and persist a new report for an analysis. Render-before-persist…, Retrieve one report by ID. The caller named only the report, so an…, List an analysis's reports, newest first., Re-render a report's PDF bytes from its immutable snapshot., Builds report snapshots, renders them, and persists the metadata., _render_or_fail() (+3 more)

### Community 112 - "get_user_service"
Cohesion: 0.40
Nodes (5): get_user_service(), Provide the configured user service., main(), Create NeuroONE's first administrator without a public endpoint., _value()

### Community 113 - "test_scan_api.py"
Cohesion: 0.28
Nodes (13): One MRI scan attached to a visit. Attaches to the Visit, not the Patient…, Scan, _client(), _db_override(), TestClient, Contract tests for the scan endpoints (ADR-006)., _scan(), test_getting_a_scan_on_a_scanless_visit_is_404() (+5 more)

### Community 114 - "NeuroOne — Design System"
Cohesion: 0.20
Nodes (9): 1. Brand identity, 2. Color system, 3. Typography, 4. Login screen, 5. Open items, Brand (login screen, decorative panel, marketing surfaces), NeuroOne — Design System, Product (dashboard, forms, tables, reports) (+1 more)

### Community 115 - "ReportFindingSnapshot"
Cohesion: 0.28
Nodes (12): _build_story(), _draw_footer(), _finding_label(), _p(), Render a ReportSnapshot into a complete clinical report PDF (ADR-004). A pure…, Escape Platypus markup and fall back for characters base14 can't render.…, _render_finding(), _safe() (+4 more)

### Community 116 - "NeuroONE Frontend Redesign"
Cohesion: 0.25
Nodes (7): Account-flow handoff, Design boundaries, Design implementation, Files in this change, NeuroONE Frontend Redesign, Preview, Required product journey

### Community 117 - "Symptom"
Cohesion: 0.18
Nodes (10): A neurological symptom recorded against a clinical case., Symptom, Session, UUID, Symptom persistence operations., Provide symptom-specific queries in addition to common CRUD operations., Return a visit's active symptoms in recording order., Count a visit's active symptoms. (+2 more)

### Community 118 - "verify-otp/page.tsx"
Cohesion: 0.27
Nodes (5): VerifyOtpForm(), OtpInput(), commit(), handleChange(), handlePaste()

### Community 119 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

### Community 120 - "web-page/src/lib/validation.ts"
Cohesion: 0.40
Nodes (4): LoginFormData, loginSchema, OtpFormData, otpSchema

### Community 121 - "useAuth"
Cohesion: 0.18
Nodes (10): DashboardLayout(), NAV_ITEMS, ForgotPasswordPage(), LoginForm(), handleOtpLogin(), handleSubmit(), validate(), ResetPasswordForm() (+2 more)

### Community 122 - "web-page/.eslintrc.json"
Cohesion: 0.50
Nodes (3): extends, next/core-web-vitals, root

### Community 124 - "DashboardPage"
Cohesion: 1.00
Nodes (3): DashboardPage(), SortHeader(), toggleSort()

### Community 134 - "frontend/src/lib/validation.ts"
Cohesion: 0.15
Nodes (12): DISPOSABLE_DOMAINS, emailSchema, ForgotPasswordInput, forgotPasswordSchema, OtpInput, PatientIntakeInput, patientIntakeSchema, ResetPasswordInput (+4 more)

### Community 135 - "FastAPI"
Cohesion: 0.23
Nodes (10): Top-level API router., Tests for soft-delete semantics and transactional failure handling., RepositoryRecord, _session(), test_create_rolls_back_and_raises_controlled_database_error(), test_mid_write_failure_persists_nothing_and_translates_database_error(), test_soft_deleted_records_are_hidden_unless_explicitly_requested(), parametrize (+2 more)

### Community 136 - "test_triage_api.py"
Cohesion: 0.30
Nodes (10): _client(), _db_override(), _entry(), TestClient, Contract tests for the triage endpoint (ADR-006)., FR-04: no stat tile, no aggregate confidence number., test_an_entry_carries_no_field_that_frames_output_as_a_measurement(), test_default_pagination_is_page_one() (+2 more)

### Community 137 - "_error_response"
Cohesion: 0.31
Nodes (11): _error_response(), http_exception_handler(), Exception, request_validation_error_handler(), unhandled_error_handler(), validation_error_handler(), JSONResponse, Request (+3 more)

### Community 138 - "ADR-006: MRI Becomes a Primary Input, With Symptoms as Context"
Cohesion: 0.18
Nodes (11): ADR-006: MRI Becomes a Primary Input, With Symptoms as Context, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Problem (+3 more)

### Community 139 - "likelihood_band_for"
Cohesion: 0.27
Nodes (8): FindingResponse, likelihood_band_for(), Confidence-tiered output (section 8.3). This is what UI copy and the PDF should…, A ranked candidate as returned by the API., Derived from confidence, never read from the row., Tier a confidence value (AGENTS.md section 8.3). Derived, never stored: a…, computed_field, LikelihoodBand

### Community 140 - "schemas/symptom.py"
Cohesion: 0.28
Nodes (6): field_validator, Symptom request and response schemas., A whitespace-only observation is the same as no observation, rejected rather…, Fields shared by symptom request and response schemas., _reject_blank(), SymptomBase

### Community 141 - "common.py"
Cohesion: 0.25
Nodes (6): MessageResponse, Pagination, Schemas shared across application features., Pagination metadata returned with collection responses., A simple response containing a human-readable message., Helpers for consistent API responses.

### Community 142 - "app/main.py"
Cohesion: 0.40
Nodes (4): health(), get, root(), Compatibility entry point for running ``uvicorn main:app``.

### Community 143 - "14056b8ec27d_create_scans.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create the scans table (ADR-006). No image bytes column: only the storage…, Drop the scans table., upgrade()

### Community 144 - "7544ad0b1ed6_add_analysis_sign_off.py"
Cohesion: 0.40
Nodes (4): downgrade(), Add clinician sign-off columns to analyses (ADR-006 decision 6). Both nullable…, Drop the sign-off columns., upgrade()

### Community 145 - "ScanResponse"
Cohesion: 0.50
Nodes (3): Scan wire schema (ADR-006). No storage_key: that is an internal reference into…, A persisted scan's metadata, as returned by the API., ScanResponse

## Ambiguous Edges - Review These
- `AI Pipeline (Normalize → Context → Retrieve → Rank → LLM → Validate → Persist)` → `backend/requirements.txt — Pinned Runtime Dependencies`  [AMBIGUOUS]
  backend/requirements.txt · relation: conceptually_related_to
- `FR-01 Authentication` → `OTP Email Verification Flow`  [AMBIGUOUS]
  frontend/README.md · relation: conceptually_related_to
- `Server-Side Authorization (ADMIN, CLINICIAN)` → `Middleware-Based Route Protection`  [AMBIGUOUS]
  frontend/README.md · relation: conceptually_related_to
- `Standard API Response Envelope` → `Assumed Backend API Contract`  [AMBIGUOUS]
  frontend/README.md · relation: conceptually_related_to
- `V1 Exclusions (MRI, uploaded reports, autonomous diagnosis, automated treatment)` → `MRI Upload + Prediction Polling`  [AMBIGUOUS]
  frontend/README.md · relation: conceptually_related_to
- `V1 Exclusions (MRI, uploaded reports, autonomous diagnosis, automated treatment)` → `MRI-Based Neurodegenerative Disease Analysis (marketing claim)`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to
- `MRI-Based Neurodegenerative Disease Analysis (marketing claim)` → `Clinical Safety Boundary (non-negotiable)`  [AMBIGUOUS]
  AGENTS.md · relation: conceptually_related_to
- `Container Setup Unusable (empty compose, placeholder Dockerfile)` → `docker-compose.yml — Local Dev Stack`  [AMBIGUOUS]
  reports/PROGRESS_REPORT.md · relation: references

## Knowledge Gaps
- **321 isolated node(s):** `extends`, `next/core-web-vitals`, `nextConfig`, `name`, `version` (+316 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 968 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `AI Pipeline (Normalize → Context → Retrieve → Rank → LLM → Validate → Persist)` and `backend/requirements.txt — Pinned Runtime Dependencies`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `FR-01 Authentication` and `OTP Email Verification Flow`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Server-Side Authorization (ADMIN, CLINICIAN)` and `Middleware-Based Route Protection`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Standard API Response Envelope` and `Assumed Backend API Contract`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `V1 Exclusions (MRI, uploaded reports, autonomous diagnosis, automated treatment)` and `MRI Upload + Prediction Polling`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `V1 Exclusions (MRI, uploaded reports, autonomous diagnosis, automated treatment)` and `MRI-Based Neurodegenerative Disease Analysis (marketing claim)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `MRI-Based Neurodegenerative Disease Analysis (marketing claim)` and `Clinical Safety Boundary (non-negotiable)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._