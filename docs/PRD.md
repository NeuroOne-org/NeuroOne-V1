# NeuroONE — Product Definition & Requirements

## Document Contract
- **Purpose:** Product source of truth.
- **Audience:** AI coding agents and technical planners.
- **Rule:** Define what NeuroONE must do, not how it is implemented.
- **Status:** MVP / V1.

## 1. Product
NeuroONE is a clinical decision-support platform for neurological case evaluation. It combines an MRI scan, structured patient/case information, and trusted medical literature with AI reasoning to produce an explainable differential diagnosis.

**Safety boundary:** NeuroONE assists clinicians. It must not present itself as an autonomous diagnostic or treatment system.

## 2. Problem
Neurological evaluation requires correlation of patient history, symptoms, observations, differential possibilities, and medical literature. NeuroONE reduces information-retrieval and reasoning overhead while keeping clinical responsibility with the clinician.

## 3. Product Goal
A clinician must be able to:
1. Authenticate.
2. Create or select a patient.
3. Open a visit for that patient.
4. Attach an MRI scan and record neurological symptoms and relevant clinical information.
5. Request AI-assisted differential diagnosis.
6. Review reasoning and evidence with citations, and see how the patient has changed across visits.
7. Sign off on the analysis, accepting or amending it.
8. Generate a downloadable clinical report.

On opening the product, a clinician must also be able to see which of their patients needs
attention first — open early-detection flags, worsening trends, and analyses awaiting their
sign-off.

## 4. Users
- **Clinician:** Primary user; manages patients/cases and reviews AI-assisted analysis.
- **Administrator:** Manages users, roles, and system configuration.

## 5. MVP Functional Requirements
### FR-01 Authentication
Secure login, password hashing, JWT authentication, token validation, protected endpoints, and role-based authorization.

### FR-02 Patient Management
Create, view, update, and retrieve patient records; associate cases with patients.

### FR-03 Clinical Input
Capture structured neurological symptoms, duration, severity, observations, relevant history, and additional case information.

### FR-04 Differential Diagnosis
Generate a ranked list of possible neurological conditions with supporting findings, uncertainty, and reasoning. Never represent the output as definitive diagnosis.

A stage estimate derived from a scan (FR-08) is expressed as the highest-ranked candidate
in this list, carrying the same likelihood, findings and citations as any other candidate.
It must not be presented as a standalone verdict, and confidence is never described as
certainty — in the schema, in API field naming, in UI copy, or in the report.

### FR-05 Literature Retrieval
Retrieve relevant evidence from trusted medical literature and preserve source metadata.

### FR-06 Explainability
Recommendations must expose relevant patient findings, reasoning factors, supporting evidence, and citations.

### FR-07 Clinical Report
Generate a report containing patient/case information, clinical inputs, differential diagnosis, reasoning, evidence, citations, and an appropriate disclaimer. A report is produced only after clinician sign-off, and records who signed it and when.

### FR-08 Scan Intake and Staging
Accept an MRI scan as part of a visit, alongside that visit's symptoms and complaint, and
produce a stage estimate that feeds the ranked differential of FR-04. One scan belongs to
one visit, so scans across a patient's visits are comparable and can support the trend
reasoning behind an early-detection flag.

The scan is retained as source data — it cannot be regenerated from a result — and its
provenance is stated on every analysis derived from it, including whether the staging model
was simulated.

## 6. Non-Functional Requirements
- **Security:** No plaintext passwords; authenticated and authorized access; controlled exposure of patient data; avoid sensitive data in logs.
- **Reliability:** Consistent errors; transactional data integrity; AI/RAG failure must not corrupt clinical records.
- **Maintainability:** Layered architecture, typed schemas, centralized exceptions, migrations, and automated tests.
- **Traceability:** AI recommendations must be traceable to input findings and retrieved evidence.

## 7. V1 Exclusions
- Uploaded diagnostic-report analysis
- Autonomous diagnosis
- Automated treatment decisions

MRI/image analysis was a V1 exclusion and is now in scope as a primary input, per
[ADR-006](decisions/ADR-006-mri-primary-with-symptoms-as-context.md). Admitting it is
specific to MRI intake and staging: it is not a precedent for the three exclusions above,
which remain hard. Uploaded diagnostic-report analysis in particular stays excluded —
a scan supplied at intake is not the same thing as parsing a third party's report.

## 8. MVP Acceptance Journey
`Login → Patient → Visit (Scan + Symptoms) → AI Analysis → Ranked Differential + Evidence → Clinician Review & Sign-off → PDF Report`

The scan and the symptoms belong to the same visit and feed one analysis. Sign-off is a
gate, not a status: no report is produced until a clinician has accepted or amended the
analysis (ADR-006).
