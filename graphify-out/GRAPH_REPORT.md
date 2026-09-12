# Graph Report - NeuroOne-V1  (2026-09-12)

## Corpus Check
- 143 files · ~172,385 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2609 nodes · 6143 edges · 183 communities (125 shown, 51 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 563 edges (avg confidence: 0.94)
- Token cost: 403,064 input · 0 output

## Community Hubs (Navigation)
- Visit & Symptom Domain Tests
- User Roles & Patient Service Tests
- Analysis Persistence Layer
- Analysis Orchestrator
- AI Provider Contracts & Clients
- API Dependency Injection
- Report Rendering
- Analysis API & Report Creation
- Analysis Output Schemas
- Live LLM Reasoning Tests
- Patients API
- Authentication Service
- Frontend Auth Pages & Validation
- AI Provider Wiring
- Legacy Patient Detail UI
- Triage Queue
- Analysis API Tests
- Frontend API Client & Auth Provider
- Analysis Service Tests
- Architecture Report Generator
- MRI Staging Tests
- Patient Service
- Visit Service
- Frontend Package Manifests
- MRI Staging Seam
- Report Persistence
- Patient Repository
- Auth API & Token Schemas
- Core Domain Models
- Trend Detection
- Scan Storage Backend
- Report Service Tests
- Mock Provider Tests
- Landing Page 3D Scenes
- Parked Design System
- Patient Visits API
- Error Handling & Exceptions
- Report API Tests
- Live LLM Provider Tests
- Clinical Context Building
- Architecture Decision Rationale
- Evidence Retrieval Seam
- TypeScript Configuration
- Scan Intake Service
- Legacy Mockup Dashboard
- BaseModel
- Symptom
- BaseRepository
- VisitRepository
- ReportSnapshot (typed JSONB Snapshot)
- NeuroOne Frontend — Redesign Checklist
- Compileroptions
- FR-04 Differential Diagnosis
- Test Auth Api
- ADR-006: MRI Becomes A Primary Input, With Symptoms As Conte
- Early Watch Category Derived From Trend Evidence
- Backend Tests Workflow
- Security And Privacy Rules
- Datetime
- Test Scan Service
- Two Narrow Protocol Provider Seam
- Dependencies
- Useauth
- Page
- Api
- AI Output Contract
- Test Otp Service
- MVP Acceptance Journey
- UserAlreadyExistsError
- Test Security
- Per-Record Ownership Check
- Interactive-pipeline-demo
- Trends
- Visit
- ADR-003: AI Analysis Contract And The Mocked-Provider Seam
- REPORT-01D — Frontend Requirements & Backend Mapping Checkli
- Reports
- Get By Patient
- Test Scan Api
- ADR-004: Clinical Report Snapshot And Rendering
- ADR-005: Live LLM Provider Behind The AI-01 Seam
- Current Development Status Table
- Test Triage Api
- Devdependencies
- NeuroONE Agent Operating Contract
- Generate Report
- Error Response
- Devdependencies (2)
- Dependencies (2)
- Init
- NeuroOne Login Neurons Artwork V1
- AI-01 Contract-Real Provider-Mocked
- Main
- Verify Credentials
- Error Handling Contract
- Three Provenance States And Pipeline Note
- Likelihood Band For
- FR-07 Clinical Report
- Dependencies (3)
- NeuroONE Frontend Redesign (parked)
- ADR-006 MRI Primary With Symptoms As Context
- Get User Service
- EvidenceRef
- Test Deleted At Timezone Migration
- Eslintrc
- Scripts
- 14056b8ec27d Create Scans
- 1f74d19af1b8 Widen Patient Email And Promote Phone
- 7544ad0b1ed6 Add Analysis Sign Off
- 8e72c1f4a9b0 Replace Legacy User Roles
- A3c7be51d904 Create Visits And Symptoms
- B2b31bad27df Add Symptom Observation
- B8d41e2f7c53 Make Deleted At Timezone Aware
- C4e19a7b6d20 Create Analyses Findings And Evidence
- Dcfbc7d5b2c9 Create Reports
- Next Config Mjs
- Scripts (2)
- Middleware
- Validation
- Q: How Are Alembic Migrations And Backend Tests Configured, 
- Q: The Parallel AI-01 Work Is Committed And Pulled; Plan Our
- Read Current User
- Layout
- Password-strength
- Seed
- RAG Requirements
- Init (2)
- Test Health
- Api Service (fastapi Backend)
- Clinician Review Flow
- NOTE: This File Should Not Be Edited
- Tailwindcss
- PLAN
- NeuroOne Login Artwork V1
- Init (3)
- Constants
- Init (4)
- Conftest
- CLAUDE
- Standard API Response Envelope
- Feature Branch Strategy
- AI Flow
- Middleware-Based Route Protection
- Tailwind Config
- README
- Backup
- Build Embeddings
- Ingest Documents
- Seed Database
- Datetime (2)
- User
- Delete
- Patch
- Field Validator
- User (2)
- User (3)
- Path
- Exception
- Pytest-asyncio
- Uvicorn
- CONTRIBUTING — NeuroONE Contributing Guide
- Commit Message Convention
- Docker-compose Yml — Local Dev Stack
- JWT Environment Configuration (HS256, 30-min Access Token)
- APP-FLOW — Application Flow
- Authentication Flow
- RAG, Database, Invalid Input)
- History)
- Primary Flow (login → Dashboard → … → Report)
- Single-Source Ownership Rule Via Service Composition
- Patient Soft-Delete Does Not Cascade To Visits
- Implementation Sequence
- Frontend README — Next Js 14 Client
- Client-Side Password Rule
- OTP Email Verification Flow
- Radiology-Viewer Design Aesthetic

## God Nodes (most connected - your core abstractions)
1. `User` - 140 edges
2. `EntityNotFoundError` - 92 edges
3. `UserRole` - 82 edges
4. `Visit` - 57 edges
5. `get_db()` - 53 edges
6. `AnalysisOrchestrator` - 52 edges
7. `VisitStatus` - 50 edges
8. `get_current_active_user()` - 49 edges
9. `Analysis` - 45 edges
10. `AuthService` - 45 edges

## Surprising Connections (you probably didn't know these)
- `MAX_CONFIDENCE 0.92 Ceiling` --semantically_similar_to--> `Clinical Safety Boundary`  [INFERRED] [semantically similar]
  docs/REPORT-01D-frontend-checklist.md → AGENTS.md
