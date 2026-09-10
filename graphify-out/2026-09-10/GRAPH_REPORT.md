# Graph Report - NeuroOne-V1  (2026-09-10)

## Corpus Check
- 155 files · ~65,382 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1590 nodes · 4025 edges · 90 communities (66 shown, 19 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 431 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4b4dbdfc`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- VisitService
- BaseRepository
- EntityNotFoundError
- detect_trends
- UserRole
- BaseModel
- get_current_active_user
- test_visits_api.py
- cn
- react
- add_symptom
- build_backend_architecture_report.py
- get_auth_service
- UserResponse
- patient_visits.py
- UserService
- dashboard/page.tsx
- interactive-pipeline-demo.tsx
- visits.py
- upload/page.tsx
- compilerOptions
- package.json
- dependencies
- test_auth_api.py
- auth-provider.tsx
- create_access_token
- test_ai_orchestrator.py
- Clinical Safety Boundary (non-negotiable)
- AGENTS.md — NeuroONE Agent Operating Contract
- AI Pipeline (Normalize → Context → Retrieve → Rank → LLM → Validate → Persist)
- Security and Privacy Rules
- test_analysis_api.py
- FR-01 Authentication
- test_analysis_service.py
- devDependencies
- JWT Authentication Flow
- Database Rules (UUIDs, timestamps, FKs, migrations, soft delete)
- neural-network.tsx
- CASE-01 — Clinical Case / Symptom Domain
- Confirmed Roles (ADMIN, CLINICIAN; RECEPTIONIST deferred)
- User
- Mode Transition State Machine
- DiagnosisCandidate
- FR-07 Clinical Report
- 1f74d19af1b8_widen_patient_email_and_promote_phone_.py
- 8e72c1f4a9b0_replace_legacy_user_roles.py
- a3c7be51d904_create_visits_and_symptoms.py
- b8d41e2f7c53_make_deleted_at_timezone_aware.py
- otp_service.py
- test_analysis_repository.py
- VerifyOtpForm
- middleware.ts
- RetrievedDocument
- test_health.py
- .eslintrc.json
- next.config.mjs
- AnalysisRepository
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
- AnalysisOrchestrator
- Patient
- test_ai_mock_providers.py
- get_analysis
- MockLLMClient
- Symptom
- AuthService
- ADR-003: AI Analysis Contract and the Mocked-Provider Seam
- v1/auth.py
- Base
- test_deleted_at_timezone_migration.py
- Agent Definition of Done Checklist
- .likelihood_band
- corpus/__init__.py
- CLAUDE.md
- Report

## God Nodes (most connected - your core abstractions)
1. `User` - 80 edges
2. `UserRole` - 69 edges
3. `EntityNotFoundError` - 66 edges
4. `BaseModel` - 59 edges
5. `VisitService` - 50 edges
6. `Visit` - 48 edges
7. `VisitStatus` - 45 edges
8. `PatientService` - 40 edges
9. `DiagnosisCandidate` - 37 edges
10. `get_db()` - 36 edges

## Surprising Connections (you probably didn't know these)
- `Milestone 2 — Deliver One Vertical Feature` --semantically_similar_to--> `PAT-01 — Authorized Patient CRUD Vertical Slice`  [INFERRED] [semantically similar]
  reports/PROGRESS_REPORT.md → docs/NEUROONE-MVP-SCOPE.md
- `MRI Upload + Prediction Polling` --semantically_similar_to--> `MRI-Based Neurodegenerative Disease Analysis (marketing claim)`  [INFERRED] [semantically similar]
  frontend/README.md → README.md
- `TRD Layered Architecture` --semantically_similar_to--> `Feature → API → Service → Repository → Model → Schema Flow`  [INFERRED] [semantically similar]
  docs/TRD.md → CONTRIBUTING.md
- `Agent Definition of Done Checklist` --semantically_similar_to--> `Contributing Definition of Done`  [INFERRED] [semantically similar]
  AGENTS.md → CONTRIBUTING.md
- `main()` --uses--> `UserRole`  [INFERRED]
  scripts/bootstrap_admin.py → backend/app/models/user.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **AI/RAG Evidence Traceability Chain** — docs_trd_ai_pipeline, docs_trd_rag_rules, docs_trd_ai_output_contract, docs_app_flow_evidence_flow, docs_prd_fr_06_explainability, docs_neuroone_mvp_scope_trend_basis [EXTRACTED 1.00]
- **MVP Acceptance Journey — Same Path Across Four Documents** — docs_prd_mvp_acceptance_journey, docs_app_flow_primary_flow, docs_neuroone_mvp_scope_demo_ready_definition, agents_test_mode, docs_trd_implementation_sequence [EXTRACTED 1.00]
- **Per-Record Ownership Enforcement Pattern (404 masking, derived one hop up)** — docs_decisions_adr_001_ownership_violation_status_code_enumeration_resistance, docs_decisions_adr_001_ownership_violation_status_code_role_vs_record_gating, docs_decisions_adr_002_visit_ownership_derivation_single_ownership_rule, docs_decisions_adr_002_visit_ownership_derivation_404_relabelling, docs_decisions_adr_002_visit_ownership_derivation_symptom_parent_check, docs_trd_error_handling [EXTRACTED 1.00]

## Communities (90 total, 19 thin omitted)

### Community 0 - "VisitService"
Cohesion: 0.12
Nodes (19): AnalysisService, Coordinates the AI pipeline and persists its output. Authorization is delegated…, Session, UUID, Open a clinical case for a patient the caller owns. The patient id came from…, Retrieve a visit by ID. Ownership violations read as 404., List a patient's visits, newest first., Return a patient's visit history ordered for trend comparison. This is the in-… (+11 more)

### Community 1 - "BaseRepository"
Cohesion: 0.06
Nodes (57): Top-level API router., health(), get, root(), BaseRepository, Session, UUID, Generic repository providing reusable CRUD operations. This base repository… (+49 more)

### Community 2 - "EntityNotFoundError"
Cohesion: 0.10
Nodes (59): str, Lifecycle of a clinical case. ANALYZED is written by the AI pipeline (AI-01),…, VisitStatus, Payload used to record a symptom against a visit., Payload used to partially update a symptom., SymptomCreate, SymptomUpdate, _as_utc() (+51 more)

### Community 3 - "detect_trends"
Cohesion: 0.06
Nodes (65): _age_years(), build_clinical_context(), Normalize Input + Build Clinical Context (TRD section 8, stages 1-2). This is…, Whole years, so a date of birth never reaches the reasoning layer., Map a Visit and its live symptoms into the AI-facing shape., Assemble the context the AI pipeline reasons over. ``prior_visits`` must be…, _to_context_visit(), AI orchestration. Layering rule: nothing in this package imports a repository… (+57 more)

### Community 4 - "UserRole"
Cohesion: 0.06
Nodes (73): Reusable FastAPI dependencies for database and access control., Create a dependency that permits only the supplied user roles., require_roles(), str, UserRole, PatientBase, PatientCreate, PatientUpdate (+65 more)

### Community 5 - "BaseModel"
Cohesion: 0.12
Nodes (22): FindingCategory, Enum, str, Persisted AI analysis, its ranked findings, and their citations. Naming is…, Whether a ranked condition sits in the differential or is flagged early.…, BaseModel, Base model definition., PhoneNumber (+14 more)

### Community 6 - "get_current_active_user"
Cohesion: 0.14
Nodes (33): get_current_active_user(), get_db(), get_patient_service(), Return the current user only when the account is active., Provide a database session and always close it after the request., Provide the configured patient service., create_patient(), delete_patient() (+25 more)

### Community 7 - "test_visits_api.py"
Cohesion: 0.16
Nodes (32): _client(), _db_override(), TestClient, Contract tests for the clinical case (visit) and symptom endpoints. Extends…, Only patient_id is exposed, so no endpoint can lazy-load per row., _symptom(), test_add_symptom_returns_201(), test_create_visit_for_another_doctors_patient_is_404() (+24 more)

### Community 8 - "cn"
Cohesion: 0.11
Nodes (21): DashboardLayout(), NAV_ITEMS, ClinicianTrustCard(), InteractiveMriViewer(), RegionInfo, REGIONS, InteractivePipelineDemo(), ACCEPTED (+13 more)

### Community 9 - "react"
Cohesion: 0.13
Nodes (21): ForgotPasswordPage(), LoginForm(), ResetPasswordForm(), SignupPage(), useAuth(), AuthShell(), PasswordStrength(), Rule (+13 more)

### Community 10 - "add_symptom"
Cohesion: 0.16
Nodes (23): add_symptom(), create_analysis(), delete_symptom(), delete_visit(), get_latest_analysis(), get_visit(), delete, Depends (+15 more)

### Community 11 - "build_backend_architecture_report.py"
Cohesion: 0.18
Nodes (31): Document, Path, RGBColor, add_body(), add_bullets(), add_callout(), add_code(), add_cover() (+23 more)

### Community 12 - "get_auth_service"
Cohesion: 0.10
Nodes (26): get_auth_service(), get_current_user(), get_user_service(), Depends, Session, User, Validate the bearer token and return its associated user., Require the current user to have the administrator role. (+18 more)

### Community 13 - "UserResponse"
Cohesion: 0.21
Nodes (11): User request and response schemas., UserBase, UserCreate, UserResponse, Session, Hash a plaintext password., Provision a staff user after enforcing the ADMIN boundary., Create the first administrator, and only when none exists. (+3 more)

### Community 14 - "patient_visits.py"
Cohesion: 0.14
Nodes (25): alias, get_visit_service(), Provide the configured visit service., create_visit(), get_visit_history(), list_patient_visits(), Depends, ge (+17 more)

### Community 15 - "UserService"
Cohesion: 0.28
Nodes (6): UserUpdate, Session, User, UUID, Business logic for user management., UserService

### Community 16 - "dashboard/page.tsx"
Cohesion: 0.10
Nodes (15): ACCENTS, AVATAR_PALETTES, DashboardPage(), SortHeader(), toggleSort(), hexToRgb01(), NeuralBackground(), PatientRow (+7 more)

### Community 17 - "interactive-pipeline-demo.tsx"
Cohesion: 0.19
Nodes (12): ConfidenceDial(), ConfidenceDialProps, CASESHOTS, SampleCase, RegionBars(), ApiError, AuthTokens, DiseaseLabel (+4 more)

### Community 18 - "visits.py"
Cohesion: 0.08
Nodes (33): _analysis_page(), list_analyses(), list_symptoms(), ge, le, Query, Visit endpoints. Item-level operations are flat rather than nested under the…, List the symptoms recorded against a visit. (+25 more)

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
Cohesion: 0.24
Nodes (15): Token, _client(), _db_override(), TestClient, Integration-style contract tests for authentication endpoints., test_admin_can_create_user_without_returning_password(), test_clinician_cannot_create_users(), test_duplicate_user_is_conflict() (+7 more)

### Community 24 - "auth-provider.tsx"
Cohesion: 0.08
Nodes (27): body, display, metadata, mono, AuthContext, AuthContextValue, AuthProvider(), AuthTokens (+19 more)

### Community 25 - "create_access_token"
Cohesion: 0.21
Nodes (13): create_access_token(), decode_access_token(), hash_password(), Any, Password hashing and JSON Web Token helpers., Hash a plaintext password using the configured password context., Verify a plaintext password against a stored hash., Create a signed access token from the supplied claims. (+5 more)

### Community 26 - "test_ai_orchestrator.py"
Cohesion: 0.12
Nodes (36): AIError, _candidate(), _context(), _document(), _orchestrator(), Pipeline tests covering the AI test category (AGENTS.md section 10, TRD 12).…, AGENTS.md 8.1: never let simulated evidence read as clinically validated., AGENTS.md 8.4.6 / 18: citations traceable. (+28 more)

### Community 27 - "Clinical Safety Boundary (non-negotiable)"
Cohesion: 0.16
Nodes (16): Extended AI Output Contract (Diagnosis with category and trend_basis), Clinical Safety Boundary (non-negotiable), MVP as Investor/Stakeholder Demo, Never Represent Output as Definitive Diagnosis, APP-FLOW V1 Boundary, AI Phasing Decision (contract-real, provider-mocked), early_watch Diagnosis Category, Mocked-AI Credibility Risk (+8 more)

### Community 28 - "AGENTS.md — NeuroONE Agent Operating Contract"
Cohesion: 0.29
Nodes (8): AGENTS.md — NeuroONE Agent Operating Contract, Source-of-Truth Precedence, Task Planning Format, APP-FLOW — Application Flow, NEUROONE-MVP-SCOPE — Locked Scope Definition, PRD — Product Definition & Requirements, TRD — Technical Requirements & Design, TRD Implementation Sequence

### Community 29 - "AI Pipeline (Normalize → Context → Retrieve → Rank → LLM → Validate → Persist)"
Cohesion: 0.17
Nodes (12): Structured Clinical Input Contract, TEST Mode, backend/requirements.txt — Pinned Runtime Dependencies, backend/requirements-dev.txt — Test Dependencies (pytest, pytest-asyncio, httpx), AI Flow, Case Flow, FR-03 Clinical Input, FR-05 Literature Retrieval (+4 more)

### Community 30 - "Security and Privacy Rules"
Cohesion: 0.17
Nodes (12): Security and Privacy Rules, api service (FastAPI backend), db service (postgres:16-alpine), Health-Gated Service Startup, Enumeration-Resistant 404 for PHI-Adjacent Records, 404 Re-Labelling / Identifier Masking, Symptom-Belongs-To-Visit Verification, Demo Data Assumption (synthetic, not real PHI) (+4 more)

### Community 31 - "test_analysis_api.py"
Cohesion: 0.15
Nodes (29): _analysis(), _client(), _db_override(), _evidence(), _finding(), TestClient, Contract tests for the analysis endpoints. Beyond the usual status/shape…, A consumer must be able to tell simulated evidence from live evidence. (+21 more)

### Community 32 - "FR-01 Authentication"
Cohesion: 0.33
Nodes (7): Auth/Crypto Dependency Set (passlib, bcrypt, python-jose, cryptography, email-validator), Role-Level 403 vs Per-Record 404 Split, FR-01 Authentication, Server-Side Authorization (ADMIN, CLINICIAN), Middleware-Based Route Protection, OTP Email Verification Flow, Frontend Stack (Next.js 14 App Router, TypeScript, Tailwind, RHF+Zod, Axios)

### Community 33 - "test_analysis_service.py"
Cohesion: 0.26
Nodes (26): _candidate(), _deny_visit(), _evidence(), Unit tests for AnalysisService. Two properties carry the weight here: that a…, The masked 404 must not disclose the visit or the patient behind it., _result(), _service(), test_a_foreign_analysis_reads_as_a_missing_analysis() (+18 more)

### Community 34 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, autoprefixer, eslint, eslint-config-next, postcss, tailwindcss, @types/js-cookie, @types/node (+4 more)

### Community 35 - "JWT Authentication Flow"
Cohesion: 0.22
Nodes (9): Centralized Error Handling Rules, CONTRIBUTING — NeuroONE Contributing Guide, Standard API Response Envelope, JWT Environment Configuration (HS256, 30-min access token), FR-02 Patient Management, JWT Authentication Flow, Centralized Error Translation, Assumed Backend API Contract (+1 more)

### Community 36 - "Database Rules (UUIDs, timestamps, FKs, migrations, soft delete)"
Cohesion: 0.18
Nodes (11): Overridable Auth Service Providers, Open Convention — Transaction Boundary Ownership, Alembic Migration Policy, Team Repository Ownership Matrix, Single-Source Ownership Rule via Service Composition, Patient Soft-Delete Does Not Cascade to Visits, API Layer Rules, Database Rules (UUIDs, timestamps, FKs, migrations, soft delete) (+3 more)

### Community 37 - "neural-network.tsx"
Cohesion: 0.19
Nodes (9): FloatingParticles(), Particle, PARTICLES, Edge, EDGES, findNode(), NeuralNetwork(), Node (+1 more)

### Community 38 - "CASE-01 — Clinical Case / Symptom Domain"
Cohesion: 0.31
Nodes (9): Decision Record (ADR) Policy, Patient Flow (Patient Profile → Cases / History), ADR-001 — Ownership Violations Return 404, Not 403, ADR-002 — Visit Ownership Derives From Parent Patient, AI-01 — Structured AI Contract with Mocked Providers, AUTH-01 — Real Auth Endpoints and Soft-Delete Fix, CASE-01 — Clinical Case / Symptom Domain, Early-Detection Design (+1 more)

### Community 39 - "Confirmed Roles (ADMIN, CLINICIAN; RECEPTIONIST deferred)"
Cohesion: 0.20
Nodes (10): V1 Scope Guard, Primary Flow (Login → Dashboard → … → Report), AI-02 — Real LLM + RAG Swap-In, Demo-Ready MVP Definition, REPORT-01 — PDF Assembly, Confirmed Roles (ADMIN, CLINICIAN; RECEPTIONIST deferred), Administrator (user/role manager), Clinician (primary user) (+2 more)

### Community 40 - "User"
Cohesion: 0.13
Nodes (10): User model definitions., User, Session, UserRepository, Session, UUID, Run the AI pipeline for a visit and persist the result. Ownership violations…, Retrieve one analysis by ID. The caller named only the analysis, so a visit-… (+2 more)

### Community 41 - "Mode Transition State Machine"
Cohesion: 0.13
Nodes (15): AI/RAG Failure Safety Rule, Layered Architecture Rules (Client → API → Service → Repository → PostgreSQL), DEBUG Mode, Mode Transition State Machine, PLAN Mode, Repository Inspection Rules, Coding Standards (type hints, PEP 8, services own business logic), Feature → API → Service → Repository → Model → Schema Flow (+7 more)

### Community 42 - "DiagnosisCandidate"
Cohesion: 0.11
Nodes (33): AnalysisResult, DiagnosisCandidate, An early-watch flag must point at the patient's own history. Note the…, Validated pipeline output, before persistence., One ranked possible condition. ``extra="forbid"`` is deliberate: a model that…, EvidenceRef, A citation attached to a ranked candidate. Traces to EXTERNAL literature. Not…, _candidate() (+25 more)

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

### Community 48 - "otp_service.py"
Cohesion: 0.40
Nodes (4): generate_and_send_otp(), Generates a 6-digit OTP, stores it, and emails it via Gmail SMTP., Checks a submitted OTP against the stored one. The code is only consumed…, verify_otp()

### Community 49 - "test_analysis_repository.py"
Cohesion: 0.24
Nodes (24): AnalysisEvidence, AnalysisFinding, One ranked candidate condition. Decision support, never a definitive diagnosis:…, One citation supporting one ranked finding. Scoped to a finding rather than to…, _analysis(), _engine(), _evidence(), _finding() (+16 more)

### Community 51 - "middleware.ts"
Cohesion: 0.40
Nodes (3): AUTH_PAGES, config, PROTECTED_PREFIXES

### Community 56 - "RetrievedDocument"
Cohesion: 0.08
Nodes (33): _document(), Deterministic stand-in for a retrieval corpus and a reasoning model. Everything…, EvidenceRetriever, LLMClient, The provider seam. This module is the entire surface AI-02 replaces. Everything…, Retrieves candidate literature for a clinical context. Implementations must…, Return documents relevant to the query, most relevant first. Returning an empty…, Produces ranked candidate conditions from context plus evidence. The return… (+25 more)

### Community 60 - "AnalysisRepository"
Cohesion: 0.17
Nodes (14): Analysis, One run of the AI pipeline against one clinical case. Re-running creates a new…, AnalysisRepository, Session, UUID, Analysis persistence operations., Return the most recent analysis for a visit, if any., Provide analysis-specific queries in addition to common CRUD. (+6 more)

### Community 74 - "AnalysisOrchestrator"
Cohesion: 0.15
Nodes (16): AnalysisOrchestrator, The AI pipeline (TRD section 8, APP-FLOW section 5). Clinical Case -> Normalize…, Drop uncited candidates, then rank and trim. A ranked condition without a…, Execute the pipeline and return validated, ranked output., Runs the pipeline for one clinical context., cap_evidence_per_candidate(), rank_candidates(), rank_evidence() (+8 more)

### Community 75 - "Patient"
Cohesion: 0.16
Nodes (13): Patient, Patient model definitions., PatientRepository, Session, UUID, Patient persistence operations., Return the active patient with the given email address, if any., Provide patient-specific queries in addition to common CRUD operations. (+5 more)

### Community 76 - "test_ai_mock_providers.py"
Cohesion: 0.17
Nodes (20): _analyze(), _context(), Tests for the mocked retriever and reasoner. Two properties matter most here.…, The fixture must not read as real literature., AGENTS.md 8.2: confidence is likelihood, never certainty., The property a seeded RNG or a canned fixture would not have., AGENTS.md 8.1: schema-valid deterministic results., The canonical demo case: tremor 3 -> 5 -> 8 across three visits. (+12 more)

### Community 77 - "get_analysis"
Cohesion: 0.24
Nodes (9): get_analysis_service(), Provide the configured analysis service., get_analysis(), Depends, get, Session, UUID, Analysis item endpoints. Flat rather than nested under the visit: an analysis… (+1 more)

### Community 78 - "MockLLMClient"
Cohesion: 0.10
Nodes (19): MockCondition, A rule mapping clinical findings to a candidate condition., Reason over the supplied context and evidence., MockLLMClient, Deterministic stand-in for the reasoning model. Scores the frozen condition…, Rank the condition rules against the supplied context and evidence., Rule-based reasoner over the frozen condition table., Highest recorded severity per symptom, across every visit. (+11 more)

### Community 79 - "Symptom"
Cohesion: 0.09
Nodes (34): A neurological symptom recorded against a clinical case., Symptom, Session, UUID, Symptom persistence operations., Provide symptom-specific queries in addition to common CRUD operations., Return a visit's active symptoms in recording order., Count a visit's active symptoms. (+26 more)

### Community 80 - "AuthService"
Cohesion: 0.14
Nodes (17): TokenPayload, AuthService, User, Authenticate a user and issue an access token directly (no OTP step)., Verify a plaintext password against a stored hash., Create an access token for a user., Validate an access token and return its payload., Business logic for authentication operations. (+9 more)

### Community 81 - "ADR-003: AI Analysis Contract and the Mocked-Provider Seam"
Cohesion: 0.15
Nodes (13): ADR-003: AI Analysis Contract and the Mocked-Provider Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 82 - "v1/auth.py"
Cohesion: 0.22
Nodes (10): login(), Depends, get, post, Session, Authentication endpoints., Verify username/email and password and return a signed JWT., Return the identity associated with the bearer token. (+2 more)

### Community 83 - "Base"
Cohesion: 0.22
Nodes (7): Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), Database engine and session configuration., Base, DeclarativeBase

### Community 84 - "test_deleted_at_timezone_migration.py"
Cohesion: 0.43
Nodes (6): _load_migration(), Regression tests for the deleted_at timezone migration., test_downgrade_restores_naive_timestamps(), test_migration_chains_from_case_01(), test_upgrade_uses_implicit_timezone_cast(), ModuleType

### Community 85 - "Agent Definition of Done Checklist"
Cohesion: 0.40
Nodes (5): BUILD Mode, Agent Definition of Done Checklist, Feature Branch Strategy, Contributing Definition of Done, Milestone 2 — Deliver One Vertical Feature

### Community 86 - ".likelihood_band"
Cohesion: 0.33
Nodes (5): likelihood_band_for(), Confidence-tiered output (section 8.3). This is what UI copy and the PDF should…, Tier a confidence value (AGENTS.md section 8.3). Derived, never stored: a…, computed_field, LikelihoodBand

## Ambiguous Edges - Review These
- `V1 Exclusions (MRI, uploaded reports, autonomous diagnosis, automated treatment)` → `MRI Upload + Prediction Polling`  [AMBIGUOUS]
  frontend/README.md · relation: conceptually_related_to
- `V1 Exclusions (MRI, uploaded reports, autonomous diagnosis, automated treatment)` → `MRI-Based Neurodegenerative Disease Analysis (marketing claim)`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to
- `MRI-Based Neurodegenerative Disease Analysis (marketing claim)` → `Clinical Safety Boundary (non-negotiable)`  [AMBIGUOUS]
  AGENTS.md · relation: conceptually_related_to
- `AI Pipeline (Normalize → Context → Retrieve → Rank → LLM → Validate → Persist)` → `backend/requirements.txt — Pinned Runtime Dependencies`  [AMBIGUOUS]
  backend/requirements.txt · relation: conceptually_related_to
- `FR-01 Authentication` → `OTP Email Verification Flow`  [AMBIGUOUS]
  frontend/README.md · relation: conceptually_related_to
- `Server-Side Authorization (ADMIN, CLINICIAN)` → `Middleware-Based Route Protection`  [AMBIGUOUS]
  frontend/README.md · relation: conceptually_related_to
- `Standard API Response Envelope` → `Assumed Backend API Contract`  [AMBIGUOUS]
  frontend/README.md · relation: conceptually_related_to
- `Container Setup Unusable (empty compose, placeholder Dockerfile)` → `docker-compose.yml — Local Dev Stack`  [AMBIGUOUS]
  reports/PROGRESS_REPORT.md · relation: references

## Knowledge Gaps
- **156 isolated node(s):** `extends`, `next/core-web-vitals`, `nextConfig`, `name`, `version` (+151 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 594 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `V1 Exclusions (MRI, uploaded reports, autonomous diagnosis, automated treatment)` and `MRI Upload + Prediction Polling`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `V1 Exclusions (MRI, uploaded reports, autonomous diagnosis, automated treatment)` and `MRI-Based Neurodegenerative Disease Analysis (marketing claim)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `MRI-Based Neurodegenerative Disease Analysis (marketing claim)` and `Clinical Safety Boundary (non-negotiable)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `AI Pipeline (Normalize → Context → Retrieve → Rank → LLM → Validate → Persist)` and `backend/requirements.txt — Pinned Runtime Dependencies`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `FR-01 Authentication` and `OTP Email Verification Flow`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Server-Side Authorization (ADMIN, CLINICIAN)` and `Middleware-Based Route Protection`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Standard API Response Envelope` and `Assumed Backend API Contract`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._