# Graph Report - NeuroOne-V1  (2026-09-10)

## Corpus Check
- 171 files · ~74,381 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1815 nodes · 4627 edges · 104 communities (79 shown, 20 thin omitted)
- Extraction: 89% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 479 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `10c6528e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- VisitService
- BaseRepository
- EntityNotFoundError
- detect_trends
- PatientService
- BaseModel
- UserRole
- test_visits_api.py
- cn
- react
- get_current_active_user
- build_backend_architecture_report.py
- dependencies.py
- ReasoningResult
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
- ReportRepository
- Standard API Response Envelope
- Database Rules (UUIDs, timestamps, FKs, migrations, soft delete)
- neural-network.tsx
- CASE-01 — Clinical Case / Symptom Domain
- Confirmed Roles (ADMIN, CLINICIAN; RECEPTIONIST deferred)
- UserRepository
- Mode Transition State Machine
- DiagnosisCandidate
- FR-07 Clinical Report
- 1f74d19af1b8_widen_patient_email_and_promote_phone_.py
- 8e72c1f4a9b0_replace_legacy_user_roles.py
- a3c7be51d904_create_visits_and_symptoms.py
- b8d41e2f7c53_make_deleted_at_timezone_aware.py
- otp_service.py
- test_report_service.py
- VerifyOtpForm
- middleware.ts
- RetrievedDocument
- test_health.py
- .eslintrc.json
- next.config.mjs
- User
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
- ClinicalContext
- build_clinical_context
- test_ai_mock_providers.py
- v1/analysis.py
- MockLLMClient
- VisitRepository
- AuthService
- ADR-003: AI Analysis Contract and the Mocked-Provider Seam
- report_service.py
- Base
- test_deleted_at_timezone_migration.py
- test_report_api.py
- likelihood_band_for
- corpus/__init__.py
- CLAUDE.md
- test_report_renderer.py
- VisitStatus
- Symptom
- test_patients_api.py
- Visit
- ADR-004: Clinical Report Snapshot and Rendering
- reports.py
- renderer.py
- b2b31bad27df_add_symptom_observation.py
- c4e19a7b6d20_create_analyses_findings_and_evidence.py
- dcfbc7d5b2c9_create_reports.py
- _reject_blank
- Q: How are Alembic migrations and backend tests configured, and where should PR CI run pytest?
- Q: The parallel AI-01 work is committed and pulled; plan our next work
- reports/__init__.py

## God Nodes (most connected - your core abstractions)
1. `User` - 97 edges
2. `EntityNotFoundError` - 79 edges
3. `UserRole` - 74 edges
4. `BaseModel` - 67 edges
5. `Visit` - 54 edges
6. `VisitService` - 53 edges
7. `VisitStatus` - 48 edges
8. `PatientService` - 43 edges
9. `get_db()` - 42 edges
10. `get_current_active_user()` - 42 edges

## Surprising Connections (you probably didn't know these)
- `Milestone 2 — Deliver One Vertical Feature` --semantically_similar_to--> `PAT-01 — Authorized Patient CRUD Vertical Slice`  [INFERRED] [semantically similar]
  reports/PROGRESS_REPORT.md → docs/NEUROONE-MVP-SCOPE.md
- `MRI Upload + Prediction Polling` --semantically_similar_to--> `MRI-Based Neurodegenerative Disease Analysis (marketing claim)`  [INFERRED] [semantically similar]
  frontend/README.md → README.md
- `MRI-Based Neurodegenerative Disease Analysis (marketing claim)` --conceptually_related_to--> `Clinical Safety Boundary (non-negotiable)`  [AMBIGUOUS]
  README.md → AGENTS.md
- `Assumed Backend API Contract` --conceptually_related_to--> `Standard API Response Envelope`  [AMBIGUOUS]
  frontend/README.md → CONTRIBUTING.md
- `TRD Layered Architecture` --semantically_similar_to--> `Feature → API → Service → Repository → Model → Schema Flow`  [INFERRED] [semantically similar]
  docs/TRD.md → CONTRIBUTING.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **AI/RAG Evidence Traceability Chain** — docs_trd_ai_pipeline, docs_trd_rag_rules, docs_trd_ai_output_contract, docs_app_flow_evidence_flow, docs_prd_fr_06_explainability, docs_neuroone_mvp_scope_trend_basis [EXTRACTED 1.00]
- **MVP Acceptance Journey — Same Path Across Four Documents** — docs_prd_mvp_acceptance_journey, docs_app_flow_primary_flow, docs_neuroone_mvp_scope_demo_ready_definition, agents_test_mode, docs_trd_implementation_sequence [EXTRACTED 1.00]
- **Per-Record Ownership Enforcement Pattern (404 masking, derived one hop up)** — docs_decisions_adr_001_ownership_violation_status_code_enumeration_resistance, docs_decisions_adr_001_ownership_violation_status_code_role_vs_record_gating, docs_decisions_adr_002_visit_ownership_derivation_single_ownership_rule, docs_decisions_adr_002_visit_ownership_derivation_404_relabelling, docs_decisions_adr_002_visit_ownership_derivation_symptom_parent_check, docs_trd_error_handling [EXTRACTED 1.00]

## Communities (104 total, 20 thin omitted)

### Community 0 - "VisitService"
Cohesion: 0.13
Nodes (17): Session, UUID, Open a clinical case for a patient the caller owns. The patient id came from…, Retrieve a visit by ID. Ownership violations read as 404., List a patient's visits, newest first., Return a patient's visit history ordered for trend comparison. This is the in-…, Partially update a visit. Ownership violations read as 404., Soft-delete a visit and its symptoms. (+9 more)

### Community 1 - "BaseRepository"
Cohesion: 0.06
Nodes (58): Top-level API router., health(), get, root(), Analysis persistence operations., BaseRepository, Session, UUID (+50 more)

### Community 2 - "EntityNotFoundError"
Cohesion: 0.10
Nodes (58): Payload used to record a symptom against a visit., Payload used to partially update a symptom., SymptomCreate, SymptomUpdate, _as_utc(), field_validator, Clinical case / visit request and response schemas., Normalize a naive datetime to UTC so ordering never mixes tz-awareness. (+50 more)

### Community 3 - "detect_trends"
Cohesion: 0.09
Nodes (40): Normalize Input + Build Clinical Context (TRD section 8, stages 1-2). This is…, Map a Visit and its live symptoms into the AI-facing shape., _to_context_visit(), detect_trends(), _direction(), normalize_symptom_name(), Cross-visit symptom trend detection. This is the mechanism behind AGENTS.md…, Normalized names of symptoms that are getting worse across visits. This is the… (+32 more)

### Community 4 - "PatientService"
Cohesion: 0.05
Nodes (65): get_patient_service(), Provide the configured patient service., create_patient(), delete_patient(), get_patient(), list_patients(), _paginated_response(), delete (+57 more)

### Community 5 - "BaseModel"
Cohesion: 0.15
Nodes (14): BaseModel, Base model definition., ForgotPasswordRequest, ForgotPasswordResponse, LoginRequest, OtpRequiredResponse, OtpVerifyRequest, ResetPasswordRequest (+6 more)

### Community 6 - "UserRole"
Cohesion: 0.24
Nodes (29): str, UserRole, PatientUpdate, PhoneNumber, A patient phone number., Payload used to partially update a patient., _create_payload(), _patient() (+21 more)

### Community 7 - "test_visits_api.py"
Cohesion: 0.15
Nodes (34): _client(), _db_override(), TestClient, Contract tests for the clinical case (visit) and symptom endpoints. Extends…, Only patient_id is exposed, so no endpoint can lazy-load per row., _symptom(), test_a_whitespace_only_observation_is_rejected(), test_add_symptom_returns_201() (+26 more)

### Community 8 - "cn"
Cohesion: 0.11
Nodes (21): DashboardLayout(), NAV_ITEMS, ClinicianTrustCard(), InteractiveMriViewer(), RegionInfo, REGIONS, InteractivePipelineDemo(), ACCEPTED (+13 more)

### Community 9 - "react"
Cohesion: 0.13
Nodes (21): ForgotPasswordPage(), LoginForm(), ResetPasswordForm(), SignupPage(), useAuth(), AuthShell(), PasswordStrength(), Rule (+13 more)

### Community 10 - "get_current_active_user"
Cohesion: 0.16
Nodes (28): get_current_active_user(), get_db(), Session, Return the current user only when the account is active., Provide a database session and always close it after the request., add_symptom(), create_analysis(), delete_symptom() (+20 more)

### Community 11 - "build_backend_architecture_report.py"
Cohesion: 0.18
Nodes (31): Document, Path, RGBColor, add_body(), add_bullets(), add_callout(), add_code(), add_cover() (+23 more)

### Community 12 - "dependencies.py"
Cohesion: 0.13
Nodes (19): get_current_user(), get_user_service(), Depends, User, Reusable FastAPI dependencies for database and access control., Validate the bearer token and return its associated user., Create a dependency that permits only the supplied user roles., Require the current user to have the administrator role. (+11 more)

### Community 13 - "ReasoningResult"
Cohesion: 0.12
Nodes (21): AI orchestration. Layering rule: nothing in this package imports a repository…, The AI pipeline (TRD section 8, APP-FLOW section 5). Clinical Case -> Normalize…, EvidenceRetriever, LLMClient, The provider seam. This module is the entire surface AI-02 replaces. Everything…, Retrieves candidate literature for a clinical context. Implementations must…, Produces ranked candidate conditions from context plus evidence. The return…, Reason over the supplied context and evidence. (+13 more)

### Community 14 - "patient_visits.py"
Cohesion: 0.15
Nodes (23): alias, get_visit_service(), Provide the configured visit service., create_visit(), get_visit_history(), list_patient_visits(), Depends, ge (+15 more)

### Community 15 - "UserService"
Cohesion: 0.16
Nodes (11): UserUpdate, BaseService, Shared service-layer infrastructure., Base service providing access to the repository., Public service-layer exports., Session, User, UUID (+3 more)

### Community 16 - "dashboard/page.tsx"
Cohesion: 0.10
Nodes (15): ACCENTS, AVATAR_PALETTES, DashboardPage(), SortHeader(), toggleSort(), hexToRgb01(), NeuralBackground(), PatientRow (+7 more)

### Community 17 - "interactive-pipeline-demo.tsx"
Cohesion: 0.19
Nodes (12): ConfidenceDial(), ConfidenceDialProps, CASESHOTS, SampleCase, RegionBars(), ApiError, AuthTokens, DiseaseLabel (+4 more)

### Community 18 - "visits.py"
Cohesion: 0.11
Nodes (27): _analysis_page(), list_analyses(), list_symptoms(), ge, le, Query, Visit endpoints. Item-level operations are flat rather than nested under the…, List the symptoms recorded against a visit. (+19 more)

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
Cohesion: 0.07
Nodes (29): dependencies, axios, clsx, framer-motion, @hookform/resolvers, js-cookie, lucide-react, next (+21 more)

### Community 23 - "test_auth_api.py"
Cohesion: 0.25
Nodes (14): _client(), _db_override(), TestClient, Integration-style contract tests for authentication endpoints., test_admin_can_create_user_without_returning_password(), test_clinician_cannot_create_users(), test_duplicate_user_is_conflict(), test_expired_token_returns_controlled_401() (+6 more)

### Community 24 - "auth-provider.tsx"
Cohesion: 0.08
Nodes (27): body, display, metadata, mono, AuthContext, AuthContextValue, AuthProvider(), AuthTokens (+19 more)

### Community 25 - "create_access_token"
Cohesion: 0.21
Nodes (13): create_access_token(), decode_access_token(), hash_password(), Any, Password hashing and JSON Web Token helpers., Hash a plaintext password using the configured password context., Verify a plaintext password against a stored hash., Create a signed access token from the supplied claims. (+5 more)

### Community 26 - "test_ai_orchestrator.py"
Cohesion: 0.12
Nodes (42): AnalysisOrchestrator, Runs the pipeline for one clinical context., AIError, _candidate(), _context(), _document(), _orchestrator(), Pipeline tests covering the AI test category (AGENTS.md section 10, TRD 12).… (+34 more)

### Community 27 - "Clinical Safety Boundary (non-negotiable)"
Cohesion: 0.21
Nodes (12): Extended AI Output Contract (Diagnosis with category and trend_basis), Clinical Safety Boundary (non-negotiable), MVP as Investor/Stakeholder Demo, Never Represent Output as Definitive Diagnosis, AI Phasing Decision (contract-real, provider-mocked), early_watch Diagnosis Category, Mocked-AI Credibility Risk, trend_basis (prior-visit traceability) (+4 more)

### Community 28 - "AGENTS.md — NeuroONE Agent Operating Contract"
Cohesion: 0.18
Nodes (12): AGENTS.md — NeuroONE Agent Operating Contract, Source-of-Truth Precedence, PLAN Mode, Repository Inspection Rules, Task Planning Format, APP-FLOW — Application Flow, NEUROONE-MVP-SCOPE — Locked Scope Definition, PRD — Product Definition & Requirements (+4 more)

### Community 29 - "AI Pipeline (Normalize → Context → Retrieve → Rank → LLM → Validate → Persist)"
Cohesion: 0.17
Nodes (12): Structured Clinical Input Contract, TEST Mode, backend/requirements.txt — Pinned Runtime Dependencies, backend/requirements-dev.txt — Test Dependencies (pytest, pytest-asyncio, httpx), AI Flow, Case Flow, FR-03 Clinical Input, FR-05 Literature Retrieval (+4 more)

### Community 30 - "Security and Privacy Rules"
Cohesion: 0.17
Nodes (12): Security and Privacy Rules, api service (FastAPI backend), db service (postgres:16-alpine), Health-Gated Service Startup, Enumeration-Resistant 404 for PHI-Adjacent Records, 404 Re-Labelling / Identifier Masking, Symptom-Belongs-To-Visit Verification, Demo Data Assumption (synthetic, not real PHI) (+4 more)

### Community 31 - "test_analysis_api.py"
Cohesion: 0.17
Nodes (27): _analysis(), _client(), _db_override(), TestClient, Contract tests for the analysis endpoints. Beyond the usual status/shape…, A consumer must be able to tell simulated evidence from live evidence., AGENTS.md 8.2: not in the schema, not in API field naming., An OpenAPI tag named "diagnosis" is the framing 8.2 forbids. (+19 more)

### Community 32 - "FR-01 Authentication"
Cohesion: 0.20
Nodes (11): Auth/Crypto Dependency Set (passlib, bcrypt, python-jose, cryptography, email-validator), JWT Environment Configuration (HS256, 30-min access token), Role-Level 403 vs Per-Record 404 Split, FR-01 Authentication, FR-02 Patient Management, JWT Authentication Flow, Server-Side Authorization (ADMIN, CLINICIAN), Assumed Backend API Contract (+3 more)

### Community 33 - "test_analysis_service.py"
Cohesion: 0.24
Nodes (28): _candidate(), _deny_visit(), _evidence(), Unit tests for AnalysisService. Two properties carry the weight here: that a…, AGENTS.md 8.4.4: source metadata must survive to persistence., The masked 404 must not disclose the visit or the patient behind it., _result(), _service() (+20 more)

### Community 34 - "ReportRepository"
Cohesion: 0.17
Nodes (19): Session, UUID, Report persistence operations., Provide report-specific queries in addition to common CRUD., Return an analysis's reports, newest first., Count an analysis's active reports., ReportRepository, _engine() (+11 more)

### Community 35 - "Standard API Response Envelope"
Cohesion: 0.20
Nodes (10): Layered Architecture Rules (Client → API → Service → Repository → PostgreSQL), Centralized Error Handling Rules, CONTRIBUTING — NeuroONE Contributing Guide, Standard API Response Envelope, Coding Standards (type hints, PEP 8, services own business logic), Feature → API → Service → Repository → Model → Schema Flow, Backend Directory Layout, Centralized Error Translation (+2 more)

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
Cohesion: 0.15
Nodes (14): V1 Scope Guard, Primary Flow (Login → Dashboard → … → Report), APP-FLOW V1 Boundary, AI-02 — Real LLM + RAG Swap-In, Demo-Ready MVP Definition, REPORT-01 — PDF Assembly, Confirmed Roles (ADMIN, CLINICIAN; RECEPTIONIST deferred), Administrator (user/role manager) (+6 more)

### Community 41 - "Mode Transition State Machine"
Cohesion: 0.18
Nodes (11): AI/RAG Failure Safety Rule, BUILD Mode, DEBUG Mode, Agent Definition of Done Checklist, Mode Transition State Machine, Feature Branch Strategy, Contributing Definition of Done, Failure Flows (AI/RAG, Database, Invalid Input) (+3 more)

### Community 42 - "DiagnosisCandidate"
Cohesion: 0.12
Nodes (31): AnalysisResult, DiagnosisCandidate, An early-watch flag must point at the patient's own history. Note the…, Validated pipeline output, before persistence., One ranked possible condition. ``extra="forbid"`` is deliberate: a model that…, _candidate(), _evidence(), parametrize (+23 more)

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

### Community 49 - "test_report_service.py"
Cohesion: 0.07
Nodes (67): AnalysisEvidence, AnalysisFinding, FindingCategory, Enum, str, Persisted AI analysis, its ranked findings, and their citations. Naming is…, One ranked candidate condition. Decision support, never a definitive diagnosis:…, One citation supporting one ranked finding. Scoped to a finding rather than to… (+59 more)

### Community 51 - "middleware.ts"
Cohesion: 0.40
Nodes (3): AUTH_PAGES, config, PROTECTED_PREFIXES

### Community 56 - "RetrievedDocument"
Cohesion: 0.09
Nodes (26): _document(), Deterministic stand-in for a retrieval corpus and a reasoning model. Everything…, Return documents relevant to the query, most relevant first. Returning an empty…, MockEvidenceRetriever, _normalize(), Deterministic stand-in for a literature retriever. Matches the query against a…, Keyword retriever over the frozen mock corpus., Return matching documents, most relevant first. An empty result is a legitimate… (+18 more)

### Community 60 - "User"
Cohesion: 0.15
Nodes (19): Analysis, One run of the AI pipeline against one clinical case. Re-running creates a new…, User model definitions., User, AnalysisService, Session, UUID, Run the AI pipeline for a visit and persist the result. Ownership violations… (+11 more)

### Community 74 - "ClinicalContext"
Cohesion: 0.12
Nodes (13): Re-attach evidence from the orchestrator's own retrieved set. A provider names…, Drop uncited candidates, then rank and trim. A ranked condition without a…, Execute the pipeline and return validated, ranked output., cap_evidence_per_candidate(), rank_candidates(), rank_evidence(), Rank Evidence (TRD section 8, stage 4). Real now and unchanged by AI-02:…, Order documents by relevance, then source trust, then recency. ``document_id``… (+5 more)

### Community 75 - "build_clinical_context"
Cohesion: 0.21
Nodes (21): _age_years(), build_clinical_context(), date, Whole years, so a date of birth never reaches the reasoning layer., Assemble the context the AI pipeline reasons over. ``prior_visits`` must be…, _patient(), Tests for the ORM -> ClinicalContext normalize stage. The PHI-minimization…, The current severity is part of the trajectory, not outside it. (+13 more)

### Community 76 - "test_ai_mock_providers.py"
Cohesion: 0.16
Nodes (21): _analyze(), _context(), Tests for the mocked retriever and reasoner. Two properties matter most here.…, The fixture must not read as real literature., AGENTS.md 8.2: confidence is likelihood, never certainty., The property a seeded RNG or a canned fixture would not have., AGENTS.md 8.1: schema-valid deterministic results., The canonical demo case: tremor 3 -> 5 -> 8 across three visits. (+13 more)

### Community 77 - "v1/analysis.py"
Cohesion: 0.14
Nodes (21): get_analysis_service(), Provide the configured analysis service., create_report(), get_analysis(), list_reports(), Depends, ge, get (+13 more)

### Community 78 - "MockLLMClient"
Cohesion: 0.18
Nodes (12): MockCondition, A rule mapping clinical findings to a candidate condition., MockLLMClient, Deterministic stand-in for the reasoning model. Scores the frozen condition…, Rank the condition rules against the supplied context and evidence., Rule-based reasoner over the frozen condition table., Highest recorded severity per symptom, across every visit., Build history references for the matched worsening symptoms. Every reference… (+4 more)

### Community 79 - "VisitRepository"
Cohesion: 0.28
Nodes (17): Provide visit-specific queries in addition to common CRUD operations., VisitRepository, _engine(), Real-database tests for cross-visit history retrieval. These run against SQLite…, The loader criteria, not just the read path, must filter soft deletes., Regression guard for the N+1 the selectinload exists to prevent. One SELECT for…, test_get_by_patient_paginates_and_filters_by_status(), test_get_with_symptoms_hides_soft_deleted_visits() (+9 more)

### Community 80 - "AuthService"
Cohesion: 0.06
Nodes (48): get_auth_service(), Provide the configured authentication service., create_user(), Depends, post, Session, User, Administrator-only endpoints. (+40 more)

### Community 81 - "ADR-003: AI Analysis Contract and the Mocked-Provider Seam"
Cohesion: 0.14
Nodes (14): Addendum: evidence-resolution correction (pre-`REPORT-01`), ADR-003: AI Analysis Contract and the Mocked-Provider Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact (+6 more)

### Community 82 - "report_service.py"
Cohesion: 0.15
Nodes (17): Clinical report contract (FR-07, ADR-004). ``ReportSnapshot`` is exactly what…, The patient/case identification FR-07 requires a report to carry., One clinical input as recorded for the visit (FR-03)., The clinical case the analysis was run against., A citation as it must appear in the PDF (FR-05/06)., Everything the renderer may draw on. Nothing else reaches the PDF., ReportEvidenceSnapshot, ReportPatientSnapshot (+9 more)

### Community 83 - "Base"
Cohesion: 0.22
Nodes (7): Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), Database engine and session configuration., Base, DeclarativeBase

### Community 84 - "test_deleted_at_timezone_migration.py"
Cohesion: 0.43
Nodes (6): _load_migration(), Regression tests for the deleted_at timezone migration., test_downgrade_restores_naive_timestamps(), test_migration_chains_from_case_01(), test_upgrade_uses_implicit_timezone_cast(), ModuleType

### Community 85 - "test_report_api.py"
Cohesion: 0.21
Nodes (19): _client(), _db_override(), TestClient, Contract tests for the report endpoints. Beyond the usual status/shape…, AGENTS.md 8.2: not in the schema, not in API field naming., _report(), _snapshot(), test_a_foreign_report_404s_without_naming_its_analysis() (+11 more)

### Community 86 - "likelihood_band_for"
Cohesion: 0.27
Nodes (8): FindingResponse, likelihood_band_for(), Confidence-tiered output (section 8.3). This is what UI copy and the PDF should…, A ranked candidate as returned by the API., Derived from confidence, never read from the row., Tier a confidence value (AGENTS.md section 8.3). Derived, never stored: a…, computed_field, LikelihoodBand

### Community 89 - "test_report_renderer.py"
Cohesion: 0.24
Nodes (19): Render a complete, multi-page clinical report PDF. Raises whatever ReportLab…, render(), _evidence(), _finding(), parametrize, Tests for the PDF renderer (ADR-004, FR-07). Runs the renderer for real and…, FR-07: patient/case, clinical inputs, differential, reasoning, evidence,…, ADR-004 assumes bundled/base fonts; exotic characters degrade, not crash. (+11 more)

### Community 90 - "VisitStatus"
Cohesion: 0.17
Nodes (12): Enum, str, Lifecycle of a clinical case. ANALYZED is written by the AI pipeline (AI-01),…, VisitStatus, Session, UUID, Clinical case / visit persistence operations., Eager-load each visit's live symptoms in one extra query. selectinload rather… (+4 more)

### Community 91 - "Symptom"
Cohesion: 0.18
Nodes (10): A neurological symptom recorded against a clinical case., Symptom, Session, UUID, Symptom persistence operations., Provide symptom-specific queries in addition to common CRUD operations., Return a visit's active symptoms in recording order., Count a visit's active symptoms. (+2 more)

### Community 92 - "test_patients_api.py"
Cohesion: 0.28
Nodes (15): AuthorizationError, _client(), _db_override(), _patient(), TestClient, Integration-style contract tests for patient endpoints. Covers the ownership-…, test_clinician_cannot_create_patient_for_another_doctor(), test_delete_on_other_doctors_patient_is_404() (+7 more)

### Community 93 - "Visit"
Cohesion: 0.21
Nodes (9): Symptom model definitions., Clinical case / visit model definitions., A clinical case / visit belonging to a patient. Ownership is derived from the…, Visit, Persist an analysis and advance the visit status in one transaction. Both…, datetime, main(), Seed a demo patient whose history contains a multi-visit trend. AGENTS.md… (+1 more)

### Community 94 - "ADR-004: Clinical Report Snapshot and Rendering"
Cohesion: 0.14
Nodes (13): ADR-004: Clinical Report Snapshot and Rendering, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 95 - "reports.py"
Cohesion: 0.24
Nodes (12): get_report_service(), Provide the configured report service., download_report_pdf(), get_report(), Depends, get, Session, UUID (+4 more)

### Community 96 - "renderer.py"
Cohesion: 0.28
Nodes (12): _build_story(), _draw_footer(), _finding_label(), _p(), Render a ReportSnapshot into a complete clinical report PDF (ADR-004). A pure…, Escape Platypus markup and fall back for characters base14 can't render.…, _render_finding(), _safe() (+4 more)

### Community 97 - "b2b31bad27df_add_symptom_observation.py"
Cohesion: 0.40
Nodes (4): downgrade(), Add the clinician-entered observation field (FR-03). Nullable, so every…, Drop the observation column., upgrade()

### Community 98 - "c4e19a7b6d20_create_analyses_findings_and_evidence.py"
Cohesion: 0.40
Nodes (4): downgrade(), Drop the analysis tables and the enum type they created., Create the AI analysis tables. No drops. The abandoned Diagnosis and Rag stubs…, upgrade()

### Community 99 - "dcfbc7d5b2c9_create_reports.py"
Cohesion: 0.40
Nodes (4): downgrade(), Create the reports table (ADR-004). No pdf_path and no binary PDF column: only…, Drop the reports table., upgrade()

### Community 100 - "_reject_blank"
Cohesion: 0.50
Nodes (3): field_validator, A whitespace-only observation is the same as no observation, rejected rather…, _reject_blank()

### Community 101 - "Q: How are Alembic migrations and backend tests configured, and where should PR CI run pytest?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: How are Alembic migrations and backend tests configured, and where should PR CI run pytest?, Source Nodes

### Community 102 - "Q: The parallel AI-01 work is committed and pulled; plan our next work"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: The parallel AI-01 work is committed and pulled; plan our next work, Source Nodes

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
- **175 isolated node(s):** `extends`, `next/core-web-vitals`, `nextConfig`, `name`, `version` (+170 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 678 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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