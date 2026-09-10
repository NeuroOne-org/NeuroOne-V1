# AGENTS.md — NeuroONE Agent Operating Contract

**Status:** Active · MVP / V1
**Applies to:** every AI coding or planning agent operating in the NeuroONE repository.

---

## 1. Purpose

This file defines how AI agents must work inside **NeuroONE**.

An agent here is not primarily a code generator. Its first responsibility is to **understand the current state, reason about architecture, identify the next correct work, document the decision, and only then implement**.

The default operating mode is **PLAN**.

Do not move from an idea to implementation unless the work has already been planned and the plan is specific enough to build from.

> A correct implementation of the wrong architecture is still a failure.

---

## 2. Project Context

NeuroONE is a **clinical decision-support platform for neurological case evaluation**. It combines structured clinical information, trusted medical literature, retrieval, and AI reasoning to produce an **explainable differential diagnosis**.

MVP acceptance journey (PRD §8) — the contractual definition of done for the MVP:

```text
Login → Patient → Case → Symptoms → AI Analysis
  → Differential Diagnosis + Evidence → Clinician Review → PDF Report
```

Observable application flow (APP-FLOW §1) — the same journey as the user experiences it:

```text
LOGIN → DASHBOARD → PATIENT → CASE → SYMPTOMS / CLINICAL INPUT
  → AI ANALYSIS → DIFFERENTIAL DIAGNOSIS → EVIDENCE + CITATIONS
  → CLINICIAN REVIEW → REPORT
```

Use the PRD form when stating acceptance criteria; use the APP-FLOW form when reasoning about screens and transitions.

### 2.1 Clinical safety boundary — non-negotiable

NeuroONE **assists** clinicians. It must never be built, described, or presented as:

- an autonomous diagnostic system,
- a replacement for clinician judgment,
- an automated treatment decision system.

The clinician remains responsible for final interpretation. Every generated report carries an appropriate disclaimer (FR-07).

This boundary holds regardless of audience, phase, or marketing framing. The confirmed USP narrative — early detection of neurodegenerative disease — is **vision language wrapping a clinician-assist tool**, not a literal autonomous-diagnosis claim. Do not let product copy migrate into product behavior.

### 2.2 Current MVP purpose

The MVP is an **investor/stakeholder demo**. The bar is "demonstrates the full product concept convincingly end-to-end," not "production-grade clinical deployment."

This relaxes rigor expectations for **AI/RAG implementation depth only**. It does **not** relax:

- security,
- layer boundaries,
- typed contracts,
- the clinical safety boundary,
- data integrity.

---

## 3. Sources of Truth

Before planning, debugging, building, or testing, read the relevant documents.

| Document | Authority | Use it for |
|---|---|---|
| `PRD.md` | Product | Goals, users, FR-01–FR-07, non-functional requirements, safety boundary, acceptance journey, V1 exclusions |
| `APP-FLOW.md` | Behavior | User flows, system transitions, AI flow, evidence flow, review flow, report flow, failure flows |
| `TRD.md` | Technical | Architecture, layering, stack, database rules, auth, AI/RAG pipeline, AI contracts, error handling, testing, implementation sequence |
| `NEUROONE-MVP-SCOPE.md` | Locked scope decisions | Current phase scope, AI phasing, roles, early-detection design, roadmap ordering, demo-ready definition |

### 3.1 Precedence

1. `PRD.md` defines **what must be true of the product**. The safety boundary and V1 exclusions here override everything below.
2. `APP-FLOW.md` defines **observable behavior**.
3. `TRD.md` defines **how it is implemented**.
4. `NEUROONE-MVP-SCOPE.md` is the **current decision layer**. Where it narrows or sequences work within the above (e.g. mocked AI providers, roadmap order), it governs the present phase. It cannot widen scope past PRD §7 and does not claim to.

Do not invent implementation requirements inside the product layer, and do not invent product requirements inside the technical layer.

### 3.2 Conflict handling

If documents appear to conflict:

1. Do not silently choose one.
2. Name the exact conflict, with document and section.
3. Explain its architectural or product impact.
4. Return to **PLAN mode**.
5. Recommend a resolution.
6. Do not implement the disputed behavior until the conflict is resolved or an explicit assumption is accepted and recorded.

---

## 4. Operating Modes

Four explicit modes:

```text
PLAN     DEBUG     BUILD     TEST
```

Every substantial response begins with the active mode:

```text
MODE: PLAN
```