- `404 Ownership Masking` --semantically_similar_to--> `Security and Privacy Rules`  [INFERRED] [semantically similar]
  docs/REPORT-01D-frontend-checklist.md → AGENTS.md
- `MRI Upload + Prediction Polling` --conceptually_related_to--> `V1 Exclusions`  [AMBIGUOUS]
  frontend/README.md → docs/PRD.md
- `Layered Architecture (API to Service to Repository to PostgreSQL)` --semantically_similar_to--> `Feature → API → Service → Repository → Model → Schema Flow`  [INFERRED] [semantically similar]
  docs/TRD.md → CONTRIBUTING.md
- `storage_key Deliberately Off the Wire` --semantically_similar_to--> `Security and Privacy Rules`  [INFERRED] [semantically similar]
  docs/REPORT-01D-frontend-checklist.md → AGENTS.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Per-Record Ownership Enforcement Pattern (404 masking, derived one hop up)** — docs_decisions_adr_001_ownership_violation_status_code_enumeration_resistance, docs_decisions_adr_002_visit_ownership_derivation_single_ownership_rule, docs_decisions_adr_002_visit_ownership_derivation_404_relabelling, docs_decisions_adr_002_visit_ownership_derivation_symptom_parent_check [EXTRACTED 1.00]
- **MVP Acceptance Journey Across Product, Scope and Implementation** — docs_prd_mvp_acceptance_journey, docs_neuroone_mvp_scope_mvp_definition, agents_demo_ready_definition, reports_progress_report_implemented_api_surface [EXTRACTED 1.00]
- **Three Independently Swappable Provider Seams** — agents_ai_01_contract_real_provider_mocked, docs_neuroone_mvp_scope_ai_02a_live_llm, docs_neuroone_mvp_scope_ai_02b_real_retrieval_corpus, agents_scan_staging_seam, agents_provenance_pipeline_note [EXTRACTED 1.00]
- **Frontend Reconnection Gap** — reports_progress_report_frontend_not_connected, docs_report_01d_frontend_checklist_baseline_finding, frontend_checklist_build_checklist, readme_dashboard_not_started, reports_progress_report_milestone_connect_frontend [INFERRED 0.95]
- **Three-Seam AI Provider Architecture (retrieval, reasoning, staging)** — docs_decisions_adr_003_ai_analysis_contract_and_provider_seam_evidenceretriever, docs_decisions_adr_003_ai_analysis_contract_and_provider_seam_llmclient, docs_decisions_adr_006_mri_primary_with_symptoms_as_context_staging_provider_seam, docs_decisions_adr_003_ai_analysis_contract_and_provider_seam_registry_build_providers [EXTRACTED 1.00]
- **Provider Selects, System Resolves (traceability containment)** — docs_decisions_adr_003_ai_analysis_contract_and_provider_seam_resolve_evidence, docs_decisions_adr_005_live_llm_provider_system_authored_trend_basis_uuids, docs_decisions_adr_005_live_llm_provider_derived_category, docs_decisions_adr_005_live_llm_provider_livecandidatepayload [EXTRACTED 1.00]
- **Honest Provenance Labelling Across Analysis, PDF and UI** — docs_decisions_adr_003_ai_analysis_contract_and_provider_seam_pipeline_note, docs_decisions_adr_005_live_llm_provider_hybrid_pipeline_note, docs_decisions_adr_006_mri_primary_with_symptoms_as_context_per_analysis_provenance, frontend_web_page_readme_design_boundaries [EXTRACTED 1.00]

## Communities (183 total, 51 thin omitted)

### Community 0 - "Visit & Symptom Domain Tests"
Cohesion: 0.06
Nodes (95): _symptom_page(), BaseModel, Symptom request and response schemas., A whitespace-only observation is the same as no observation, rejected rather…, Fields shared by symptom request and response schemas., Payload used to record a symptom against a visit., Payload used to partially update a symptom., Public symptom data returned by the API. (+87 more)

### Community 1 - "User Roles & Patient Service Tests"
Cohesion: 0.05
Nodes (71): Require the current user to have the administrator role., require_admin(), create_user(), Depends, post, Session, User, Administrator-only endpoints. (+63 more)

### Community 2 - "Analysis Persistence Layer"
Cohesion: 0.08
Nodes (58): AnalysisEvidence, AnalysisFinding, FindingCategory, BaseModel, Enum, str, One ranked candidate condition. Decision support, never a definitive diagnosis:…, One citation supporting one ranked finding. Scoped to a finding rather than to… (+50 more)

### Community 3 - "Analysis Orchestrator"
Cohesion: 0.09
Nodes (48): AnalysisOrchestrator, Re-attach evidence from the orchestrator's own retrieved set. A provider names…, Describe what actually produced this analysis. Derived from every provider that…, Execute the pipeline and return validated, ranked output., Runs the pipeline for one clinical context., Run imaging staging for the current visit, and a trend across it. Symptoms…, What the LLM provider returns. Validated at the seam, so a real provider in…, ReasoningResult (+40 more)

### Community 4 - "AI Provider Contracts & Clients"
Cohesion: 0.07
Nodes (37): _document(), MockCondition, Deterministic stand-in for a retrieval corpus and a reasoning model. Everything…, A rule mapping clinical findings to a candidate condition., Reason over the supplied context and evidence., LiveCandidatePayload, LiveLLMClient, LiveReasoningPayload (+29 more)

### Community 5 - "API Dependency Injection"
Cohesion: 0.11
Nodes (50): get_current_active_user(), get_db(), get_scan_service(), get_visit_service(), VisitService, Provide the configured scan service., Return the current user only when the account is active., Provide a database session and always close it after the request. (+42 more)

### Community 6 - "Report Rendering"
Cohesion: 0.11
Nodes (42): Render a complete, multi-page clinical report PDF. Raises whatever ReportLab…, render(), BaseModel, Clinical report contract (FR-07, ADR-004). ``ReportSnapshot`` is exactly what…, A generated report's metadata, as returned by the API. Deliberately excludes…, The patient/case identification FR-07 requires a report to carry., One clinical input as recorded for the visit (FR-03)., The clinical case the analysis was run against. (+34 more)

### Community 7 - "Analysis API & Report Creation"
Cohesion: 0.09
Nodes (34): get_analysis_service(), Provide the configured analysis service., create_report(), get_analysis(), list_reports(), Depends, ge, get (+26 more)

