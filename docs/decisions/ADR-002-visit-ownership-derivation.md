# ADR-002: Visit Ownership Derives From the Parent Patient, and the 404 Is Re-Labelled

## Status
Accepted

## Context
CASE-01 introduces the clinical case (`Visit`) and `Symptom` resources. Neither carries a `doctor_id`: a visit belongs to a patient, and the patient belongs to a clinician. Ownership therefore has to be derived one hop up, and for symptoms, two hops up.

[ADR-001](ADR-001-ownership-violation-status-code.md) established that a per-record ownership violation returns 404 rather than 403, so that a caller with no legitimate claim to a record cannot distinguish "you may not see this" from "this does not exist". Extending that guarantee to a nested resource raises two questions the patient slice never had to answer:

1. **Where does the rule live?** `PatientService._authorize_access` already implements it. A second copy inside `VisitService` would drift the moment the rule changes (for example, if a supervising-clinician role is added later).
2. **What does the 404 say?** `PatientService.get_patient` raises `EntityNotFoundError("Patient", patient_id)`, whose message embeds the patient UUID. On a flat route like `GET /visits/{visit_id}` the caller never supplied a patient id. Letting that error propagate unchanged would disclose the parent patient's UUID to a clinician with no claim to the record — an ADR-001 violation wearing a 404's clothing.

## Decision

**1. `VisitService` composes `PatientService` and delegates every authorization decision to it.**

The ownership rule lives in exactly one place. This follows the existing service-to-service pattern (`AuthService(user_service)` in `app/api/dependencies.py`). It also means soft-deleted patients are handled for free, since `get_patient` resolves through `get_or_404`, which filters `is_deleted`.

**2. A 404 is labelled with the resource the caller actually named.**

On `/visits/{visit_id}` routes, an `EntityNotFoundError` raised by the patient gate is caught and re-raised as `EntityNotFoundError("Visit", visit_id)`. All four failure modes become response-identical:

- the visit does not exist
- the visit is soft-deleted
- the parent patient is soft-deleted
- the parent patient belongs to another clinician

Symptoms mask one level deeper: a symptom on an inaccessible visit produces a **Visit**-shaped 404, never a Symptom-shaped one, because the caller must not learn that the visit id was real.

**3. On patient-scoped routes, the patient label is kept.**

`/patients/{patient_id}/visits` and `/patients/{patient_id}/visits/history` take the patient id from the path. The caller already named it, so `EntityNotFoundError("Patient", patient_id)` propagates unmasked — that is the honest and correct label there. Masking is about not disclosing identifiers the caller did not supply, not about hiding labels for their own sake.

**4. A symptom is verified to belong to the visit in its path.**

`_load_authorized_symptom` asserts `symptom.visit_id == visit.id`. Without this, nesting symptoms under a visit would allow `/visits/{A}/symptoms/{belongs-to-B}` to silently edit a symptom on a different case. A mismatched pair reads as a missing symptom.

## Consequences

- Every read path for visits and symptoms passes through `_load_authorized_visit`. New endpoints on these resources must use it rather than calling the repository directly.
- Error *messages* for masked 404s deliberately carry less information than the underlying cause. Operators debugging a genuine 404 will not see "patient not found" in the response; the distinction is only visible in the exception chain (`raise ... from exc`), not on the wire.
- DIAG-01 inherits this pattern directly: diagnoses hang off visits, so they need the same two-level derivation and masking. AI-01 calls `VisitService.get_patient_history()` in-process, which applies the patient gate itself.
- Patient soft-delete does not cascade to visits (`PatientService.delete_patient` is PAT-01 surface and was left unchanged). This is not an access-control gap: because every visit read resolves ownership through `get_patient`, a soft-deleted patient's visits become immediately unreachable. Their rows simply keep `is_deleted = False`. Cleaning that up is a follow-up.

## Alternatives considered

**Give `Visit` its own `doctor_id`.** Denormalizing ownership onto every child resource would make each check a single comparison and avoid the extra lookup. Rejected: it creates two sources of truth that must be kept in sync on patient reassignment, and the same problem recurs for every future child (diagnoses, reports).

**Return 403 for a visit whose patient belongs to another clinician.** Rejected for the reasons already settled in ADR-001; nesting does not change the argument, it only widens the surface the argument applies to.

**Duplicate `_authorize_access` into `VisitService` over `PatientRepository`.** Marginally fewer calls, but two copies of a security rule. Rejected.