The active mode controls what the agent is allowed to do. Do not perform BUILD actions while in PLAN, or architectural redesign while in DEBUG.

### 4.1 Default rule — plan before build

For any meaningful feature, architectural change, AI/RAG change, schema change, security change, workflow change, or cross-module refactor:

```text
UNDERSTAND → PLAN → REVIEW DECISION → BUILD → TEST → DOCUMENT RESULT
```

Do not skip to BUILD because an implementation looks obvious.

**Exempt from the full cycle** (proceed directly, still report what changed): typo and comment fixes, formatting, adding a test for existing behavior, dependency-free renames confined to one file, and changes explicitly pre-approved in a prior plan.

---

## 5. PLAN Mode

### Goal

Determine **what should be done next and how it should be implemented, before code changes begin**. PLAN is the primary reasoning mode for this project; the heavy architectural thinking happens here.

### Responsibilities

1. Read the relevant project documentation.
2. Inspect the current implementation when repository access is available (§16).
3. Establish the current state — not the assumed state.
4. Understand the requested outcome.
5. Ask high-value questions where the answer materially changes the design.
6. Identify assumptions explicitly.
7. Identify architectural constraints and dependencies.
8. Consider multiple approaches when the choice is meaningful.
9. Compare tradeoffs against stated criteria.
10. Recommend one approach.
11. Break the work into ordered, implementation-ready tasks.
12. Define acceptance criteria and the testing strategy *before* implementation.
13. Identify documentation that must change.
14. Identify risks, failure modes, security implications, and clinical-safety implications.
15. State what is **out of scope**.
16. Produce a build-ready plan.

### Questions

Ask when the answer could materially change product behavior, architecture, API contracts, database schema, AI/RAG behavior, frontend/backend ownership, security, authorization, deployment, testing, backwards compatibility, or scope.

Do **not** ask what is already answered by `PRD.md`, `APP-FLOW.md`, `TRD.md`, `NEUROONE-MVP-SCOPE.md`, the repository, existing tests, existing configuration, or a previously recorded decision.

Prefer a few high-impact questions over a questionnaire. If instructed to proceed on assumptions, document them and continue.

### PLAN must not

Implement production code, perform broad refactors, modify schemas, add dependencies, create migrations, silently make product decisions, or silently expand scope.

Pseudocode, interfaces, schemas, file trees, sequence diagrams, and example contracts are allowed where they clarify the plan.

### Required PLAN output

```text
1.  Objective
2.  Current State
3.  Relevant Requirements
4.  Questions / Resolved Decisions
5.  Assumptions
6.  Scope
7.  Out of Scope
8.  Architecture Impact
9.  Design Options
10. Recommended Design
11. Data / Schema Impact
12. API / Contract Impact
13. AI / RAG Impact
14. Security / Privacy Impact
15. Clinical Safety Impact
16. Failure / Recovery Behavior
17. Implementation Tasks
18. Task Dependencies
19. Testing Strategy
20. Acceptance Criteria
21. Documentation Updates
22. Risks / Open Issues
23. Build Readiness
```

Sections that genuinely do not apply are marked `N/A` with one line of reasoning — never deleted.

### Completion gate

A plan is complete only if another capable engineer or agent could implement it without rediscovering the architecture.

End PLAN with exactly one of:

```text
BUILD READY
NOT BUILD READY
```

If not ready, state precisely what remains unresolved.

Do not enter BUILD automatically unless explicitly instructed to continue, or the approved plan already authorizes implementation.

---

## 6. BUILD Mode

### Goal

Implement an approved plan faithfully and incrementally. BUILD is execution, not architectural improvisation. If a major unresolved design decision surfaces mid-implementation, stop and return to PLAN.

### Responsibilities

1. Read the approved plan.
2. Confirm task dependencies.
3. Implement in dependency order.
4. Keep changes scoped to the task.
5. Preserve layer boundaries (§7).
6. Preserve typed contracts.
7. Add migrations for every schema change.
8. Add tests alongside implementation, not after.
9. Preserve centralized error handling.
10. Preserve server-side authorization.
11. Preserve clinical data on AI/RAG failure.
12. Update required documentation.
13. Report any deviation from the plan, with reasoning.

---

## 7. Architecture Rules

```text
Client → API → Service → Repository → PostgreSQL
```

### Backend layout (TRD §3)

```text
backend/
├── app/
│   ├── api/
│   │   └── dependencies.py
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── ai/
│   ├── reports/
│   └── utils/
├── main.py
├── migrations/
└── tests/
```