### Community 8 - "Analysis Output Schemas"
Cohesion: 0.10
Nodes (38): AnalysisResult, DiagnosisCandidate, FindingResponse, BaseModel, Structured differential-diagnosis contract (AGENTS.md section 8.2). Decision…, An early-watch flag must point at the patient's own history. Note the…, Validated pipeline output, before persistence., A ranked candidate as returned by the API. (+30 more)

### Community 9 - "Live LLM Reasoning Tests"
Cohesion: 0.13
Nodes (43): _analyze(), _candidates(), _context(), _evidence(), _llm(), A client whose model always answers with ``content``., One well-formed candidate payload, JSON-encoded as a model would., A provider selects evidence by id; it does not get to invent one. (+35 more)

### Community 10 - "Patients API"
Cohesion: 0.10
Nodes (40): get_patient_service(), Provide the configured patient service., create_patient(), delete_patient(), get_patient(), list_patients(), _paginated_response(), delete (+32 more)

### Community 11 - "Authentication Service"
Cohesion: 0.09
Nodes (30): Create a dependency that permits only the supplied user roles., require_roles(), TokenPayload, AuthService, UserService, Hash a plaintext password., Validate an access token and return its payload., Validate the reset code and set a new password. (+22 more)

### Community 12 - "Frontend Auth Pages & Validation"
Cohesion: 0.11
Nodes (27): AuthShell(), PasswordStrength(), Rule, RULES, Button, ButtonProps, Size, sizeClasses (+19 more)

### Community 13 - "AI Provider Wiring"
Cohesion: 0.09
Nodes (27): AI orchestration. Layering rule: nothing in this package imports a repository…, The AI pipeline (TRD section 8, APP-FLOW section 5). Clinical Case -> Normalize…, Drop uncited candidates, then rank and trim. A ranked condition without a…, EvidenceRetriever, ImagingStager, LLMClient, Protocol, The provider seam. This module is the entire surface AI-02 replaces. Everything… (+19 more)

### Community 14 - "Legacy Patient Detail UI"
Cohesion: 0.12
Nodes (23): PatientDetailPage(), ConfidenceDial(), ConfidenceDialProps, ClinicianTrustCard(), InteractiveMriViewer(), RegionInfo, REGIONS, ACCEPTED (+15 more)

### Community 15 - "Triage Queue"
Cohesion: 0.08
Nodes (27): get_triage_service(), Provide the configured triage service., get_triage_queue(), Depends, ge, get, le, Query (+19 more)

### Community 16 - "Analysis API Tests"
Cohesion: 0.14
Nodes (32): _analysis(), _client(), _db_override(), _evidence(), _finding(), TestClient, Contract tests for the analysis endpoints. Beyond the usual status/shape…, A consumer must be able to tell simulated evidence from live evidence. (+24 more)

### Community 17 - "Frontend API Client & Auth Provider"
Cohesion: 0.09
Nodes (28): js-cookie, lucide-react, load(), UploadPage(), onSubmit(), body, display, metadata (+20 more)

### Community 18 - "Analysis Service Tests"
Cohesion: 0.21
Nodes (32): _candidate(), _deny_visit(), _evidence(), Unit tests for AnalysisService. Two properties carry the weight here: that a…, AGENTS.md 8.4.4: source metadata must survive to persistence., The masked 404 must not disclose the visit or the patient behind it., Idempotent: no amendment flow exists yet to revoke a prior sign-off., _result() (+24 more)

### Community 19 - "Architecture Report Generator"
Cohesion: 0.18
Nodes (31): Document, RGBColor, add_body(), add_bullets(), add_callout(), add_code(), add_cover(), add_field() (+23 more)

### Community 20 - "MRI Staging Tests"
Cohesion: 0.15
Nodes (27): Normalize Input + Build Clinical Context (TRD section 8, stages 1-2). This is…, Map a Visit and its live symptoms into the AI-facing shape., _to_context_visit(), ContextSymptom, ContextVisit, BaseModel, Normalized clinical context supplied to the AI pipeline. This is the "Build…, A symptom as the AI layer sees it. (+19 more)

### Community 21 - "Patient Service"
Cohesion: 0.15
Nodes (19): BaseModel, User model definitions., User, PatientService, Patient, Session, UUID, Business logic for patient management. (+11 more)

### Community 22 - "Visit Service"
Cohesion: 0.15
Nodes (16): Session, UUID, Open a clinical case for a patient the caller owns. The patient id came from…, Retrieve a visit by ID. Ownership violations read as 404., Return a patient's visit history ordered for trend comparison. This is the in-…, Partially update a visit. Ownership violations read as 404., Soft-delete a visit and its symptoms., List a visit's symptoms in recording order. (+8 more)

### Community 23 - "Frontend Package Manifests"
Cohesion: 0.09
Nodes (27): autoprefixer, axios, eslint, eslint-config-next, next, postcss, react, react-dom (+19 more)

### Community 24 - "MRI Staging Seam"
Cohesion: 0.12
Nodes (22): Return a stage estimate for the supplied scan metadata., MockImagingStager, Deterministic stand-in for an MRI staging model (ADR-006). The stage estimate…, Deterministic stage estimate derived from the scan's checksum., Derive a stage, confidence and region breakdown from the checksum., BaseModel, Imaging staging contract (ADR-006). A third provider seam alongside the…, One anatomical region's weight in a staging estimate. Descriptive detail only.… (+14 more)

### Community 25 - "Report Persistence"
Cohesion: 0.15
Nodes (22): BaseModel, One generated PDF report, snapshotting its source analysis. Never mutated after…, Report, Session, UUID, Report persistence operations., Provide report-specific queries in addition to common CRUD., Return an analysis's reports, newest first. (+14 more)

### Community 26 - "Patient Repository"
Cohesion: 0.13
Nodes (15): PatientRepository, Patient, Session, UUID, Patient persistence operations., Count active patients assigned to a doctor., Return the active patient with the given phone number, if any., Provide patient-specific queries in addition to common CRUD operations. (+7 more)

### Community 27 - "Auth API & Token Schemas"
Cohesion: 0.20
Nodes (25): get_auth_service(), Provide the configured authentication service., forgot_password(), login(), Depends, post, Session, Authentication endpoints. (+17 more)

