# Graph Report - NeuroOne-V1  (2026-09-11)

## Corpus Check
- 179 files · ~92,978 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1994 nodes · 5105 edges · 115 communities (89 shown, 21 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 500 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `422084fb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- User
- BaseRepository
- test_visit_service.py
- AnalysisOrchestrator
- patients.py
- Patient
- UserRole
- EntityNotFoundError
- cn
- react
- get_db
- build_backend_architecture_report.py
- get_current_user
- build_providers
- patient_visits.py
- UserService
- dashboard/page.tsx
- interactive-pipeline-demo.tsx
- test_report_service.py
- upload/page.tsx
- compilerOptions
- package.json
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
- ReportRepository
- Repository Inspection Rules
- JWT Authentication Flow
- neural-network.tsx
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
- VerifyOtpForm
- middleware.ts
- AnalysisService
- test_health.py
- .eslintrc.json
- next.config.mjs
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
- RetrievedDocument
- detect_trends
- test_ai_mock_providers.py
- v1/analysis.py
- build_clinical_context
- VisitRepository
- AuthService
- ADR-003: AI Analysis Contract and the Mocked-Provider Seam
- report_service.py
- REPORT-01D — Frontend Requirements & Backend Mapping Checklist
- test_deleted_at_timezone_migration.py
- BaseModel
- test_patients_api.py
- corpus/__init__.py
- CLAUDE.md
- UserResponse
- MockLLMClient
- trends.py
- ADR-005: Live LLM Provider Behind the AI-01 Seam
- Security and Privacy Rules
- ADR-004: Clinical Report Snapshot and Rendering
- NeuroOne — Design System
- v1/auth.py
- b2b31bad27df_add_symptom_observation.py
- c4e19a7b6d20_create_analyses_findings_and_evidence.py
- dcfbc7d5b2c9_create_reports.py
- UserRepository
- Q: How are Alembic migrations and backend tests configured, and where should PR CI run pytest?
- Q: The parallel AI-01 work is committed and pulled; plan our next work
- reports/__init__.py
- ReportService
- env.py
- seed
- NeuroOne Frontend — Redesign Checklist
- ContextVisit
- devDependencies
- orchestrator.py
- .verify_credentials
- get_user_service
- schemas/patient.py
- test_retriever_prioritizes_trusted_tiers_on_equal_matches

## God Nodes (most connected - your core abstractions)
1. `User` - 100 edges
2. `EntityNotFoundError` - 79 edges
3. `UserRole` - 74 edges
4. `BaseModel` - 68 edges
5. `Visit` - 54 edges
6. `VisitService` - 53 edges
7. `VisitStatus` - 48 edges
8. `get_db()` - 44 edges
9. `AuthService` - 44 edges
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

## Communities (115 total, 21 thin omitted)

### Community 0 - "User"
Cohesion: 0.15
Nodes (19): User model definitions., User, Session, UUID, Open a clinical case for a patient the caller owns. The patient id came from…, Retrieve a visit by ID. Ownership violations read as 404., List a patient's visits, newest first., Return a patient's visit history ordered for trend comparison. This is the in-… (+11 more)

### Community 1 - "BaseRepository"
Cohesion: 0.07
Nodes (57): Top-level API router., health(), get, root(), BaseRepository, Session, UUID, Generic repository providing reusable CRUD operations. This base repository… (+49 more)

### Community 2 - "test_visit_service.py"
Cohesion: 0.07
Nodes (73): Enum, str, Lifecycle of a clinical case. ANALYZED is written by the AI pipeline (AI-01),…, VisitStatus, Public schema exports., field_validator, Symptom request and response schemas., A whitespace-only observation is the same as no observation, rejected rather… (+65 more)

### Community 3 - "AnalysisOrchestrator"
Cohesion: 0.13
Nodes (28): AnalysisOrchestrator, Re-attach evidence from the orchestrator's own retrieved set. A provider names…, Drop uncited candidates, then rank and trim. A ranked condition without a…, Describe what actually produced this analysis. Derived from both providers…, Execute the pipeline and return validated, ranked output., Runs the pipeline for one clinical context., What the LLM provider returns. Validated at the seam, so a real provider in…, ReasoningResult (+20 more)

### Community 4 - "patients.py"
Cohesion: 0.15
Nodes (27): get_patient_service(), Provide the configured patient service., create_patient(), delete_patient(), get_patient(), list_patients(), _paginated_response(), delete (+19 more)

### Community 5 - "Patient"
Cohesion: 0.16
Nodes (13): Patient, Patient model definitions., PatientRepository, Session, UUID, Patient persistence operations., Return the active patient with the given email address, if any., Provide patient-specific queries in addition to common CRUD operations. (+5 more)

### Community 6 - "UserRole"
Cohesion: 0.22
Nodes (30): Enum, str, UserRole, PatientUpdate, PhoneNumber, A patient phone number., Payload used to partially update a patient., _create_payload() (+22 more)

### Community 7 - "EntityNotFoundError"
Cohesion: 0.08
Nodes (56): EntityNotFoundError, Any, Raised when a requested entity does not exist., _client(), _db_override(), TestClient, Contract tests for the report endpoints. Beyond the usual status/shape…, AGENTS.md 8.2: not in the schema, not in API field naming. (+48 more)

### Community 8 - "cn"
Cohesion: 0.11
Nodes (21): DashboardLayout(), NAV_ITEMS, ClinicianTrustCard(), InteractiveMriViewer(), RegionInfo, REGIONS, InteractivePipelineDemo(), ACCEPTED (+13 more)

### Community 9 - "react"
Cohesion: 0.13
Nodes (21): ForgotPasswordPage(), LoginForm(), ResetPasswordForm(), SignupPage(), useAuth(), AuthShell(), PasswordStrength(), Rule (+13 more)

### Community 10 - "get_db"
Cohesion: 0.11
Nodes (47): get_current_active_user(), get_db(), get_visit_service(), Return the current user only when the account is active., Provide a database session and always close it after the request., Provide the configured visit service., add_symptom(), _analysis_page() (+39 more)

### Community 11 - "build_backend_architecture_report.py"
Cohesion: 0.18
Nodes (31): Document, Path, RGBColor, add_body(), add_bullets(), add_callout(), add_code(), add_cover() (+23 more)

### Community 12 - "get_current_user"
Cohesion: 0.16
Nodes (14): get_current_user(), Depends, Session, User, Validate the bearer token and return its associated user., Create a dependency that permits only the supplied user roles., Require the current user to have the administrator role., Require the current user to have the clinician role. (+6 more)

### Community 13 - "build_providers"
Cohesion: 0.16
Nodes (13): AI orchestration. Layering rule: nothing in this package imports a repository…, EvidenceRetriever, LLMClient, The provider seam. This module is the entire surface AI-02 replaces. Everything…, Retrieves candidate literature for a clinical context. Implementations must…, Produces ranked candidate conditions from context plus evidence. The return…, Reason over the supplied context and evidence., AI provider implementations behind the base protocols. (+5 more)

### Community 14 - "patient_visits.py"
Cohesion: 0.12
Nodes (26): alias, create_visit(), get_visit_history(), list_patient_visits(), Depends, ge, get, le (+18 more)

### Community 15 - "UserService"
Cohesion: 0.16
Nodes (11): UserUpdate, BaseService, Shared service-layer infrastructure., Base service providing access to the repository., Public service-layer exports., Session, User, UUID (+3 more)

### Community 16 - "dashboard/page.tsx"
Cohesion: 0.10
Nodes (15): ACCENTS, AVATAR_PALETTES, DashboardPage(), SortHeader(), toggleSort(), hexToRgb01(), NeuralBackground(), PatientRow (+7 more)

### Community 17 - "interactive-pipeline-demo.tsx"
Cohesion: 0.19
Nodes (12): ConfidenceDial(), ConfidenceDialProps, CASESHOTS, SampleCase, RegionBars(), ApiError, AuthTokens, DiseaseLabel (+4 more)

### Community 18 - "test_report_service.py"
Cohesion: 0.22
Nodes (22): _analysis(), _evidence(), _finding(), _patient(), Unit tests for ReportService. Two properties carry the weight, mirroring…, The masked 404 must not disclose the analysis behind it., _service(), _symptom() (+14 more)

### Community 19 - "upload/page.tsx"
Cohesion: 0.18
Nodes (16): PatientDetailPage(), load(), UploadPage(), onSubmit(), Card(), CardBody(), CardHeader(), usePatients() (+8 more)

### Community 20 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 21 - "package.json"
Cohesion: 0.06
Nodes (29): name, private, scripts, build, dev, lint, start, version (+21 more)

### Community 22 - "dependencies"
Cohesion: 0.12
Nodes (17): dependencies, axios, clsx, framer-motion, @hookform/resolvers, js-cookie, lucide-react, next (+9 more)

### Community 23 - "test_auth_api.py"
Cohesion: 0.22
Nodes (16): _client(), _db_override(), TestClient, Integration-style contract tests for authentication endpoints., test_admin_can_create_user_without_returning_password(), test_clinician_cannot_create_users(), test_duplicate_user_is_conflict(), test_expired_token_returns_controlled_401() (+8 more)

### Community 24 - "auth-provider.tsx"
Cohesion: 0.08
Nodes (27): body, display, metadata, mono, AuthContext, AuthContextValue, AuthProvider(), AuthTokens (+19 more)

### Community 25 - "create_access_token"
Cohesion: 0.21
Nodes (13): create_access_token(), decode_access_token(), hash_password(), Any, Password hashing and JSON Web Token helpers., Hash a plaintext password using the configured password context., Verify a plaintext password against a stored hash., Create a signed access token from the supplied claims. (+5 more)

### Community 26 - "test_ai_orchestrator.py"
Cohesion: 0.18
Nodes (22): _orchestrator(), Pipeline tests covering the AI test category (AGENTS.md section 10, TRD 12).…, AGENTS.md 8.1: never let simulated evidence read as clinically validated., AGENTS.md 8.4.6 / 18: citations traceable., AGENTS.md 8.1: the mock must simulate at least one multi-visit trend., The traceability requirement of section 18, asserted end to end., Without history there is no trend for an early_watch to point at., AGENTS.md 8.2: own history vs external literature are distinct. (+14 more)

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
Cohesion: 0.09
Nodes (72): MockEvidenceRetriever, Keyword retriever over the frozen mock corpus., _analyze(), _candidates(), _context(), _evidence(), _llm(), Tests for the live reasoning provider (AI-02 slice 1, ADR-005). A live model is… (+64 more)

### Community 32 - "FR-01 Authentication"
Cohesion: 0.33
Nodes (7): Auth/Crypto Dependency Set (passlib, bcrypt, python-jose, cryptography, email-validator), Role-Level 403 vs Per-Record 404 Split, FR-01 Authentication, Server-Side Authorization (ADMIN, CLINICIAN), Middleware-Based Route Protection, OTP Email Verification Flow, Frontend Stack (Next.js 14 App Router, TypeScript, Tailwind, RHF+Zod, Axios)

### Community 33 - "test_analysis_service.py"
Cohesion: 0.22
Nodes (30): A pointer into the patient's OWN visit history. Distinct from ``EvidenceRef``,…, TrendBasisRef, _candidate(), _deny_visit(), _evidence(), Unit tests for AnalysisService. Two properties carry the weight here: that a…, AGENTS.md 8.4.4: source metadata must survive to persistence., The masked 404 must not disclose the visit or the patient behind it. (+22 more)

### Community 34 - "ReportRepository"
Cohesion: 0.17
Nodes (19): Session, UUID, Report persistence operations., Provide report-specific queries in addition to common CRUD., Return an analysis's reports, newest first., Count an analysis's active reports., ReportRepository, _engine() (+11 more)

### Community 35 - "Repository Inspection Rules"
Cohesion: 0.15
Nodes (13): Layered Architecture Rules (Client → API → Service → Repository → PostgreSQL), Centralized Error Handling Rules, Repository Inspection Rules, CONTRIBUTING — NeuroONE Contributing Guide, Standard API Response Envelope, Coding Standards (type hints, PEP 8, services own business logic), Feature → API → Service → Repository → Model → Schema Flow, Backend Directory Layout (+5 more)

### Community 36 - "JWT Authentication Flow"
Cohesion: 0.20
Nodes (10): Overridable Auth Service Providers, Open Convention — Transaction Boundary Ownership, JWT Environment Configuration (HS256, 30-min access token), Single-Source Ownership Rule via Service Composition, FR-02 Patient Management, API Layer Rules, JWT Authentication Flow, Repository Layer Rules (+2 more)

### Community 37 - "neural-network.tsx"
Cohesion: 0.19
Nodes (9): FloatingParticles(), Particle, PARTICLES, Edge, EDGES, findNode(), NeuralNetwork(), Node (+1 more)

### Community 38 - "CASE-01 — Clinical Case / Symptom Domain"
Cohesion: 0.36
Nodes (9): Decision Record (ADR) Policy, Patient Flow (Patient Profile → Cases / History), ADR-001 — Ownership Violations Return 404, Not 403, ADR-002 — Visit Ownership Derives From Parent Patient, AI-01 — Structured AI Contract with Mocked Providers, AUTH-01 — Real Auth Endpoints and Soft-Delete Fix, CASE-01 — Clinical Case / Symptom Domain, Early-Detection Design (+1 more)

### Community 39 - "Clinical Safety Boundary (non-negotiable)"
Cohesion: 0.13
Nodes (17): Clinical Safety Boundary (non-negotiable), MVP as Investor/Stakeholder Demo, V1 Scope Guard, APP-FLOW V1 Boundary, AI-02 — Real LLM + RAG Swap-In, AI Phasing Decision (contract-real, provider-mocked), Mocked-AI Credibility Risk, REPORT-01 — PDF Assembly (+9 more)

### Community 40 - "ReasoningRequest"
Cohesion: 0.13
Nodes (16): LiveCandidatePayload, LiveLLMClient, LiveReasoningPayload, Any, Client, Live reasoning over an OpenAI-compatible chat-completions endpoint. The AI-02…, The model's whole response. ``extra="forbid"`` is the structural half of the…, Reasoner backed by a real model behind ``LLMClient``. (+8 more)

### Community 41 - "Mode Transition State Machine"
Cohesion: 0.14
Nodes (14): BUILD Mode, DEBUG Mode, Agent Definition of Done Checklist, Mode Transition State Machine, PLAN Mode, Task Planning Format, TEST Mode, Feature Branch Strategy (+6 more)

### Community 42 - "DiagnosisCandidate"
Cohesion: 0.11
Nodes (33): AnalysisResult, DiagnosisCandidate, An early-watch flag must point at the patient's own history. Note the…, Validated pipeline output, before persistence., One ranked possible condition. ``extra="forbid"`` is deliberate: a model that…, _candidate(), _evidence(), parametrize (+25 more)

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
Cohesion: 0.06
Nodes (69): AnalysisEvidence, AnalysisFinding, FindingCategory, Enum, str, One ranked candidate condition. Decision support, never a definitive diagnosis:…, One citation supporting one ranked finding. Scoped to a finding rather than to…, Whether a ranked condition sits in the differential or is flagged early.… (+61 more)

### Community 51 - "middleware.ts"
Cohesion: 0.40
Nodes (3): AUTH_PAGES, config, PROTECTED_PREFIXES

### Community 56 - "AnalysisService"
Cohesion: 0.19
Nodes (11): Analysis, One run of the AI pipeline against one clinical case. Re-running creates a new…, AnalysisService, Session, UUID, Business logic for AI analysis of a clinical case. The ordering in…, Run the AI pipeline for a visit and persist the result. Ownership violations…, Retrieve one analysis by ID. The caller named only the analysis, so a visit-… (+3 more)

### Community 60 - "PatientService"
Cohesion: 0.17
Nodes (18): PhoneNumber, PatientCreate, Payload used to create a patient., PatientService, Patient, Session, User, UUID (+10 more)

### Community 74 - "RetrievedDocument"
Cohesion: 0.13
Nodes (16): _document(), Deterministic stand-in for a retrieval corpus and a reasoning model. Everything…, Return documents relevant to the query, most relevant first. Returning an empty…, _normalize(), Deterministic stand-in for a literature retriever. Matches the query against a…, Return matching documents, most relevant first. An empty result is a legitimate…, EvidenceResponse, Structured differential-diagnosis contract (AGENTS.md section 8.2). Decision… (+8 more)

### Community 75 - "detect_trends"
Cohesion: 0.19
Nodes (21): detect_trends(), Detect per-symptom severity trends across a patient's visits. ``visits`` must…, Tests for cross-visit trend detection. A trend is what an early_watch flag…, symptoms: (name, severity) tuples., One visit per severity, 30 days apart, oldest-first., One observation is a snapshot, not a direction., Two rows on the same visit still span only one visit., _series() (+13 more)

### Community 76 - "test_ai_mock_providers.py"
Cohesion: 0.12
Nodes (26): _analyze(), _context(), Tests for the mocked retriever and reasoner. Two properties matter most here.…, The fixture must not read as real literature., An empty result is a legitimate outcome, not an exception., AGENTS.md 8.2: confidence is likelihood, never certainty., The property a seeded RNG or a canned fixture would not have., AGENTS.md 8.1: schema-valid deterministic results. (+18 more)

### Community 77 - "v1/analysis.py"
Cohesion: 0.14
Nodes (21): get_analysis_service(), Provide the configured analysis service., create_report(), get_analysis(), list_reports(), Depends, ge, get (+13 more)

### Community 78 - "build_clinical_context"
Cohesion: 0.21
Nodes (21): _age_years(), build_clinical_context(), date, Whole years, so a date of birth never reaches the reasoning layer., Assemble the context the AI pipeline reasons over. ``prior_visits`` must be…, _patient(), Tests for the ORM -> ClinicalContext normalize stage. The PHI-minimization…, The current severity is part of the trajectory, not outside it. (+13 more)

### Community 79 - "VisitRepository"
Cohesion: 0.09
Nodes (32): Session, UUID, Symptom persistence operations., Provide symptom-specific queries in addition to common CRUD operations., Return a visit's active symptoms in recording order., Count a visit's active symptoms., SymptomRepository, Session (+24 more)

### Community 80 - "AuthService"
Cohesion: 0.13
Nodes (23): TokenPayload, AuthService, Hash a plaintext password., Validate an access token and return its payload., Validate the reset code and set a new password., Business logic for authentication operations., InvalidCredentialsError, InvalidOtpError (+15 more)

### Community 81 - "ADR-003: AI Analysis Contract and the Mocked-Provider Seam"
Cohesion: 0.14
Nodes (14): Addendum: evidence-resolution correction (pre-`REPORT-01`), ADR-003: AI Analysis Contract and the Mocked-Provider Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact (+6 more)

### Community 82 - "report_service.py"
Cohesion: 0.07
Nodes (55): _build_story(), _draw_footer(), _finding_label(), _p(), Render a ReportSnapshot into a complete clinical report PDF (ADR-004). A pure…, Render a complete, multi-page clinical report PDF. Raises whatever ReportLab…, Escape Platypus markup and fall back for characters base14 can't render.…, render() (+47 more)

### Community 83 - "REPORT-01D — Frontend Requirements & Backend Mapping Checklist"
Cohesion: 0.11
Nodes (17): 0. Baseline finding: this is not a "reconcile," it's mostly new pages, 1. Auth — smaller surface than the current pages assume, 2. Patients, 3. Clinical Case (Visit) + Symptoms, 4. AI Analysis + Differential Diagnosis + Evidence, 5. Clinician Review → PDF Report, 6. Cross-cutting: error handling contract, 7. Explicit non-goals (do not build these) (+9 more)

### Community 84 - "test_deleted_at_timezone_migration.py"
Cohesion: 0.43
Nodes (6): _load_migration(), Regression tests for the deleted_at timezone migration., test_downgrade_restores_naive_timestamps(), test_migration_chains_from_case_01(), test_upgrade_uses_implicit_timezone_cast(), ModuleType

### Community 85 - "BaseModel"
Cohesion: 0.13
Nodes (18): Database engine and session configuration., Persisted AI analysis, its ranked findings, and their citations. Naming is…, Base, BaseModel, Base model definition., Immutable snapshot of a generated clinical report (ADR-004)., Symptom model definitions., A neurological symptom recorded against a clinical case. (+10 more)

### Community 86 - "test_patients_api.py"
Cohesion: 0.30
Nodes (14): _client(), _db_override(), _patient(), TestClient, Integration-style contract tests for patient endpoints. Covers the ownership-…, test_clinician_cannot_create_patient_for_another_doctor(), test_delete_on_other_doctors_patient_is_404(), test_delete_own_patient_returns_204() (+6 more)

### Community 89 - "UserResponse"
Cohesion: 0.14
Nodes (16): create_user(), Depends, post, Session, User, Administrator-only endpoints., Provision an ADMIN or CLINICIAN account., User request and response schemas. (+8 more)

### Community 90 - "MockLLMClient"
Cohesion: 0.19
Nodes (10): MockCondition, A rule mapping clinical findings to a candidate condition., MockLLMClient, Deterministic stand-in for the reasoning model. Scores the frozen condition…, Rank the condition rules against the supplied context and evidence., Rule-based reasoner over the frozen condition table., Highest recorded severity per symptom, across every visit., Build history references for the matched worsening symptoms. Every reference… (+2 more)

### Community 91 - "trends.py"
Cohesion: 0.15
Nodes (13): _direction(), normalize_symptom_name(), Cross-visit symptom trend detection. This is the mechanism behind AGENTS.md…, Normalized names of symptoms that are getting worse across visits. This is the…, Group key for a symptom, so "Tremor" and "tremor " are one series., Classify a severity series ordered oldest-first., worsening_symptom_names(), One observation of a symptom at one visit. Carries the real visits.id and… (+5 more)

### Community 92 - "ADR-005: Live LLM Provider Behind the AI-01 Seam"
Cohesion: 0.15
Nodes (13): ADR-005: Live LLM Provider Behind the AI-01 Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 93 - "Security and Privacy Rules"
Cohesion: 0.20
Nodes (10): AI/RAG Failure Safety Rule, Security and Privacy Rules, Failure Flows (AI/RAG, Database, Invalid Input), Enumeration-Resistant 404 for PHI-Adjacent Records, 404 Re-Labelling / Identifier Masking, Symptom-Belongs-To-Visit Verification, Demo Data Assumption (synthetic, not real PHI), Non-Functional Requirements (Security, Reliability, Maintainability, Traceability) (+2 more)

### Community 94 - "ADR-004: Clinical Report Snapshot and Rendering"
Cohesion: 0.14
Nodes (13): ADR-004: Clinical Report Snapshot and Rendering, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 95 - "NeuroOne — Design System"
Cohesion: 0.20
Nodes (9): 1. Brand identity, 2. Color system, 3. Typography, 4. Login screen, 5. Open items, Brand (login screen, decorative panel, marketing surfaces), NeuroOne — Design System, Product (dashboard, forms, tables, reports) (+1 more)

### Community 96 - "v1/auth.py"
Cohesion: 0.17
Nodes (21): get_auth_service(), Provide the configured authentication service., forgot_password(), login(), Depends, get, post, Session (+13 more)

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

### Community 104 - "ReportService"
Cohesion: 0.13
Nodes (23): get_report_service(), Reusable FastAPI dependencies for database and access control., Provide the configured report service., download_report_pdf(), get_report(), Depends, get, Session (+15 more)

### Community 105 - "env.py"
Cohesion: 0.40
Nodes (4): Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online()

### Community 106 - "seed"
Cohesion: 0.67
Nodes (3): main(), Seed a demo patient whose history contains a multi-visit trend. AGENTS.md…, seed()

### Community 107 - "NeuroOne Frontend — Redesign Checklist"
Cohesion: 0.14
Nodes (13): Account & Settings, Admin, Auth, Clinical Input, Design Foundations, Diagnosis & Explainability, Engineering & Cross-Cutting, Information Architecture & Nav (+5 more)

### Community 108 - "ContextVisit"
Cohesion: 0.21
Nodes (9): Normalize Input + Build Clinical Context (TRD section 8, stages 1-2). This is…, Map a Visit and its live symptoms into the AI-facing shape., _to_context_visit(), ContextSymptom, ContextVisit, Normalized clinical context supplied to the AI pipeline. This is the "Build…, A symptom as the AI layer sees it., A clinical case as the AI layer sees it. (+1 more)

### Community 109 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, autoprefixer, eslint, eslint-config-next, postcss, tailwindcss, @types/js-cookie, @types/node (+4 more)

### Community 110 - "orchestrator.py"
Cohesion: 0.24
Nodes (8): The AI pipeline (TRD section 8, APP-FLOW section 5). Clinical Case -> Normalize…, cap_evidence_per_candidate(), rank_candidates(), rank_evidence(), Rank Evidence (TRD section 8, stage 4). Real now and unchanged by AI-02:…, Order documents by relevance, then source trust, then recency. ``document_id``…, Order candidates by descending confidence, name breaking ties., Trim each candidate's citations to the configured maximum. Trimming never…

### Community 111 - ".verify_credentials"
Cohesion: 0.25
Nodes (5): User, Authenticate a user and issue an access token directly (no OTP step)., Verify a plaintext password against a stored hash., Create an access token for a user., Validates username/email + password and returns the User, without issuing a…

### Community 112 - "get_user_service"
Cohesion: 0.40
Nodes (5): get_user_service(), Provide the configured user service., main(), Create NeuroONE's first administrator without a public endpoint., _value()

### Community 113 - "schemas/patient.py"
Cohesion: 0.40
Nodes (5): PatientBase, PatientResponse, Patient request and response schemas., Fields shared by patient request and response schemas., Public patient data returned by the API.

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
- **216 isolated node(s):** `extends`, `next/core-web-vitals`, `nextConfig`, `name`, `version` (+211 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 759 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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