### Stack

Python · FastAPI · Pydantic 2 · SQLAlchemy · Alembic · PostgreSQL · JWT auth · secure password hashing · RAG + LLM · PDF generation.

Do not introduce a dependency that duplicates something already in the stack.

### API layer

**Allowed:** routing, request validation, authentication dependencies, serialization, HTTP error translation.

**Not allowed:** domain or business logic, database orchestration belonging to services, embedded AI orchestration.

### Service layer

Business rules, use-case orchestration, authorization decisions, repository coordination, AI coordination.

### Repository layer

Persistence and database queries only. No HTTP behavior, no business rules.

*Open convention:* transaction-boundary ownership (repository vs. service) is not assigned by `TRD.md`. Pick it once, in an ADR, before the first multi-repository use case — do not settle it implicitly per-endpoint.

### Models

SQLAlchemy entities. Initial domain entities: **User, Patient, Clinical Case / Visit, Diagnosis, Evidence, Report**.

### Schemas

Typed Pydantic 2 contracts for request/response models and all AI structured output.

### Clinical input contract (FR-03)

Structured clinical input captures **neurological symptoms, duration, severity, observations, relevant history**, and additional case information. Validate these at the schema boundary; do not collapse them into a free-text blob, since the AI pipeline's normalization and cross-visit trend comparison (§8.3) depend on their structure.

### Report contract (FR-07)

A generated report contains **patient/case information, clinical inputs, differential diagnosis, reasoning, evidence, citations, and an appropriate disclaimer**. A report missing citations or the disclaimer is incomplete, not merely unpolished.

### Database

PostgreSQL, UUID identifiers, timestamps, foreign keys, Alembic migrations, referential integrity, appropriate soft-delete semantics.

### Authentication

```text
Credentials → Validate → Verify Password → Issue JWT → Protected Request → Validate JWT
```

Authentication dependencies must expose **overridable service providers** rather than constructing services directly inside request dependencies — this keeps the auth path testable.

### Authorization

Roles: `ADMIN`, `CLINICIAN`. (`RECEPTIONIST` is deferred and is not yet defined in PRD §4; do not implement it.)

Enforce access control **server-side** at the API/service boundary. Never rely on frontend-only access control.

---

## 8. AI / RAG Rules

### Pipeline (TRD §8, APP-FLOW §5)

```text
Clinical Case
  ↓ Normalize Input
  ↓ Build Clinical Context
  ↓ Retrieve Literature
  ↓ Rank Evidence
  ↓ Construct AI Context
  ↓ LLM Reasoning
  ↓ Validate Structured Output
  ↓ Persist / Return Analysis
```

### 8.1 AI-01 — contract-real, provider-mocked

Per `NEUROONE-MVP-SCOPE.md`, the `AI-01` phase is deliberately split. (`AI-01` is fifth in the roadmap — see §15. This section governs it when it is reached; it is not authorization to start it early.)

**Real and enforced now:**

- the AI orchestrator interface,
- the structured Diagnosis / Evidence output contract,
- validation of that contract,
- everything downstream — ranking, citation attachment, clinician review, PDF assembly.

**Mocked now, swapped later (`AI-02`):**

- the retrieval corpus,
- the LLM call.

Mock providers return **schema-valid deterministic results** and sit **behind the same interface** the real providers will use. Fixing the contract first is the entire point: `AI-02` must be a provider swap, not a pipeline rewrite.

Two obligations follow:

- Mock data must simulate **at least one multi-visit trend**, so an `early_watch` flag has something real to point at.
- Mock-sourced output must stay clearly labeled internally as *"pipeline complete, evidence retrieval simulated."* Never let it be described as clinically validated. This is a credibility risk, not just a code comment.

### 8.2 AI output contract

AI output is never accepted as unvalidated free-form text.

**FR-04 constraint on every diagnosis output:** the result is a *ranked list of possible conditions with supporting findings, uncertainty, and reasoning*. **Never represent the output as a definitive diagnosis** — not in the schema, not in API field naming, not in UI copy, not in the PDF. Confidence is always expressed as likelihood, never as certainty.

A differential-diagnosis result preserves:

```text
Diagnosis
├── name
├── category                 # differential_diagnosis | early_watch
├── likelihood / confidence
├── supporting_findings
├── contradicting_findings
├── explanation
├── trend_basis[]            # prior visits/findings driving an early_watch flag
└── evidence[]
    ├── source
    ├── citation
    └── relevant_passage
```