### Community 28 - "Core Domain Models"
Cohesion: 0.13
Nodes (17): Persisted AI analysis, its ranked findings, and their citations. Naming is…, Immutable snapshot of a generated clinical report (ADR-004)., BaseModel, MRI scan metadata for a visit (ADR-006). The scan's bytes are not a column here…, One MRI scan attached to a visit. Attaches to the Visit, not the Patient…, Scan, Symptom model definitions., BaseModel (+9 more)

### Community 29 - "Trend Detection"
Cohesion: 0.16
Nodes (25): detect_trends(), Normalized names of symptoms that are getting worse across visits. This is the…, Detect per-symptom severity trends across a patient's visits. ``visits`` must…, worsening_symptom_names(), How one symptom moved across a patient's visits. Only symptoms observed at two…, SymptomTrend, Tests for cross-visit trend detection. A trend is what an early_watch flag…, symptoms: (name, severity) tuples. (+17 more)

### Community 30 - "Scan Storage Backend"
Cohesion: 0.11
Nodes (18): Storage backends for artifacts that do not belong in the database., LocalScanStorage, Protocol, UUID, Storage for MRI scan bytes, outside the database (ADR-006 decision 5). A PDF…, Where a scan's bytes live, addressed by an opaque storage key., Persist ``content`` and return its storage key., Remove previously saved content. Missing content is not an error. (+10 more)

### Community 31 - "Report Service Tests"
Cohesion: 0.20
Nodes (25): _analysis(), _evidence(), _finding(), _patient(), Unit tests for ReportService. Two properties carry the weight, mirroring…, The masked 404 must not disclose the analysis behind it., _service(), _symptom() (+17 more)

### Community 32 - "Mock Provider Tests"
Cohesion: 0.15
Nodes (22): _analyze(), _context(), Tests for the mocked retriever and reasoner. Two properties matter most here.…, A stage estimate with no resolvable citation would be silently dropped., The fixture must not read as real literature., AGENTS.md 8.2: confidence is likelihood, never certainty., The property a seeded RNG or a canned fixture would not have., AGENTS.md 8.1: schema-valid deterministic results. (+14 more)

### Community 33 - "Landing Page 3D Scenes"
Cohesion: 0.10
Nodes (16): R3fCanvasScene, FloatingParticles(), Particle, PARTICLES, StoryCard3D(), StoryCardProps, Edge, EDGES (+8 more)

### Community 34 - "Parked Design System"
Cohesion: 0.10
Nodes (24): 1. Brand identity, 2. Color system, 3. Typography, 4. Login screen, 5. Open items, Brand (login screen, decorative panel, marketing surfaces), Brand Color Palette, Cormorant Garamond Fallback (+16 more)

### Community 35 - "Patient Visits API"
Cohesion: 0.14
Nodes (23): alias, create_visit(), get_visit_history(), list_patient_visits(), Depends, ge, get, le (+15 more)

### Community 36 - "Error Handling & Exceptions"
Cohesion: 0.19
Nodes (21): Top-level API router., ErrorResponse, The standard shape returned for API errors., ApplicationError, ConflictError, DatabaseError, ExternalServiceError, NotFoundError (+13 more)

### Community 37 - "Report API Tests"
Cohesion: 0.19
Nodes (22): AnalysisNotReviewedError, InternalServerError, Raised when a report is requested for an unreviewed analysis. ADR-006 decision…, _client(), _db_override(), TestClient, Contract tests for the report endpoints. Beyond the usual status/shape…, ADR-006 decision 6: sign-off gates the report. (+14 more)

### Community 38 - "Live LLM Provider Tests"
Cohesion: 0.13
Nodes (23): Tests for the live reasoning provider (AI-02 slice 1, ADR-005). A live model is…, The model names a symptom; the system resolves the ids (ADR-005)., The ADR-003 invariant holds by construction, not by raising., early_watch is a low-confidence watch, not a confident finding. A real model…, The seam exists so a category cannot mean two things (ADR-005)., No UUID reaches the model, so none can come back (ADR-005)., The retriever is still mocked, so the note must not claim otherwise., The canonical demo case: tremor 3 -> 5 -> 8 across three visits. (+15 more)

### Community 39 - "Clinical Context Building"
Cohesion: 0.20
Nodes (22): _age_years(), build_clinical_context(), date, Patient, Whole years, so a date of birth never reaches the reasoning layer., Assemble the context the AI pipeline reasons over. ``prior_visits`` must be…, _patient(), Tests for the ORM -> ClinicalContext normalize stage. The PHI-minimization… (+14 more)

### Community 40 - "Architecture Decision Rationale"
Cohesion: 0.09
Nodes (23): AnalysisRepository.create_with_status, ClinicalContext, Database-Free app/ai Package, Failure Precedes the First Write, MAX_CONFIDENCE Ceiling of 0.92, A Failed Run Persists Nothing, Re-Running Analysis Creates a New Row, Rule-Based Deterministic Mock Scoring (+15 more)

### Community 41 - "Evidence Retrieval Seam"
Cohesion: 0.13
Nodes (18): MockEvidenceRetriever, _normalize(), Deterministic stand-in for a literature retriever. Matches the query against a…, Keyword retriever over the frozen mock corpus., Return matching documents, most relevant first. An empty result is a legitimate…, What the orchestrator asks the retriever for., RetrievalQuery, Section 8.5: the clinical record survives a provider failure. (+10 more)

### Community 42 - "TypeScript Configuration"
Cohesion: 0.09
Nodes (21): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+13 more)

### Community 43 - "Scan Intake Service"
Cohesion: 0.12
Nodes (14): Retrieve the scan attached to a visit, if any., Session, UUID, Scan persistence operations., Provide scan-specific queries in addition to common CRUD., Return the active scan attached to a visit, if any., ScanRepository, Session (+6 more)

### Community 44 - "Legacy Mockup Dashboard"
Cohesion: 0.11
Nodes (12): ACCENTS, AVATAR_PALETTES, hexToRgb01(), NeuralBackground(), PatientRow, PATIENTS, RadialGauge(), SCAN_VOLUME (+4 more)

### Community 45 - "BaseModel"
Cohesion: 0.12
Nodes (15): Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), Database engine and session configuration., Base, BaseModel, Base model definition. (+7 more)

### Community 46 - "Symptom"
Cohesion: 0.15
Nodes (13): BaseModel, A neurological symptom recorded against a clinical case., Symptom, Session, UUID, Symptom persistence operations., Provide symptom-specific queries in addition to common CRUD operations., Return a visit's active symptoms in recording order. (+5 more)

