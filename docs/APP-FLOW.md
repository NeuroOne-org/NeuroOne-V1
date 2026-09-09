# NeuroONE — Application Flow

## Document Contract
- **Purpose:** Behavioral source of truth.
- **Audience:** AI coding agents, frontend/backend engineers, QA.
- **Rule:** Describe observable application behavior and system transitions.
- **Status:** MVP / V1.

## 1. Primary Flow
```text
LOGIN
  ↓
DASHBOARD
  ↓
PATIENT
  ↓
CASE
  ↓
SYMPTOMS / CLINICAL INPUT
  ↓
AI ANALYSIS
  ↓
DIFFERENTIAL DIAGNOSIS
  ↓
EVIDENCE + CITATIONS
  ↓
CLINICIAN REVIEW
  ↓
REPORT
```

## 2. Authentication
```text
Login
 ↓
Submit credentials
 ↓
Validate credentials
 ├─ invalid → 401
 └─ valid → JWT
 ↓
Authenticated session
 ↓
Protected resources
```

## 3. Patient Flow
```text
Dashboard → Patients → Create Patient → Validate → Save → Patient Profile
```
Existing patient:
```text
Patients → Select Patient → Profile → Cases / History
```

## 4. Case Flow
```text
Patient Profile
 ↓
Create Case
 ↓
Enter clinical information
 ↓
Enter neurological symptoms
 ↓
Validate
 ↓
Save case
 ↓
Run AI analysis
```

## 5. AI Flow
```text
Clinical Case
 ↓
Normalize Input
 ↓
Build Clinical Context
 ↓
Retrieve Literature
 ↓
Rank Evidence
 ↓
Construct AI Context
 ↓
LLM Reasoning
 ↓
Validate Structured Output
 ↓
Store/Return Analysis
```

## 6. Evidence Flow
```text
Clinical Context
 ↓
Retrieval
 ↓
Relevant Literature
 ↓
Evidence Ranking
 ↓
Selected Evidence
 ↓
AI Context
 ↓
Recommendation
 ↓
Citation
```
Every major recommendation should remain traceable to supporting evidence.

## 7. Review Flow
```text
AI Analysis Complete
 ↓
Differential Diagnosis
 ↓
Supporting Findings
 ↓
Contradicting Findings
 ↓
Evidence + Citations
 ↓
Clinician Review
 ↓
Clinical Decision
```
The clinician remains responsible for final interpretation.

## 8. Report Flow
```text
Case
 ↓
Clinical Information
 ↓
AI Analysis
 ↓
Differential Diagnosis
 ↓
Evidence + Citations
 ↓
Report Builder
 ↓
PDF
```

## 9. Failure Flows
### AI/RAG failure
`Analysis Request → Failure → Preserve Clinical Data → Controlled Error → Retry/Recover`

### Database failure
`DB Operation → Failure → Rollback → Centralized Error Handler → Controlled Response`

### Invalid input
`User Input → Schema Validation → Invalid → 400/422 → Correct Input`

## 10. V1 Boundary
No MRI/image analysis, diagnostic-document analysis, autonomous diagnosis, or automated treatment decision flow exists in V1.