`trend_basis` traces to the **patient's own visit history** and is distinct from `evidence[]`, which traces to **external literature**. Do not conflate them.

### 8.3 Early-detection design

The early-detection capability for this MVP is **trend-aware reasoning over clinician-entered data across a patient's visit history, plus confidence-tiered output** — not imaging, not biomarkers.

Consequences:

- Clinical context building uses the patient's **prior visits/cases**, not only the currently open case.
- The case/visit domain must support **cross-visit comparison**.
- This implements FR-04's existing "uncertainty" requirement; it is not a new functional requirement.

Imaging analysis is excluded by PRD §7; biomarker analysis is excluded for the MVP by `NEUROONE-MVP-SCOPE.md`, consistent with that PRD exclusion. Both are later, separate phases.

### 8.4 RAG requirements

1. Accept clinical context.
2. Retrieve relevant medical literature.
3. Rank and select evidence.
4. Preserve source metadata.
5. Supply evidence to the model.
6. Attach citations to recommendations.

Trusted medical sources are prioritized. Every major recommendation stays traceable:

```text
patient finding + reasoning factor + supporting evidence + citation
```

### 8.5 AI failure safety

```text
AI / retrieval failure
  → preserve clinical data
  → return a controlled error
  → allow retry / recovery
```

An AI or RAG failure must **never** corrupt or partially overwrite a patient or clinical case record.

---

## 9. DEBUG Mode

### Goal

Find the actual cause of a defect, resolve it with the smallest safe change, and prevent regression. DEBUG is evidence-driven. Do not begin by rewriting the subsystem.

### Workflow

```text
Observe → Reproduce → Localize → Form Hypothesis → Collect Evidence
  → Identify Root Cause → Design Minimal Fix → Implement Fix
  → Regression Test → Document
```

### Responsibilities

1. Restate the observed failure.
2. Identify expected behavior from the docs or tests.
3. Reproduce when possible.
4. Capture relevant logs, errors, and test failures.
5. Narrow to the failing layer.
6. Separate symptom from root cause.
7. List plausible hypotheses.
8. Test hypotheses rather than guessing.
9. Identify the root cause.
10. Apply the smallest correct fix.
11. Avoid unrelated cleanup.
12. Add or update a regression test.
13. Re-run impacted tests.
14. Check related failure paths.
15. Document root cause and fix.

### Layer-oriented debugging

```text
Client → API → Service → Repository → Database
```

For AI features:

```text
Case Data → Normalization → Clinical Context → Retrieval → Evidence Ranking
  → AI Context → LLM → Structured Validation → Persistence / Response
```

Identify the layer where the contract **first** becomes incorrect — not the layer where the error surfaced.

### Prohibited

- Patching around a failing contract without understanding why it failed.
- Hiding or swallowing exceptions.
- Weakening validation to make a test pass.
- Removing authorization checks to bypass a bug.
- Suppressing AI/RAG failures.
- Corrupting or overwriting clinical records during recovery.
- Turning a bug fix into an architectural rewrite.

If the fix requires significant architecture change, stop and return to **PLAN**.

### Required DEBUG output

```text
MODE: DEBUG

Observed Failure:
Expected Behavior:
Reproduction:
Evidence:
Root Cause:
Affected Components:
Fix:
Files Changed:
Regression Test:
Validation Performed:
Remaining Risk:
```

---

## 10. TEST Mode

### Goal

Determine whether the implementation is **logically correct, contract-correct, safe, and regression-free**. A passing happy path is not sufficient evidence of correctness.

### Categories

**Unit** — services, repositories, validation, AI orchestration, utilities.

**Integration** — database behavior, authentication, authorization, API endpoints, patient workflow, case workflow.

**AI** — structured-output validation, retrieval relevance, citation presence, traceability, malformed model output, missing evidence, AI failure handling, RAG failure handling.

**End-to-end** — the MVP acceptance journey:

```text
Login → Patient → Case → Symptoms → AI Analysis
  → Differential Diagnosis + Evidence → Clinician Review → PDF Report
```

### Responsibilities

1. Identify the behavior being verified.
2. Map it to a requirement or implementation contract.
3. Run the narrowest relevant tests first, broader regression afterward.
4. Test success paths, invalid input, authorization boundaries, failure/recovery, and data integrity.
5. Test AI structured-output validation and citation traceability.
6. Report failures without disguising them.
7. Distinguish a product bug from a test bug.
8. Never change production behavior merely to satisfy an incorrect test.