### Community 47 - "BaseRepository"
Cohesion: 0.18
Nodes (11): BaseRepository, Session, UUID, Soft-delete an entity. Marks the entity as deleted by setting the `is_deleted`…, Check whether a record exists. Returns True if an active record with the given…, Create a new database record and persist it. Adds the model instance to the…, Retrieve a single record by its unique identifier. Returns the entity if it…, Retrieve all active records. Returns a list of all entities that have not been… (+3 more)

### Community 48 - "VisitRepository"
Cohesion: 0.28
Nodes (17): Provide visit-specific queries in addition to common CRUD operations., VisitRepository, _engine(), Real-database tests for cross-visit history retrieval. These run against SQLite…, The loader criteria, not just the read path, must filter soft deletes., Regression guard for the N+1 the selectinload exists to prevent. One SELECT for…, test_get_by_patient_paginates_and_filters_by_status(), test_get_with_symptoms_hides_soft_deleted_visits() (+9 more)

### Community 49 - "ReportSnapshot (typed JSONB Snapshot)"
Cohesion: 0.13
Nodes (19): Alembic Migration Policy, Team Repository Ownership Matrix, AIError Controlled Failure, analyses / analysis_findings / analysis_evidence Tables, Evidence Scoped to a Finding, Not a Report, EvidenceRef (narrowed wire shape), _resolve_evidence Orchestrator Stage, RetrievedDocument (+11 more)

### Community 50 - "NeuroOne Frontend — Redesign Checklist"
Cohesion: 0.11
Nodes (19): Confirmed Roles ADMIN and CLINICIAN, Users: Clinician and Administrator, Account & Settings, Admin, Admin Screens, Auth, Frontend Redesign Build Checklist, Clinical Input (+11 more)

### Community 51 - "Compileroptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 52 - "FR-04 Differential Diagnosis"
Cohesion: 0.15
Nodes (18): Early-Detection Design, python-multipart, Early-Detection Design (confirmed), FR-04 Differential Diagnosis, FR-08 Scan Intake and Staging, Suggested Build Order, MAX_CONFIDENCE 0.92 Ceiling, seed_demo_case.py Predates ADR-006 (+10 more)

### Community 53 - "Test Auth Api"
Cohesion: 0.22
Nodes (16): _client(), _db_override(), TestClient, Integration-style contract tests for authentication endpoints., test_admin_can_create_user_without_returning_password(), test_clinician_cannot_create_users(), test_duplicate_user_is_conflict(), test_expired_token_returns_controlled_401() (+8 more)

### Community 54 - "ADR-006: MRI Becomes A Primary Input, With Symptoms As Conte"
Cohesion: 0.12
Nodes (12): ADR-002 — Visit Ownership Derives From Parent Patient, ADR-006: MRI Becomes a Primary Input, With Symptoms as Context, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact (+4 more)

### Community 55 - "Early Watch Category Derived From Trend Evidence"
Cohesion: 0.12
Nodes (18): DiagnosisCandidate, early_watch Category Derived From Trend Evidence, pipeline_note Provenance Label, provider_mode, ReasoningResult, trend_basis as a JSON Column, category Is Derived, Not Accepted, HYBRID_PIPELINE_NOTE (+10 more)

### Community 56 - "Backend Tests Workflow"
Cohesion: 0.12
Nodes (17): Alembic Heads Check, Backend Tests Workflow, Pytest Run, Architectural Decision Records, Client to API to Service to Repository Layering, Transaction Boundary Ownership (open convention), alembic, pytest (+9 more)

### Community 57 - "Security And Privacy Rules"
Cohesion: 0.12
Nodes (17): Security and Privacy Rules, AI-02b Real Retrieval Corpus (deferred), Synthetic Demo Data Assumption, FR-03 Clinical Input, AI-Owned analyzed Visit Status, Scan Intake Contract, ScanResponse, storage_key Deliberately Off the Wire (+9 more)

### Community 58 - "Datetime"
Cohesion: 0.18
Nodes (15): _build_story(), _draw_footer(), _finding_label(), _p(), Render a ReportSnapshot into a complete clinical report PDF (ADR-004). A pure…, Escape Platypus markup and fall back for characters base14 can't render.…, _render_finding(), _safe() (+7 more)

### Community 59 - "Test Scan Service"
Cohesion: 0.34
Nodes (16): _deny_visit(), Unit tests for ScanService (ADR-006). Mirrors test_report_service.py's shape:…, ADR-006 decision 2: one scan per visit., _service(), test_a_second_scan_on_the_same_visit_is_a_conflict_and_cleans_up_storage(), test_an_empty_file_is_rejected(), test_an_oversized_file_is_rejected(), test_get_scan_on_a_scanless_visit_is_a_missing_scan() (+8 more)

### Community 60 - "Two Narrow Protocol Provider Seam"
Cohesion: 0.13
Nodes (17): Enumeration Resistance for PHI-Adjacent Resources, Ownership Violations Return 404, Not 403, Server-Side Audit Logging of the Real Reason, 404 Re-Labelling / Identifier Masking, Symptom-Belongs-To-Visit Verification, EvidenceRetriever Protocol, LLMClient Protocol, registry.build_providers() (+9 more)

### Community 61 - "Dependencies"
Cohesion: 0.12
Nodes (17): dependencies, axios, clsx, framer-motion, @hookform/resolvers, js-cookie, lucide-react, next (+9 more)

### Community 62 - "Useauth"
Cohesion: 0.15
Nodes (13): DashboardLayout(), NAV_ITEMS, DashboardPage(), SortHeader(), toggleSort(), ForgotPasswordPage(), LoginForm(), handleOtpLogin() (+5 more)

### Community 63 - "Page"
Cohesion: 0.16
Nodes (8): VerifyOtpForm(), OtpInput(), commit(), handleChange(), handlePaste(), AuthShell(), SynapseArtwork(), react

### Community 64 - "Api"
Cohesion: 0.15
Nodes (8): api, ApiClient, ApiError, ApiResponse, extractApiError(), LoginResponse, OtpResponse, OtpVerifyResponse

### Community 65 - "AI Output Contract"
Cohesion: 0.13
Nodes (16): AI Output Contract, Clinical Safety Boundary, Definition of Done, Document Precedence, Sources of Truth, trend_basis Distinct from evidence, MVP Definition (locked), USP Framing as Vision Narrative (+8 more)

