# NeuroONE — Product Definition & Requirements

## Document Contract
- **Purpose:** Product source of truth.
- **Audience:** AI coding agents and technical planners.
- **Rule:** Define what NeuroONE must do, not how it is implemented.
- **Status:** MVP / V1.

## 1. Product
NeuroONE is a clinical decision-support platform for neurological case evaluation. It combines structured patient/case information with trusted medical literature and AI reasoning to produce an explainable differential diagnosis.

**Safety boundary:** NeuroONE assists clinicians. It must not present itself as an autonomous diagnostic or treatment system.

## 2. Problem
Neurological evaluation requires correlation of patient history, symptoms, observations, differential possibilities, and medical literature. NeuroONE reduces information-retrieval and reasoning overhead while keeping clinical responsibility with the clinician.

## 3. Product Goal
A clinician must be able to:
1. Authenticate.
2. Create or select a patient.
3. Create a clinical case.
4. Record neurological symptoms and relevant clinical information.
5. Request AI-assisted differential diagnosis.
6. Review reasoning and evidence with citations.
7. Generate a downloadable clinical report.

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

### FR-05 Literature Retrieval
Retrieve relevant evidence from trusted medical literature and preserve source metadata.

### FR-06 Explainability
Recommendations must expose relevant patient findings, reasoning factors, supporting evidence, and citations.

### FR-07 Clinical Report
Generate a report containing patient/case information, clinical inputs, differential diagnosis, reasoning, evidence, citations, and an appropriate disclaimer.

## 6. Non-Functional Requirements
- **Security:** No plaintext passwords; authenticated and authorized access; controlled exposure of patient data; avoid sensitive data in logs.
- **Reliability:** Consistent errors; transactional data integrity; AI/RAG failure must not corrupt clinical records.
- **Maintainability:** Layered architecture, typed schemas, centralized exceptions, migrations, and automated tests.
- **Traceability:** AI recommendations must be traceable to input findings and retrieved evidence.

## 7. V1 Exclusions
- MRI/image analysis
- Uploaded diagnostic-report analysis
- Autonomous diagnosis
- Automated treatment decisions

## 8. MVP Acceptance Journey
`Login → Patient → Case → Symptoms → AI Analysis → Differential Diagnosis + Evidence → Clinician Review → PDF Report`
