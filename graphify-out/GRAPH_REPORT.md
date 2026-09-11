# Graph Report - NeuroOne-V1  (2026-09-11)

## Corpus Check
- 201 files · ~157,029 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2149 nodes · 5260 edges · 134 communities (100 shown, 27 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 505 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c1fa3f39`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- User
- BaseRepository
- EntityNotFoundError
- AnalysisOrchestrator
- patients.py
- Patient
- UserRole
- test_visits_api.py
- cn
- reset-password/page.tsx
- get_current_active_user
- build_backend_architecture_report.py
- get_db
- build_providers
- list_patient_visits
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
- test_ai_orchestrator.py
- AI Output Contract (Diagnosis + Evidence)
- AGENTS.md — NeuroONE Agent Operating Contract
- AI Pipeline (Normalize → Context → Retrieve → Rank → LLM → Validate → Persist)
- SEC-01 — Security Housekeeping
- test_ai_live_llm.py
- FR-01 Authentication
- test_analysis_service.py
- test_report_service.py
- Repository Inspection Rules
- JWT Authentication Flow
- r3f-canvas-scene.tsx
- CASE-01 — Clinical Case / Symptom Domain
- Clinical Safety Boundary (non-negotiable)
- ReasoningRequest
- Mode Transition State Machine
- DiagnosisCandidate
- FR-07 Clinical Report
- 1f74d19af1b8_widen_patient_email_and_promote_phone_.py
- 8e72c1f4a9b0_replace_legacy_user_roles.py
- a3c7be51d904_create_visits_and_symptoms.py
- b8d41e2f7c53_make_deleted_at_timezone_aware.py
- test_otp_service.py
- test_analysis_api.py
- visits.py
- middleware.ts
- AnalysisService
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
- schemas/__init__.py
- detect_trends
- test_ai_mock_providers.py
- v1/analysis.py
- build_clinical_context
- VisitRepository
- AuthService
- ADR-003: AI Analysis Contract and the Mocked-Provider Seam
- ReportService
- REPORT-01D — Frontend Requirements & Backend Mapping Checklist
- test_deleted_at_timezone_migration.py
- FindingCategory
- test_patients_api.py
- corpus/__init__.py
- CLAUDE.md
- UserResponse
- AnalysisRepository
- compilerOptions
- ADR-005: Live LLM Provider Behind the AI-01 Seam
- Security and Privacy Rules
- ADR-004: Clinical Report Snapshot and Rendering
- Visit
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
- patient_service.py
- NeuroOne Frontend — Redesign Checklist
- Analysis
- devDependencies
- web-page/src/lib/api.ts
- Token
- get_user_service
- schemas/patient.py
- NeuroOne — Design System
- create_user
- NeuroONE Frontend Redesign
- .get_by_visit
- OtpInput
- scripts
- web-page/src/lib/validation.ts
- LoginForm
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

## God Nodes (most connected - your core abstractions)
1. `User` - 100 edges
2. `EntityNotFoundError` - 79 edges
3. `UserRole` - 74 edges
4. `BaseModel` - 71 edges
5. `Visit` - 54 edges
6. `VisitService` - 53 edges
7. `VisitStatus` - 48 edges
8. `AuthService` - 48 edges
9. `get_db()` - 46 edges
10. `PatientService` - 43 edges

## Surprising Connections (you probably didn't know these)
- `Milestone 2 — Deliver One Vertical Feature` --semantically_similar_to--> `PAT-01 — Authorized Patient CRUD Vertical Slice`  [INFERRED] [semantically similar]
  reports/PROGRESS_REPORT.md → docs/NEUROONE-MVP-SCOPE.md
- `Critical Risk — Tracked backend/.env` --conceptually_related_to--> `Security and Privacy Rules`  [INFERRED]
  reports/PROGRESS_REPORT.md → AGENTS.md
- `Assumed Backend API Contract` --conceptually_related_to--> `Standard API Response Envelope`  [AMBIGUOUS]
  frontend/README.md → CONTRIBUTING.md
- `TRD Layered Architecture` --semantically_similar_to--> `Feature → API → Service → Repository → Model → Schema Flow`  [INFERRED] [semantically similar]
  docs/TRD.md → CONTRIBUTING.md
- `MRI Upload + Prediction Polling` --semantically_similar_to--> `MRI-Based Neurodegenerative Disease Analysis (marketing claim)`  [INFERRED] [semantically similar]
  frontend/README.md → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **AI/RAG Evidence Traceability Chain** — docs_trd_ai_pipeline, docs_trd_rag_rules, docs_trd_ai_output_contract, docs_app_flow_evidence_flow, docs_prd_fr_06_explainability, docs_neuroone_mvp_scope_trend_basis [EXTRACTED 1.00]
- **MVP Acceptance Journey — Same Path Across Four Documents** — docs_prd_mvp_acceptance_journey, docs_app_flow_primary_flow, docs_neuroone_mvp_scope_demo_ready_definition, agents_test_mode, docs_trd_implementation_sequence [EXTRACTED 1.00]
- **Per-Record Ownership Enforcement Pattern (404 masking, derived one hop up)** — docs_decisions_adr_001_ownership_violation_status_code_enumeration_resistance, docs_decisions_adr_001_ownership_violation_status_code_role_vs_record_gating, docs_decisions_adr_002_visit_ownership_derivation_single_ownership_rule, docs_decisions_adr_002_visit_ownership_derivation_404_relabelling, docs_decisions_adr_002_visit_ownership_derivation_symptom_parent_check, docs_trd_error_handling [EXTRACTED 1.00]

## Communities (134 total, 27 thin omitted)

### Community 0 - "User"
Cohesion: 0.12
Nodes (24): A neurological symptom recorded against a clinical case., Symptom, User model definitions., User, Symptom persistence operations., Provide symptom-specific queries in addition to common CRUD operations., SymptomRepository, Session (+16 more)

### Community 1 - "BaseRepository"
Cohesion: 0.06
Nodes (58): Top-level API router., health(), get, root(), BaseRepository, Session, UUID, Generic repository providing reusable CRUD operations. This base repository… (+50 more)

### Community 2 - "EntityNotFoundError"
Cohesion: 0.07
Nodes (79): Payload used to record a symptom against a visit., Payload used to partially update a symptom., SymptomCreate, SymptomUpdate, _as_utc(), field_validator, Clinical case / visit request and response schemas., Normalize a naive datetime to UTC so ordering never mixes tz-awareness. (+71 more)

### Community 3 - "AnalysisOrchestrator"
Cohesion: 0.07
Nodes (34): _document(), Deterministic stand-in for a retrieval corpus and a reasoning model. Everything…, AI orchestration. Layering rule: nothing in this package imports a repository…, AnalysisOrchestrator, The AI pipeline (TRD section 8, APP-FLOW section 5). Clinical Case -> Normalize…, Re-attach evidence from the orchestrator's own retrieved set. A provider names…, Drop uncited candidates, then rank and trim. A ranked condition without a…, Describe what actually produced this analysis. Derived from both providers… (+26 more)

### Community 4 - "patients.py"
Cohesion: 0.15
Nodes (27): get_patient_service(), Provide the configured patient service., create_patient(), delete_patient(), get_patient(), list_patients(), _paginated_response(), delete (+19 more)

### Community 5 - "Patient"
Cohesion: 0.15
Nodes (13): Patient, Patient model definitions., PatientRepository, Session, UUID, Patient persistence operations., Return the active patient with the given email address, if any., Provide patient-specific queries in addition to common CRUD operations. (+5 more)

### Community 6 - "UserRole"
Cohesion: 0.26
Nodes (27): str, UserRole, PatientUpdate, Payload used to partially update a patient., _create_payload(), _patient(), Unit tests for PatientService ownership and doctor_id resolution rules., _service() (+19 more)

### Community 7 - "test_visits_api.py"
Cohesion: 0.15
Nodes (34): _client(), _db_override(), TestClient, Contract tests for the clinical case (visit) and symptom endpoints. Extends…, Only patient_id is exposed, so no endpoint can lazy-load per row., _symptom(), test_a_whitespace_only_observation_is_rejected(), test_add_symptom_returns_201() (+26 more)

### Community 8 - "cn"
Cohesion: 0.10
Nodes (27): DashboardLayout(), NAV_ITEMS, PatientDetailPage(), ConfidenceDial(), ConfidenceDialProps, ClinicianTrustCard(), InteractiveMriViewer(), RegionInfo (+19 more)

### Community 9 - "reset-password/page.tsx"
Cohesion: 0.12
Nodes (20): ForgotPasswordPage(), ResetPasswordForm(), SignupPage(), VerifyOtpForm(), useAuth(), AuthShell(), PasswordStrength(), Rule (+12 more)

### Community 10 - "get_current_active_user"
Cohesion: 0.13
Nodes (34): get_current_active_user(), get_visit_service(), Return the current user only when the account is active., Provide the configured visit service., add_symptom(), create_analysis(), delete_symptom(), delete_visit() (+26 more)

### Community 11 - "build_backend_architecture_report.py"
Cohesion: 0.18
Nodes (31): Document, Path, RGBColor, add_body(), add_bullets(), add_callout(), add_code(), add_cover() (+23 more)

### Community 12 - "get_db"
Cohesion: 0.18
Nodes (14): get_current_user(), get_db(), Depends, Session, User, Reusable FastAPI dependencies for database and access control., Validate the bearer token and return its associated user., Create a dependency that permits only the supplied user roles. (+6 more)

### Community 13 - "build_providers"
Cohesion: 0.18
Nodes (13): build_providers(), Client, Provider selection. The single place that maps configuration to concrete…, Return the (retriever, llm) pair for the configured provider., Settings, AI-02 slice 1 swaps reasoning only (ADR-005)., _settings(), test_build_providers_rejects_a_live_selection_without_a_key() (+5 more)

### Community 14 - "list_patient_visits"
Cohesion: 0.18
Nodes (17): alias, create_visit(), get_visit_history(), list_patient_visits(), Depends, ge, get, le (+9 more)

### Community 15 - "UserService"
Cohesion: 0.28
Nodes (6): UserUpdate, Session, User, UUID, Business logic for user management., UserService

### Community 16 - "dashboard/page.tsx"
Cohesion: 0.10
Nodes (13): ACCENTS, AVATAR_PALETTES, hexToRgb01(), NeuralBackground(), PatientRow, PATIENTS, RadialGauge(), SCAN_VOLUME (+5 more)

### Community 17 - "interactive-pipeline-demo.tsx"
Cohesion: 0.22
Nodes (12): CASESHOTS, InteractivePipelineDemo(), SampleCase, RegionBars(), ApiError, AuthTokens, DiseaseLabel, DiseaseStage (+4 more)

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
Cohesion: 0.22
Nodes (16): _client(), _db_override(), TestClient, Integration-style contract tests for authentication endpoints., test_admin_can_create_user_without_returning_password(), test_clinician_cannot_create_users(), test_duplicate_user_is_conflict(), test_expired_token_returns_controlled_401() (+8 more)

### Community 24 - "auth-provider.tsx"
Cohesion: 0.10
Nodes (22): body, display, metadata, mono, AuthContext, AuthContextValue, AuthProvider(), AuthTokens (+14 more)

### Community 25 - "create_access_token"
Cohesion: 0.21
Nodes (13): create_access_token(), decode_access_token(), hash_password(), Any, Password hashing and JSON Web Token helpers., Hash a plaintext password using the configured password context., Verify a plaintext password against a stored hash., Create a signed access token from the supplied claims. (+5 more)

### Community 26 - "test_ai_orchestrator.py"
Cohesion: 0.12
Nodes (40): AIError, _candidate(), _context(), _document(), _orchestrator(), Pipeline tests covering the AI test category (AGENTS.md section 10, TRD 12).…, AGENTS.md 8.1: never let simulated evidence read as clinically validated., AGENTS.md 8.4.6 / 18: citations traceable. (+32 more)

### Community 27 - "AI Output Contract (Diagnosis + Evidence)"
Cohesion: 0.47
Nodes (6): Extended AI Output Contract (Diagnosis with category and trend_basis), Never Represent Output as Definitive Diagnosis, early_watch Diagnosis Category, trend_basis (prior-visit traceability), FR-04 Differential Diagnosis, AI Output Contract (Diagnosis + Evidence)

### Community 28 - "AGENTS.md — NeuroONE Agent Operating Contract"
Cohesion: 0.28
Nodes (7): AGENTS.md — NeuroONE Agent Operating Contract, Source-of-Truth Precedence, APP-FLOW — Application Flow, NEUROONE-MVP-SCOPE — Locked Scope Definition, PRD — Product Definition & Requirements, TRD — Technical Requirements & Design, TRD Implementation Sequence

### Community 29 - "AI Pipeline (Normalize → Context → Retrieve → Rank → LLM → Validate → Persist)"
Cohesion: 0.20
Nodes (10): Structured Clinical Input Contract, backend/requirements.txt — Pinned Runtime Dependencies, backend/requirements-dev.txt — Test Dependencies (pytest, pytest-asyncio, httpx), AI Flow, Case Flow, FR-03 Clinical Input, FR-05 Literature Retrieval, AI Pipeline (Normalize → Context → Retrieve → Rank → LLM → Validate → Persist) (+2 more)

### Community 30 - "SEC-01 — Security Housekeeping"
Cohesion: 0.18
Nodes (11): Alembic Migration Policy, Team Repository Ownership Matrix, api service (FastAPI backend), db service (postgres:16-alpine), Health-Gated Service Startup, Patient Soft-Delete Does Not Cascade to Visits, SEC-01 — Security Housekeeping, Database Rules (UUIDs, timestamps, FKs, migrations, soft delete) (+3 more)

### Community 31 - "test_ai_live_llm.py"
Cohesion: 0.10
Nodes (64): _analyze(), _candidates(), _context(), _evidence(), _llm(), Tests for the live reasoning provider (AI-02 slice 1, ADR-005). A live model is…, A client whose model always answers with ``content``., One well-formed candidate payload, JSON-encoded as a model would. (+56 more)

### Community 32 - "FR-01 Authentication"
Cohesion: 0.33
Nodes (7): Auth/Crypto Dependency Set (passlib, bcrypt, python-jose, cryptography, email-validator), Role-Level 403 vs Per-Record 404 Split, FR-01 Authentication, Server-Side Authorization (ADMIN, CLINICIAN), Middleware-Based Route Protection, OTP Email Verification Flow, Frontend Stack (Next.js 14 App Router, TypeScript, Tailwind, RHF+Zod, Axios)

### Community 33 - "test_analysis_service.py"
Cohesion: 0.24
Nodes (28): _candidate(), _deny_visit(), _evidence(), Unit tests for AnalysisService. Two properties carry the weight here: that a…, AGENTS.md 8.4.4: source metadata must survive to persistence., The masked 404 must not disclose the visit or the patient behind it., _result(), _service() (+20 more)

### Community 34 - "test_report_service.py"
Cohesion: 0.09
Nodes (43): One generated PDF report, snapshotting its source analysis. Never mutated after…, Report, Session, UUID, Report persistence operations., Provide report-specific queries in addition to common CRUD., Return an analysis's reports, newest first., Count an analysis's active reports. (+35 more)

### Community 35 - "Repository Inspection Rules"
Cohesion: 0.15
Nodes (13): Layered Architecture Rules (Client → API → Service → Repository → PostgreSQL), Centralized Error Handling Rules, Repository Inspection Rules, CONTRIBUTING — NeuroONE Contributing Guide, Standard API Response Envelope, Coding Standards (type hints, PEP 8, services own business logic), Feature → API → Service → Repository → Model → Schema Flow, Backend Directory Layout (+5 more)

### Community 36 - "JWT Authentication Flow"
Cohesion: 0.20
Nodes (10): Overridable Auth Service Providers, Open Convention — Transaction Boundary Ownership, JWT Environment Configuration (HS256, 30-min access token), Single-Source Ownership Rule via Service Composition, FR-02 Patient Management, API Layer Rules, JWT Authentication Flow, Repository Layer Rules (+2 more)

### Community 37 - "r3f-canvas-scene.tsx"
Cohesion: 0.11
Nodes (15): R3fCanvasScene, FloatingParticles(), Particle, PARTICLES, StoryCard3D(), StoryCardProps, Edge, EDGES (+7 more)

### Community 38 - "CASE-01 — Clinical Case / Symptom Domain"
Cohesion: 0.36
Nodes (9): Decision Record (ADR) Policy, Patient Flow (Patient Profile → Cases / History), ADR-001 — Ownership Violations Return 404, Not 403, ADR-002 — Visit Ownership Derives From Parent Patient, AI-01 — Structured AI Contract with Mocked Providers, AUTH-01 — Real Auth Endpoints and Soft-Delete Fix, CASE-01 — Clinical Case / Symptom Domain, Early-Detection Design (+1 more)

### Community 39 - "Clinical Safety Boundary (non-negotiable)"
Cohesion: 0.13
Nodes (17): Clinical Safety Boundary (non-negotiable), MVP as Investor/Stakeholder Demo, V1 Scope Guard, APP-FLOW V1 Boundary, AI-02 — Real LLM + RAG Swap-In, AI Phasing Decision (contract-real, provider-mocked), Mocked-AI Credibility Risk, REPORT-01 — PDF Assembly (+9 more)

### Community 40 - "ReasoningRequest"
Cohesion: 0.08
Nodes (27): MockCondition, A rule mapping clinical findings to a candidate condition., Reason over the supplied context and evidence., LiveCandidatePayload, LiveLLMClient, Any, Client, Live reasoning over an OpenAI-compatible chat-completions endpoint. The AI-02… (+19 more)

### Community 41 - "Mode Transition State Machine"
Cohesion: 0.14
Nodes (14): BUILD Mode, DEBUG Mode, Agent Definition of Done Checklist, Mode Transition State Machine, PLAN Mode, Task Planning Format, TEST Mode, Feature Branch Strategy (+6 more)

### Community 42 - "DiagnosisCandidate"
Cohesion: 0.11
Nodes (34): AnalysisResult, DiagnosisCandidate, Structured differential-diagnosis contract (AGENTS.md section 8.2). Decision…, An early-watch flag must point at the patient's own history. Note the…, Validated pipeline output, before persistence., A pointer into the patient's OWN visit history. Distinct from ``EvidenceRef``,…, One ranked possible condition. ``extra="forbid"`` is deliberate: a model that…, TrendBasisRef (+26 more)

### Community 43 - "FR-07 Clinical Report"
Cohesion: 0.33
Nodes (6): Report Completeness Contract, Evidence Flow (Retrieval → Ranking → Citation), Report Flow (Report Builder → PDF), Clinician Review Flow, FR-06 Explainability, FR-07 Clinical Report

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
Nodes (29): _analysis(), _client(), _db_override(), _evidence(), _finding(), TestClient, Contract tests for the analysis endpoints. Beyond the usual status/shape…, A consumer must be able to tell simulated evidence from live evidence. (+21 more)

### Community 50 - "visits.py"
Cohesion: 0.07
Nodes (35): Patient-scoped visit endpoints. Collections nest under the patient, matching…, _visit_page(), _analysis_page(), Visit endpoints. Item-level operations are flat rather than nested under the…, _symptom_page(), AnalysisCreateRequest, AnalysisListResponse, AnalysisResponse (+27 more)

### Community 51 - "middleware.ts"
Cohesion: 0.40
Nodes (3): AUTH_PAGES, config, PROTECTED_PREFIXES

### Community 56 - "AnalysisService"
Cohesion: 0.17
Nodes (11): AnalysisEvidence, One citation supporting one ranked finding. Scoped to a finding rather than to…, AnalysisService, Session, UUID, Business logic for AI analysis of a clinical case. The ordering in…, Run the AI pipeline for a visit and persist the result. Ownership violations…, Retrieve one analysis by ID. The caller named only the analysis, so a visit-… (+3 more)

### Community 60 - "PatientService"
Cohesion: 0.19
Nodes (16): PatientCreate, Payload used to create a patient., PatientService, Patient, Session, User, UUID, List patients, scoped to the caller's role. CLINICIAN always sees only their… (+8 more)

### Community 74 - "schemas/__init__.py"
Cohesion: 0.25
Nodes (6): EvidenceResponse, A citation as returned by the API., EvidenceRef, Literature evidence schemas. ``EvidenceRef`` is exactly the three fields…, A citation attached to a ranked candidate. Traces to EXTERNAL literature. Not…, Public schema exports.

### Community 75 - "detect_trends"
Cohesion: 0.08
Nodes (43): Normalize Input + Build Clinical Context (TRD section 8, stages 1-2). This is…, Map a Visit and its live symptoms into the AI-facing shape., _to_context_visit(), detect_trends(), _direction(), normalize_symptom_name(), Cross-visit symptom trend detection. This is the mechanism behind AGENTS.md…, Normalized names of symptoms that are getting worse across visits. This is the… (+35 more)

### Community 76 - "test_ai_mock_providers.py"
Cohesion: 0.11
Nodes (29): MockEvidenceRetriever, Keyword retriever over the frozen mock corpus., _analyze(), _context(), Tests for the mocked retriever and reasoner. Two properties matter most here.…, The fixture must not read as real literature., An empty result is a legitimate outcome, not an exception., AGENTS.md 8.4: trusted medical sources are prioritized. (+21 more)

### Community 77 - "v1/analysis.py"
Cohesion: 0.13
Nodes (23): get_analysis_service(), get_report_service(), Provide the configured analysis service., Provide the configured report service., create_report(), get_analysis(), list_reports(), Depends (+15 more)

### Community 78 - "build_clinical_context"
Cohesion: 0.21
Nodes (21): _age_years(), build_clinical_context(), date, Whole years, so a date of birth never reaches the reasoning layer., Assemble the context the AI pipeline reasons over. ``prior_visits`` must be…, _patient(), Tests for the ORM -> ClinicalContext normalize stage. The PHI-minimization…, The current severity is part of the trajectory, not outside it. (+13 more)

### Community 79 - "VisitRepository"
Cohesion: 0.28
Nodes (17): Provide visit-specific queries in addition to common CRUD operations., VisitRepository, _engine(), Real-database tests for cross-visit history retrieval. These run against SQLite…, The loader criteria, not just the read path, must filter soft deletes., Regression guard for the N+1 the selectinload exists to prevent. One SELECT for…, test_get_by_patient_paginates_and_filters_by_status(), test_get_with_symptoms_hides_soft_deleted_visits() (+9 more)

### Community 80 - "AuthService"
Cohesion: 0.14
Nodes (21): TokenPayload, AuthService, Hash a plaintext password., Validate an access token and return its payload., Validate the reset code and set a new password., Business logic for authentication operations., InvalidCredentialsError, InvalidOtpError (+13 more)

### Community 81 - "ADR-003: AI Analysis Contract and the Mocked-Provider Seam"
Cohesion: 0.14
Nodes (14): Addendum: evidence-resolution correction (pre-`REPORT-01`), ADR-003: AI Analysis Contract and the Mocked-Provider Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact (+6 more)

### Community 82 - "ReportService"
Cohesion: 0.06
Nodes (63): _build_story(), _draw_footer(), _finding_label(), _p(), Render a ReportSnapshot into a complete clinical report PDF (ADR-004). A pure…, Render a complete, multi-page clinical report PDF. Raises whatever ReportLab…, Escape Platypus markup and fall back for characters base14 can't render.…, render() (+55 more)

### Community 83 - "REPORT-01D — Frontend Requirements & Backend Mapping Checklist"
Cohesion: 0.11
Nodes (17): 0. Baseline finding: this is not a "reconcile," it's mostly new pages, 1. Auth — smaller surface than the current pages assume, 2. Patients, 3. Clinical Case (Visit) + Symptoms, 4. AI Analysis + Differential Diagnosis + Evidence, 5. Clinician Review → PDF Report, 6. Cross-cutting: error handling contract, 7. Explicit non-goals (do not build these) (+9 more)

### Community 84 - "test_deleted_at_timezone_migration.py"
Cohesion: 0.43
Nodes (6): _load_migration(), Regression tests for the deleted_at timezone migration., test_downgrade_restores_naive_timestamps(), test_migration_chains_from_case_01(), test_upgrade_uses_implicit_timezone_cast(), ModuleType

### Community 85 - "FindingCategory"
Cohesion: 0.20
Nodes (9): FindingCategory, Enum, str, Persisted AI analysis, its ranked findings, and their citations. Naming is…, Whether a ranked condition sits in the differential or is flagged early.…, Immutable snapshot of a generated clinical report (ADR-004)., Symptom model definitions., Enum (+1 more)

### Community 86 - "test_patients_api.py"
Cohesion: 0.30
Nodes (14): _client(), _db_override(), _patient(), TestClient, Integration-style contract tests for patient endpoints. Covers the ownership-…, test_clinician_cannot_create_patient_for_another_doctor(), test_delete_on_other_doctors_patient_is_404(), test_delete_own_patient_returns_204() (+6 more)

### Community 89 - "UserResponse"
Cohesion: 0.16
Nodes (13): Administrator-only endpoints., User request and response schemas., UserBase, UserCreate, UserResponse, Session, Email a reset code if the address belongs to an active account. Always returns…, Email an OTP if the address belongs to an active account. Always returns… (+5 more)

### Community 90 - "AnalysisRepository"
Cohesion: 0.24
Nodes (25): AnalysisFinding, One ranked candidate condition. Decision support, never a definitive diagnosis:…, AnalysisRepository, Provide analysis-specific queries in addition to common CRUD., _analysis(), _engine(), _evidence(), _finding() (+17 more)

### Community 91 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+13 more)

### Community 92 - "ADR-005: Live LLM Provider Behind the AI-01 Seam"
Cohesion: 0.15
Nodes (13): ADR-005: Live LLM Provider Behind the AI-01 Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 93 - "Security and Privacy Rules"
Cohesion: 0.20
Nodes (10): AI/RAG Failure Safety Rule, Security and Privacy Rules, Failure Flows (AI/RAG, Database, Invalid Input), Enumeration-Resistant 404 for PHI-Adjacent Records, 404 Re-Labelling / Identifier Masking, Symptom-Belongs-To-Visit Verification, Demo Data Assumption (synthetic, not real PHI), Non-Functional Requirements (Security, Reliability, Maintainability, Traceability) (+2 more)

### Community 94 - "ADR-004: Clinical Report Snapshot and Rendering"
Cohesion: 0.14
Nodes (13): ADR-004: Clinical Report Snapshot and Rendering, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 95 - "Visit"
Cohesion: 0.17
Nodes (13): str, Lifecycle of a clinical case. ANALYZED is written by the AI pipeline (AI-01),…, A clinical case / visit belonging to a patient. Ownership is derived from the…, Visit, VisitStatus, Session, UUID, Clinical case / visit persistence operations. (+5 more)

### Community 96 - "BaseModel"
Cohesion: 0.13
Nodes (31): LiveReasoningPayload, The model's whole response. ``extra="forbid"`` is the structural half of the…, get_auth_service(), Provide the configured authentication service., forgot_password(), login(), Depends, get (+23 more)

### Community 97 - "b2b31bad27df_add_symptom_observation.py"
Cohesion: 0.40
Nodes (4): downgrade(), Add the clinician-entered observation field (FR-03). Nullable, so every…, Drop the observation column., upgrade()

### Community 98 - "c4e19a7b6d20_create_analyses_findings_and_evidence.py"
Cohesion: 0.40
Nodes (4): downgrade(), Drop the analysis tables and the enum type they created., Create the AI analysis tables. No drops. The abandoned Diagnosis and Rag stubs…, upgrade()

### Community 99 - "dcfbc7d5b2c9_create_reports.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create the reports table (ADR-004). No pdf_path and no binary PDF column: only…, Drop the reports table., upgrade()

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

### Community 106 - "patient_service.py"
Cohesion: 0.14
Nodes (11): PhoneNumber, Enum, BaseService, Shared service-layer infrastructure., Base service providing access to the repository., Public service-layer exports., Business logic for patient management., RepositoryType (+3 more)

### Community 107 - "NeuroOne Frontend — Redesign Checklist"
Cohesion: 0.14
Nodes (13): Account & Settings, Admin, Auth, Clinical Input, Design Foundations, Diagnosis & Explainability, Engineering & Cross-Cutting, Information Architecture & Nav (+5 more)

### Community 108 - "Analysis"
Cohesion: 0.18
Nodes (11): Analysis, One run of the AI pipeline against one clinical case. Re-running creates a new…, Session, UUID, Analysis persistence operations., Return the most recent analysis for a visit, if any., Eager-load findings and their citations in two extra queries. Every read path…, Persist an analysis and advance the visit status in one transaction. Both… (+3 more)

### Community 109 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, autoprefixer, eslint, eslint-config-next, postcss, tailwindcss, @types/js-cookie, @types/node (+4 more)

### Community 110 - "web-page/src/lib/api.ts"
Cohesion: 0.15
Nodes (8): api, ApiClient, ApiError, ApiResponse, extractApiError(), LoginResponse, OtpResponse, OtpVerifyResponse

### Community 111 - "Token"
Cohesion: 0.21
Nodes (7): Token, User, Authenticate a user and issue an access token directly (no OTP step)., Verify a plaintext password against a stored hash., Create an access token for a user., Verify credentials and OTP together, then issue an access token. This flow…, Validates username/email + password and returns the User, without issuing a…

### Community 112 - "get_user_service"
Cohesion: 0.40
Nodes (5): get_user_service(), Provide the configured user service., main(), Create NeuroONE's first administrator without a public endpoint., _value()

### Community 113 - "schemas/patient.py"
Cohesion: 0.29
Nodes (7): PatientBase, PatientResponse, PhoneNumber, Patient request and response schemas., A patient phone number., Fields shared by patient request and response schemas., Public patient data returned by the API.

### Community 114 - "NeuroOne — Design System"
Cohesion: 0.20
Nodes (9): 1. Brand identity, 2. Color system, 3. Typography, 4. Login screen, 5. Open items, Brand (login screen, decorative panel, marketing surfaces), NeuroOne — Design System, Product (dashboard, forms, tables, reports) (+1 more)

### Community 115 - "create_user"
Cohesion: 0.22
Nodes (9): Require the current user to have the administrator role., require_admin(), create_user(), Depends, post, Session, User, Provision an ADMIN or CLINICIAN account. (+1 more)

### Community 116 - "NeuroONE Frontend Redesign"
Cohesion: 0.25
Nodes (7): Account-flow handoff, Design boundaries, Design implementation, Files in this change, NeuroONE Frontend Redesign, Preview, Required product journey

### Community 117 - ".get_by_visit"
Cohesion: 0.43
Nodes (4): Session, UUID, Return a visit's active symptoms in recording order., Count a visit's active symptoms.

### Community 118 - "OtpInput"
Cohesion: 0.47
Nodes (4): OtpInput(), commit(), handleChange(), handlePaste()

### Community 119 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

### Community 120 - "web-page/src/lib/validation.ts"
Cohesion: 0.40
Nodes (4): LoginFormData, loginSchema, OtpFormData, otpSchema

### Community 121 - "LoginForm"
Cohesion: 0.83
Nodes (4): LoginForm(), handleOtpLogin(), handleSubmit(), validate()

### Community 122 - "web-page/.eslintrc.json"
Cohesion: 0.50
Nodes (3): extends, next/core-web-vitals, root

### Community 124 - "DashboardPage"
Cohesion: 1.00
Nodes (3): DashboardPage(), SortHeader(), toggleSort()

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
- **311 isolated node(s):** `extends`, `next/core-web-vitals`, `nextConfig`, `name`, `version` (+306 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 871 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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