### Community 66 - "Test Otp Service"
Cohesion: 0.26
Nodes (13): generate_and_send_otp(), _OtpEntry, Generates a 6-digit OTP, stores it, and emails it via Gmail SMTP., Checks a submitted OTP against the stored one. The code is only consumed…, verify_otp(), Tests for the OTP generation/verification helpers behind password reset., _stub_smtp(), test_code_is_burned_after_max_attempts() (+5 more)

### Community 67 - "MVP Acceptance Journey"
Cohesion: 0.14
Nodes (15): Demo-Ready Definition, bcrypt, passlib, python-jose, Definition of Demo-Ready MVP, FR-01 Authentication, FR-02 Patient Management, MVP Acceptance Journey (+7 more)

### Community 68 - "UserAlreadyExistsError"
Cohesion: 0.20
Nodes (10): Email a reset code if the address belongs to an active account. Always returns…, Session, UserCreate, UserResponse, Email an OTP if the address belongs to an active account. Always returns…, Provision a staff user after enforcing the ADMIN boundary., Create the first administrator, and only when none exists., Create a user after uniqueness checks and password hashing. (+2 more)

### Community 69 - "Test Security"
Cohesion: 0.21
Nodes (13): create_access_token(), decode_access_token(), hash_password(), Any, Password hashing and JSON Web Token helpers., Hash a plaintext password using the configured password context., Verify a plaintext password against a stored hash., Create a signed access token from the supplied claims. (+5 more)

### Community 70 - "Per-Record Ownership Check"
Cohesion: 0.13
Nodes (15): Coding Standards (type hints, PEP 8, services own business logic), Feature → API → Service → Repository → Model → Schema Flow, EntityNotFoundError, PatientService._authorize_access, Per-Record Ownership Check, require_roles Role-Level 403 Signaling, detect_trends Must Be Extended for Scan Metrics, Intake Splits Into New Patient and New Visit (+7 more)

### Community 71 - "Interactive-pipeline-demo"
Cohesion: 0.22
Nodes (12): CASESHOTS, InteractivePipelineDemo(), SampleCase, RegionBars(), ApiError, AuthTokens, DiseaseLabel, DiseaseStage (+4 more)

### Community 72 - "Trends"
Cohesion: 0.20
Nodes (13): detect_stage_trend(), _direction(), UUID, Cross-visit symptom trend detection. This is the mechanism behind AGENTS.md…, Detect how an imaging-derived stage moved across a patient's visits. Mirrors…, Build history references for a worsening imaging-derived stage trend. Mirrors…, Classify a severity series ordered oldest-first., stage_trend_basis_ref() (+5 more)

### Community 73 - "Visit"
Cohesion: 0.20
Nodes (11): _as_utc(), datetime, field_validator, Clinical case / visit request and response schemas., Normalize a naive datetime to UTC so ordering never mixes tz-awareness., Vital signs recorded at a visit. Persisted as JSON, so this schema is the only…, Fields shared by visit request and response schemas., Payload used to partially update a visit. Deliberately has no ``symptoms``… (+3 more)

### Community 74 - "ADR-003: AI Analysis Contract And The Mocked-Provider Seam"
Cohesion: 0.14
Nodes (14): Addendum: evidence-resolution correction (pre-`REPORT-01`), ADR-003: AI Analysis Contract and the Mocked-Provider Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact (+6 more)

### Community 75 - "REPORT-01D — Frontend Requirements & Backend Mapping Checkli"
Cohesion: 0.22
Nodes (14): 0. Baseline finding: this is not a "reconcile," it's mostly new pages, 1. Auth, 1A. Triage queue — the dashboard (ADR-006 decision 7), 2. Patients, 3. Clinical Case (Visit) + Symptoms, 3A. Scan intake (ADR-006 decisions 1, 2, 5), 4. AI Analysis + Differential Diagnosis + Evidence, 5. Clinician Sign-off → PDF Report (+6 more)

### Community 76 - "Reports"
Cohesion: 0.24
Nodes (12): get_report_service(), Provide the configured report service., download_report_pdf(), get_report(), Depends, get, Session, UUID (+4 more)

### Community 77 - "Get By Patient"
Cohesion: 0.26
Nodes (7): Session, UUID, Eager-load each visit's live symptoms in one extra query. selectinload rather…, Return an active visit with its live symptoms loaded., Return a patient's active visits, newest first., Count a patient's active visits., Return a patient's visit history ordered for trend comparison. This is the…

### Community 78 - "Test Scan Api"
Cohesion: 0.33
Nodes (11): _client(), _db_override(), TestClient, Contract tests for the scan endpoints (ADR-006)., _scan(), test_getting_a_scan_on_a_scanless_visit_is_404(), test_getting_a_visits_scan_succeeds(), test_uploading_a_scan_returns_201_with_metadata() (+3 more)

### Community 79 - "ADR-004: Clinical Report Snapshot And Rendering"
Cohesion: 0.15
Nodes (13): ADR-004: Clinical Report Snapshot and Rendering, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 80 - "ADR-005: Live LLM Provider Behind The AI-01 Seam"
Cohesion: 0.15
Nodes (13): ADR-005: Live LLM Provider Behind the AI-01 Seam, Alternatives Rejected, Consequences, Constraints, Context, Decision, Migration / Rollback Impact, Options Considered (+5 more)

### Community 81 - "Current Development Status Table"
Cohesion: 0.18
Nodes (12): Repository Inspection Rules, REPORT-01D Contract Map, Authentication Complete, Backend APIs Complete (35 endpoints, 400 tests), Dashboard Not Started Against Real Data, Explainable AI in the API, Not the UI, Current Development Status Table, Status Stated Plainly (+4 more)

### Community 82 - "Test Triage Api"
Cohesion: 0.30
Nodes (10): _client(), _db_override(), _entry(), TestClient, Contract tests for the triage endpoint (ADR-006)., FR-04: no stat tile, no aggregate confidence number., test_an_entry_carries_no_field_that_frames_output_as_a_measurement(), test_default_pagination_is_page_one() (+2 more)

### Community 83 - "Devdependencies"
Cohesion: 0.17
Nodes (12): devDependencies, autoprefixer, eslint, eslint-config-next, postcss, tailwindcss, @types/js-cookie, @types/node (+4 more)