### Required TEST output

```text
MODE: TEST

Scope:
Requirements Verified:
Tests Run:
Passed:
Failed:
Regression Status:
Logic Assessment:
Security Assessment:
Clinical Safety Assessment:
Known Gaps:
Final Verdict:
```

Final verdict is exactly one of:

```text
PASS
PASS WITH KNOWN LIMITATIONS
FAIL
BLOCKED
```

---

## 11. Mode Transitions

```text
                    ┌─────────────┐
                    │    PLAN     │
                    └──────┬──────┘
                           │ approved
                           ▼
                    ┌─────────────┐
             ┌─────▶│    BUILD    │
             │      └──────┬──────┘
             │             │ implemented
             │             ▼
             │      ┌─────────────┐
             │      │    TEST     │
             │      └──────┬──────┘
             │             │ failure
             │             ▼
             │      ┌─────────────┐
             └──────│    DEBUG    │
                    └──────┬──────┘
                           │ fix complete
                           ▼
                         TEST
```

Return to PLAN when:

- scope materially changes,
- the architecture must change,
- a new dependency is required,
- a data model must be redesigned,
- a public API contract must change,
- the AI/RAG contract changes,
- security assumptions change,
- requested behavior conflicts with a source-of-truth document.

---

## 12. Security and Privacy Rules

Patient data is sensitive. At minimum:

- never store plaintext passwords,
- never put sensitive patient data in logs,
- authenticate every protected resource,
- authorize server-side,
- validate all input at the schema boundary,
- preserve transactional integrity,
- never leak internal exceptions or stack traces to clients,
- minimize unnecessary exposure of patient data,
- never bypass validation to simplify development,
- never commit secrets, `.env` files, or credentials.

Security-sensitive changes require explicit testing.

### Demo data — flagged assumption, not yet confirmed

`NEUROONE-MVP-SCOPE.md` records this as an **assumption awaiting confirmation**, deliberately not decided silently: the demo environment uses synthetic/seed patient and case data rather than real PHI, on the grounds that the system has not been through a security review.

Build to that assumption. Do not restate it as a settled policy, and do not treat it as resolved until it is confirmed. Any move toward real patient data is a PLAN-mode decision requiring explicit sign-off, and would carry security-review implications well beyond the code.

---

## 13. Error Handling Rules

Use centralized error translation. Domain and application exceptions remain **independent of HTTP concerns**.

Categories: Validation · Authentication · Authorization · Not Found · Conflict · Database · AI · External Service · Internal Server Error.

```text
DB Operation → Failure → Rollback → Centralized Error Handler → Controlled Response
User Input   → Schema Validation → Invalid → 400/422 → Correct Input
```

---

## 14. Task Planning Format

Plans decompose into independently understandable tasks, ordered so foundational contracts land before features depending on them.

Task IDs follow the roadmap prefixes: `SEC-`, `AUTH-`, `PAT-`, `CASE-`, `AI-`, `REPORT-`.

```text
## TASK <ID> — <title>

### Goal
What this task achieves.

### Why
Requirement or architectural reason.

### Dependencies
What must exist first.

### Files / Components
Likely areas affected.

### Implementation
Concrete steps.

### Contracts
API / schema / database / AI contracts affected.

### Failure Cases
Expected error behavior.

### Tests
Tests required for completion.

### Documentation
Docs to update.

### Definition of Done
Objective completion criteria.
```

### Task quality

Not acceptable:

```text
Implement AI. Add database. Write tests.
```

Acceptable:

```text
TASK AI-03 — Structured differential-diagnosis response schema

Create the structured differential-diagnosis response schema in
backend/app/schemas/analysis.py.

Requirements:
- diagnosis name
- category (differential_diagnosis | early_watch)
- likelihood/confidence
- supporting findings
- contradicting findings
- explanation
- trend_basis references
- evidence references

Dependencies:
- clinical context schema
- evidence schema

Tests:
- valid output accepted
- missing evidence rejected where required
- malformed confidence rejected
- early_watch without trend_basis rejected

Definition of Done:
- schema is typed (Pydantic 2)
- AI orchestrator uses the schema
- validation failure routes through the centralized error path
- unit tests pass
```

---

## 15. Roadmap and Sequencing

Current locked ordering (`NEUROONE-MVP-SCOPE.md`):

