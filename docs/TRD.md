# NeuroONE — Technical Requirements & Design

## Document Contract
- **Purpose:** Technical source of truth.
- **Audience:** AI coding agents and engineers.
- **Rule:** Define implementation architecture, contracts, and technical constraints.
- **Status:** MVP / V1.

## 1. Architecture
```text
Client
  ↓
API Layer
  ↓
Service Layer
  ↓
Repository Layer
  ↓
PostgreSQL

Clinical Case
  ↓
AI Orchestrator
  ↓
Retriever → Medical Knowledge Base
  ↓
LLM Reasoning
  ↓
Structured Result
  ↓
Clinical Report
```

## 2. Stack
- Python
- FastAPI
- Pydantic 2
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT authentication
- Secure password hashing
- RAG + LLM
- PDF generation

## 3. Backend Layout
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

## 4. Layer Rules
### API
HTTP routing, validation, authentication dependencies, serialization, HTTP error translation. No business logic.

### Services
Business rules, use-case orchestration, authorization decisions, repository/AI coordination.

### Repositories
Persistence and database queries only. No HTTP logic.

### Models
SQLAlchemy entities. Initial domain entities: User, Patient, Clinical Case/Visit, Diagnosis, Evidence, Report.

### Schemas
Pydantic request/response and AI contracts.

## 5. Database
Use PostgreSQL with UUID identifiers, timestamps, foreign keys, migrations, and appropriate soft-delete semantics. Preserve referential integrity.

## 6. Authentication
```text
Credentials → Validate → Verify Password → Issue JWT → Protected Request → Validate JWT
```
Authentication dependencies should expose overridable service providers rather than constructing services directly inside request dependencies.

## 7. Authorization
Initial roles:
- `ADMIN`
- `CLINICIAN`

Enforce access control server-side at API/service boundaries.

## 8. AI Pipeline
```text
Case Data
 ↓
Normalize
 ↓
Build Clinical Context
 ↓
Retrieve Evidence
 ↓
Rank Evidence
 ↓
Build AI Context
 ↓
LLM
 ↓
Structured Output
 ↓
Validate
 ↓
Persist/Return
```

AI output must use a structured contract rather than unvalidated free-form text.

## 9. AI Output Contract
Conceptual structure:
```text
Diagnosis
├── name
├── category                 # differential_diagnosis | early_watch
├── likelihood/confidence
├── supporting_findings
├── contradicting_findings
├── explanation
├── trend_basis[]            # prior visits/findings driving an early_watch flag
└── evidence[]
    ├── source
    ├── citation
    └── relevant_passage
```

`trend_basis` traces to the patient's own visit history; `evidence[]` traces to
external literature. They are distinct and must not be conflated.

`category` and `trend_basis[]` were added by the early-detection design decision
in `NEUROONE-MVP-SCOPE.md` and are implemented by `AI-01`. See
`decisions/ADR-003-ai-analysis-contract-and-provider-seam.md`.

## 10. RAG Rules
1. Accept clinical context.
2. Retrieve relevant literature.
3. Rank/select evidence.
4. Preserve source metadata.
5. Supply evidence to the model.
6. Attach citations to recommendations.

Trusted medical sources should be prioritized.

## 11. Error Handling
Centralize translation of domain/application errors into HTTP responses:
- Validation
- Authentication
- Authorization
- Not Found
- Conflict
- Database
- AI
- External Service
- Internal Server Error

Domain exceptions must remain independent of HTTP concerns.

## 12. Testing
- **Unit:** services, repositories, validation, AI orchestration, utilities.
- **Integration:** database, authentication, API endpoints, patient workflow.
- **AI:** structured output validation, retrieval relevance, citation presence, failure handling.

## 13. Implementation Sequence
1. Authentication APIs
2. Patient APIs
3. Clinical case/visit domain
4. Diagnosis domain
5. AI orchestration
6. RAG/evidence pipeline
7. Citation system
8. PDF reporting
9. End-to-end tests
10. Production hardening