### Community 84 - "NeuroONE Agent Operating Contract"
Cohesion: 0.25
Nodes (11): NeuroONE Agent Operating Contract, BUILD Mode, DEBUG Mode, PLAN Mode, TEST Mode, Graphify Knowledge Graph Convention, Generate API Types From openapi.json, backend-routes.json OpenAPI Dump (+3 more)

### Community 85 - "Generate Report"
Cohesion: 0.27
Nodes (7): Session, UUID, Build, render, and persist a new report for an analysis. Render-before-persist…, Retrieve one report by ID. The caller named only the report, so an…, List an analysis's reports, newest first., Re-render a report's PDF bytes from its immutable snapshot., _render_or_fail()

### Community 86 - "Error Response"
Cohesion: 0.31
Nodes (11): _error_response(), http_exception_handler(), Exception, request_validation_error_handler(), unhandled_error_handler(), validation_error_handler(), JSONResponse, Request (+3 more)

### Community 87 - "Devdependencies (2)"
Cohesion: 0.18
Nodes (11): devDependencies, autoprefixer, eslint, eslint-config-next, postcss, tailwindcss, @types/js-cookie, @types/node (+3 more)

### Community 88 - "Dependencies (2)"
Cohesion: 0.22
Nodes (9): get_current_user(), Depends, Session, Reusable FastAPI dependencies for database and access control., Validate the bearer token and return its associated user., Require the current user to have the clinician role., require_clinician(), get_current_clinician (+1 more)

### Community 89 - "Init"
Cohesion: 0.20
Nodes (7): MessageResponse, Pagination, Schemas shared across application features., Pagination metadata returned with collection responses., A simple response containing a human-readable message., Public schema exports., Helpers for consistent API responses.

### Community 90 - "NeuroOne Login Neurons Artwork V1"
Cohesion: 0.38
Nodes (10): NeuroOne Login Neurons Artwork v1, Dark Indigo Gradient Background, Decorative Non-Informational Asset Role, Dual Neuron Diagonal Composition, Neural Brand Identity Signal, Parked Login Design Reference, Portrait Split-Panel Login Slot, Golden Synapse Spark Focal Point (+2 more)

### Community 91 - "AI-01 Contract-Real Provider-Mocked"
Cohesion: 0.25
Nodes (9): AI-01 Contract-Real Provider-Mocked, AI / RAG Pipeline, Locked Roadmap and Sequencing, httpx, ADR-005 Live LLM Provider, AI-02a Live LLM Provider, AI Phasing Decision, Investor/Stakeholder Demo Purpose (+1 more)

### Community 92 - "Main"
Cohesion: 0.25
Nodes (5): health(), get, root(), Compatibility entry point for running ``uvicorn main:app``., Regenerate backend-routes.json from the live FastAPI application. The file is…

### Community 93 - "Verify Credentials"
Cohesion: 0.25
Nodes (4): Authenticate a user and issue an access token directly (no OTP step)., Create an access token for a user., Verify credentials and OTP together, then issue an access token. This flow…, Validates username/email + password and returns the User, without issuing a…

### Community 94 - "Error Handling Contract"
Cohesion: 0.25
Nodes (8): AI Failure Safety, Centralized Error Handling Rules, Non-Functional Requirements, 404 Ownership Masking, ApiError, Baseline Finding: Mostly New Pages, Error Handling Contract, extractApiError

### Community 95 - "Three Provenance States And Pipeline Note"
Cohesion: 0.32
Nodes (8): Three Provenance States and pipeline_note, Scan Staging Provider Seam (SCAN-02), Mocked AI Credibility Risk, Analysis and Evidence Contract, AnalysisResponse, Contributing Regions Visualization Has No API, AI Pipeline Contract Complete, Providers Simulated, Mocked Staging Model Reads as Measurement

### Community 96 - "Likelihood Band For"
Cohesion: 0.36
Nodes (6): likelihood_band_for(), Confidence-tiered output (section 8.3). This is what UI copy and the PDF should…, Derived from confidence, never read from the row., Tier a confidence value (AGENTS.md section 8.3). Derived, never stored: a…, computed_field, LikelihoodBand

### Community 97 - "FR-07 Clinical Report"
Cohesion: 0.29
Nodes (8): pypdf, reportlab, FR-07 Clinical Report, Sign-Off Is a Gate, Not a Status, ReportResponse, Clinician Sign-off to PDF Report, Report Preview Page Has No API, Reports Screens

### Community 98 - "Dependencies (3)"
Cohesion: 0.25
Nodes (8): dependencies, axios, js-cookie, lucide-react, next, react, react-dom, zod

### Community 99 - "NeuroONE Frontend Redesign (parked)"
Cohesion: 0.25
Nodes (7): Sign in via OTP Button Replaces Google Sign-In, Account-flow handoff, Design implementation, Files in this change, NeuroONE Frontend Redesign (parked), Parked state, Preview

### Community 100 - "ADR-006 MRI Primary With Symptoms As Context"
Cohesion: 0.38
Nodes (7): V1 Scope Guard, APP-FLOW V1 Boundary, ADR-006 MRI Primary With Symptoms as Context, Revised Exclusions, V1 Exclusions, Explicit Frontend Non-Goals, MRI Upload + Prediction Polling

### Community 101 - "Get User Service"
Cohesion: 0.33
Nodes (6): get_user_service(), UserService, Provide the configured user service., main(), Create NeuroONE's first administrator without a public endpoint., _value()

### Community 102 - "EvidenceRef"
Cohesion: 0.29
Nodes (6): EvidenceResponse, A citation as returned by the API., EvidenceRef, BaseModel, Literature evidence schemas. ``EvidenceRef`` is exactly the three fields…, A citation attached to a ranked candidate. Traces to EXTERNAL literature. Not…

### Community 103 - "Test Deleted At Timezone Migration"
Cohesion: 0.43
Nodes (6): _load_migration(), Regression tests for the deleted_at timezone migration., test_downgrade_restores_naive_timestamps(), test_migration_chains_from_case_01(), test_upgrade_uses_implicit_timezone_cast(), ModuleType

### Community 104 - "Eslintrc"
Cohesion: 0.33
Nodes (4): extends, next/core-web-vitals, extends, root

### Community 105 - "Scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

### Community 106 - "14056b8ec27d Create Scans"
Cohesion: 0.40
Nodes (4): downgrade(), Create the scans table (ADR-006). No image bytes column: only the storage…, Drop the scans table., upgrade()

