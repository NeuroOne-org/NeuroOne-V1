# NeuroONE — Application Flow

## Document Contract
- **Purpose:** Behavioral source of truth.
- **Audience:** AI coding agents, frontend/backend engineers, QA.
- **Rule:** Describe observable application behavior and system transitions.
- **Status:** MVP / V1. Revised for [ADR-006](decisions/ADR-006-mri-primary-with-symptoms-as-context.md): an MRI scan is a primary visit input, the dashboard is a triage queue, and sign-off gates the report.

A **visit** is the clinical encounter at a point in time (earlier drafts called it a "case"): chief complaint, history, structured symptoms and at most one MRI scan.

## 1. Primary Flow
```text
LOGIN
  ↓
TRIAGE DASHBOARD
  ↓
PATIENT
  ↓
VISIT (SCAN + SYMPTOMS / CLINICAL INPUT)
  ↓
AI ANALYSIS
  ↓
RANKED DIFFERENTIAL (STAGE ESTIMATE PINNED FIRST WHEN SCANNED)
  ↓
EVIDENCE + CITATIONS
  ↓
CLINICIAN SIGN-OFF
  ↓
PDF REPORT
```

## 2. Authentication
```text
Login
 ↓
Submit credentials
 ↓
Validate credentials
 ├─ invalid → 401
 └─ valid → OTP required (default)
              ↓
            Submit emailed/console code
              ├─ invalid / expired → 401
              └─ valid → JWT in HttpOnly cookie
 ↓
Authenticated session
 ↓
Protected resources (writes also need the CSRF header)
```
Accounts are provisioned by an administrator; there is no self-registration.

## 3. Dashboard and Patient Flow
```text
Dashboard → Triage queue
  ordered: open early-watch flags → worsening trends → analyses awaiting sign-off
```
New patient:
```text
Patients → Create Patient (demographics only) → Validate → Save → offer first visit
```
Existing patient:
```text
Patients → Select Patient → Profile → Visits / History → New Visit (follow-up)
```

## 4. Visit Flow
```text
Patient Profile
 ↓
Create Visit
 ↓
Enter chief complaint, history and neurological symptoms
 ↓
Attach MRI scan (optional; NIfTI, DICOM, PNG or JPEG)
 ├─ header parsed → dimensions stored, file retained outside the database
 └─ unreadable / oversized / second scan on this visit → 4xx, nothing stored
 ↓
Validate
 ↓
Save visit
 ↓
Run AI analysis
```
One scan belongs to one visit. A follow-up scan belongs to a new visit, which is what makes scans comparable across visits.

## 5. AI Flow
```text
Visit (+ prior visits strictly before it)
 ↓
Normalize Input
 ↓
Build Clinical Context (symptom trends across visits)
 ↓
Stage Scan (only if the visit has one; prior scanned visits feed a stage trend)
 ↓
Retrieve Literature (the stage's citations on their own budget)
 ↓
Rank Evidence
 ↓
Construct AI Context
 ↓
LLM Reasoning
 ↓
Validate Structured Output (stage pinned first, every candidate cited)
 ↓
Store Analysis + context snapshot + provenance note
```
Each provider (retrieval, reasoning, staging) is mock or live by configuration, and every analysis states which were simulated.

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
Ranked Differential (likelihood bands, never certainty)
 ↓
Supporting Findings
 ↓
Contradicting Findings
 ↓
Evidence + Citations, and own-history trend references
 ↓
Clinician Sign-off (clinician role only; records who and when)
 ↓
Clinical Decision
```
The clinician remains responsible for final interpretation. Sign-off currently accepts the analysis as generated; amending it before sign-off (ADR-006 decision 6) is not implemented.

## 8. Report Flow
```text
Analysis
 ├─ not signed off → 409, no report
 └─ signed off
      ↓
    Snapshot: patient, the visit as the analysis saw it, differential,
              evidence, citations, provenance, reviewer and sign-off time
      ↓
    Render PDF (before anything is stored)
      ↓
    Store snapshot; downloads re-render from it
```

## 9. Failure Flows
### AI/RAG failure
`Analysis Request → Failure → Preserve Clinical Data → Controlled Error → Retry/Recover`

A scanned visit whose staging fails (`staging_error`) or whose analysis has no cited stage candidate (`ai_stage_missing`) fails the same way: no symptoms-only result is returned in its place.

### Database failure
`DB Operation → Failure → Rollback → Centralized Error Handler → Controlled Response`

A scan file whose database row fails to save is deleted.

### Invalid input
`User Input → Schema Validation → Invalid → 400/422 → Correct Input`

## 10. V1 Boundary
MRI scan intake and staging are in scope (ADR-006). The stage estimate is a ranked candidate with likelihood and citations, never a standalone verdict, and the staging model is simulated by default.

No diagnostic-document analysis, autonomous diagnosis, or automated treatment decision flow exists in V1.