```text
SEC-01        housekeeping (.env untracking, SQL echo, /health exception exposure)
AUTH-01       CLINICIAN rename, real auth endpoints, soft-delete fix, DB rollback/error handling
PAT-01        authorized patient CRUD vertical slice
CASE-01       clinical case / symptom domain (currently a broken stub; must support cross-visit history)
AI-01 (mock)  structured AI contract + mocked retriever/LLM + evidence/citation shape
REPORT-01     PDF assembly — full acceptance journey becomes demoable end-to-end
AI-02         real LLM + RAG swap-in behind the AI-01 interface (post-demo)
```

This ordering supersedes the generic sequence in `TRD.md` §13 for the current phase. Do not start a downstream item while an upstream contract it depends on is unimplemented.

### Demo-ready definition

The full PRD §8 journey works end-to-end through the actual API/UI with synthetic data: a clinician logs in, creates a patient and case, enters symptoms, triggers analysis, sees a ranked differential diagnosis with schema-correct mock-sourced evidence and citations — including at least one `early_watch` flag traced to a simulated prior-visit trend — reviews it, and downloads a PDF report. **No real LLM/RAG call is required to hit this milestone.**

---

## 16. Repository Inspection Rules

When repository access is available, never plan from documentation alone if the task depends on current implementation state. Documentation describes intent; the repository describes reality, and on this project the two have already diverged (the Visit model is a known stub).

Inspect, as relevant: project tree, configuration, dependencies, schemas, models, services, repositories, API routes, AI orchestration, migrations, tests, existing documentation.

Before proposing a new component, verify an equivalent does not already exist.
Before proposing a dependency, verify the repository does not already provide the capability.
Before asserting that something is broken, missing, or complete, verify it by reading the code.

State clearly which claims come from documentation and which from inspected code.

---

## 17. Decision Records

For meaningful architectural decisions, create or update a short decision record **before** implementation.

Location: `docs/decisions/` · Format: `ADR-XXX-title.md`

```text
Title
Status
Context
Problem
Constraints
Options Considered
Decision
Why
Consequences
Risks
Alternatives Rejected
Testing Impact
Migration / Rollback Impact
```

Do not write an ADR for trivial implementation details. Do write one for: schema redesign, contract changes, auth model changes, AI/RAG interface changes, new dependencies, and anything that revises a source-of-truth document.

---

## 18. Definition of Done

A feature is not complete because code exists. A task is complete only when every applicable item holds:

- [ ] requirement is implemented,
- [ ] architecture boundaries preserved,
- [ ] schemas and contracts typed,
- [ ] errors controlled through the centralized path,
- [ ] authorization enforced server-side,
- [ ] database integrity preserved,
- [ ] migrations exist where required,
- [ ] tests exist and pass,
- [ ] AI output validated against the contract,
- [ ] evidence metadata preserved,
- [ ] citations traceable,
- [ ] `trend_basis` traceable for any `early_watch` output,
- [ ] no output framed as a definitive diagnosis; report disclaimer present,
- [ ] clinical data survives AI/RAG failure,
- [ ] no secrets committed,
- [ ] documentation updated,
- [ ] no unapproved scope expansion.

---

## 19. V1 Scope Guard

**Hard exclusions (PRD §7)** — out of V1 unless the product documents are deliberately revised:

- MRI / image analysis,
- uploaded diagnostic-report analysis,
- autonomous diagnosis,
- automated treatment decisions.

**Deferred, not excluded** — out of the MVP but with a defined return path:

- the `RECEPTIONIST` role (not in the MVP, and not yet defined in PRD §4; if it returns, PRD §4 must define it first),
- biomarker analysis (§8.3),
- real LLM + RAG providers (`AI-02`, §15).

Do not introduce any of these quietly while implementing adjacent features. If asked for one, switch to PLAN mode and treat the request as a scope/version decision, not a feature request.

---

## 20. Reasoning and Communication

Think deeply before architectural decisions; communicate the result as **clear engineering rationale**, not an unfiltered reasoning transcript.

**Prefer:** assumptions, evidence, tradeoffs, decision criteria, the selected option, risks, consequences.

**Avoid:** "this seems better," unexplained architectural choices, implementation before requirements are understood, and pretending certainty that does not exist.

When uncertain, say what is uncertain and how it affects the decision. Report bad news — failing tests, a broken stub, a contract that does not hold — plainly and early. An agent that hides a problem to appear productive has caused a second problem.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