### Community 107 - "1f74d19af1b8 Widen Patient Email And Promote Phone"
Cohesion: 0.40
Nodes (4): downgrade(), Widen patients.email to 255 chars and give patient_phones the standard…, Restore the legacy integer-keyed patient_phones and 20-char email., upgrade()

### Community 108 - "7544ad0b1ed6 Add Analysis Sign Off"
Cohesion: 0.40
Nodes (4): downgrade(), Add clinician sign-off columns to analyses (ADR-006 decision 6). Both nullable…, Drop the sign-off columns., upgrade()

### Community 109 - "8e72c1f4a9b0 Replace Legacy User Roles"
Cohesion: 0.40
Nodes (4): downgrade(), Rename DOCTOR and remove the deferred RECEPTIONIST role safely., Restore the legacy role enum., upgrade()

### Community 110 - "A3c7be51d904 Create Visits And Symptoms"
Cohesion: 0.40
Nodes (4): downgrade(), Drop the symptom and visit tables, and the enum type they created., Create the clinical case (visit) and symptom tables. The composite (patient_id,…, upgrade()

### Community 111 - "B2b31bad27df Add Symptom Observation"
Cohesion: 0.40
Nodes (4): downgrade(), Add the clinician-entered observation field (FR-03). Nullable, so every…, Drop the observation column., upgrade()

### Community 112 - "B8d41e2f7c53 Make Deleted At Timezone Aware"
Cohesion: 0.40
Nodes (4): downgrade(), Widen deleted_at from timestamp to timestamptz. No USING clause, deliberately.…, Narrow deleted_at back to a naive timestamp. Symmetric with upgrade(): the…, upgrade()

### Community 113 - "C4e19a7b6d20 Create Analyses Findings And Evidence"
Cohesion: 0.40
Nodes (4): downgrade(), Drop the analysis tables and the enum type they created., Create the AI analysis tables. No drops. The abandoned Diagnosis and Rag stubs…, upgrade()

### Community 114 - "Dcfbc7d5b2c9 Create Reports"
Cohesion: 0.40
Nodes (4): downgrade(), Create the reports table (ADR-004). No pdf_path and no binary PDF column: only…, Drop the reports table., upgrade()

### Community 116 - "Scripts (2)"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

### Community 117 - "Middleware"
Cohesion: 0.40
Nodes (3): AUTH_PAGES, config, PROTECTED_PREFIXES

### Community 118 - "Validation"
Cohesion: 0.40
Nodes (4): LoginFormData, loginSchema, OtpFormData, otpSchema

### Community 119 - "Q: How Are Alembic Migrations And Backend Tests Configured, "
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: How are Alembic migrations and backend tests configured, and where should PR CI run pytest?, Source Nodes

### Community 120 - "Q: The Parallel AI-01 Work Is Committed And Pulled; Plan Our"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: The parallel AI-01 work is committed and pulled; plan our next work, Source Nodes

### Community 121 - "Read Current User"
Cohesion: 0.50
Nodes (4): get, UserResponse, Return the identity associated with the bearer token., read_current_user()

### Community 124 - "Seed"
Cohesion: 0.67
Nodes (3): main(), Seed a demo patient whose history contains a multi-visit trend. AGENTS.md…, seed()

### Community 125 - "RAG Requirements"
Cohesion: 1.00
Nodes (3): RAG Requirements, FR-05 Literature Retrieval, FR-06 Explainability

### Community 132 - "Api Service (fastapi Backend)"
Cohesion: 0.67
Nodes (3): api service (FastAPI backend), db service (postgres:16-alpine), Health-Gated Service Startup

### Community 133 - "Clinician Review Flow"
Cohesion: 0.67
Nodes (3): Evidence Flow (Retrieval → Ranking → Citation), Report Flow (Report Builder → PDF), Clinician Review Flow

## Ambiguous Edges - Review These
- `MRI Upload + Prediction Polling` → `V1 Exclusions`  [AMBIGUOUS]
  frontend/README.md · relation: conceptually_related_to
- `Standard API Response Envelope` → `Assumed Backend API Contract`  [AMBIGUOUS]
  frontend/README.md · relation: conceptually_related_to
- `httpx` → `AI-02a Live LLM Provider`  [AMBIGUOUS]
  backend/requirements.txt · relation: conceptually_related_to
- `Golden Synapse Spark Focal Point` → `Neural Brand Identity Signal`  [AMBIGUOUS]
  frontend/web-page/public/images/neuroone-login-neurons-v1.png · relation: conceptually_related_to
- `Teal and Violet Accent Pair` → `Neural Brand Identity Signal`  [AMBIGUOUS]
  frontend/web-page/public/images/neuroone-login-neurons-v1.png · relation: conceptually_related_to

## Knowledge Gaps
- **331 isolated node(s):** `OtpInput`, `PatientRow`, `ConfidenceDialProps`, `Edge`, `Node` (+326 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1003 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **51 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `MRI Upload + Prediction Polling` and `V1 Exclusions`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Standard API Response Envelope` and `Assumed Backend API Contract`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `httpx` and `AI-02a Live LLM Provider`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Golden Synapse Spark Focal Point` and `Neural Brand Identity Signal`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Teal and Violet Accent Pair` and `Neural Brand Identity Signal`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `User` connect `Patient Service` to `Visit & Symptom Domain Tests`, `User Roles & Patient Service Tests`, `Analysis Persistence Layer`, `API Dependency Injection`, `Report Rendering`, `Analysis API & Report Creation`, `Patients API`, `Authentication Service`, `Triage Queue`, `Analysis API Tests`, `Analysis Service Tests`, `Visit Service`, `Auth API & Token Schemas`, `Core Domain Models`, `Report Service Tests`, `Patient Visits API`, `Report API Tests`, `Scan Intake Service`, `Symptom`, `Test Auth Api`, `Test Scan Service`, `UserAlreadyExistsError`, `Reports`, `Test Scan Api`, `Test Triage Api`, `Generate Report`, `Dependencies (2)`, `Verify Credentials`, `Read Current User`, `Seed`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Why does `AnalysisOrchestrator` connect `Analysis Orchestrator` to `Analysis Persistence Layer`, `AI Provider Contracts & Clients`, `Live LLM Provider Tests`, `Analysis API & Report Creation`, `Analysis Output Schemas`, `Trends`, `Evidence Retrieval Seam`, `AI Provider Wiring`, `MRI Staging Tests`, `MRI Staging Seam`, `Dependencies (2)`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._