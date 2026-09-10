# ADR-001: Ownership Violations Return 404, Not 403

## Status
Accepted

## Context
PAT-01 introduces server-side ownership enforcement for the Patient resource (TRD §4/§7). A `CLINICIAN` may only access patients where `patient.doctor_id == current_user.id`. An `ADMIN` is unrestricted. Prior to PAT-01, no ownership enforcement existed at all — any authenticated user could read, update, or delete any patient record.

Once ownership enforcement is added, a decision is needed for what an authenticated-but-unauthorized request receives: a CLINICIAN who is authenticated correctly, but is not the owning doctor, requests `GET /patients/{id}`, `PATCH /patients/{id}`, or `DELETE /patients/{id}` for a patient they don't own.

## Problem
Two HTTP semantics are both technically correct for "you may not access this resource":
- **403 Forbidden** — "I know this resource exists; you may not have it."
- **404 Not Found** — "Nothing here (as far as you're concerned)."

Patient records sit adjacent to PHI. Which response the API gives is itself a small information disclosure: 403 confirms the record's existence to a caller who has no legitimate claim to know that.

## Constraints
- Patient data is sensitive (AGENTS.md §16); minimize unnecessary exposure.
- The codebase already uses 403-style signaling elsewhere via `require_roles(*roles)` for role-exclusion (e.g., admin-only endpoints) — a different situation from per-record ownership.
- Enumeration resistance matters more for a resource keyed by UUID that's still tied to a real patient than it might for a low-sensitivity resource.

## Options Considered

**A. 403 Forbidden**
- Pro: Explicit; consistent with existing `require_roles` failure signaling elsewhere in the codebase.
- Con: Confirms record existence to a caller with no legitimate claim to that patient — an enumeration/information-disclosure surface on a PHI-adjacent resource.

**B. 404 Not Found**
- Pro: Reveals nothing about whether the record exists; standard practice for PHI-adjacent or otherwise sensitive per-record access control (as opposed to role-level access control, where 403 is fine).
- Con: Slightly less "honest" to a legitimate-but-mistaken caller (e.g., a CLINICIAN who mistyped an ID vs. one probing another doctor's patient can't be told apart from the response alone) — mitigated by server-side logging still recording the real reason.

## Decision
**Option B — 404 Not Found.**

Ownership violations are indistinguishable, from the response body and status code, from the record simply not existing. This applies uniformly to `get`, `update`, and `delete`.

This is scoped narrowly to **per-record ownership checks**. Role-level exclusions (e.g., a CLINICIAN calling an ADMIN-only endpoint) are unaffected by this decision and continue to use 403 via `require_roles`, since there's no record-existence information to protect in that case — the caller already knows the endpoint exists.

## Why
- Patients are PHI-adjacent; the marginal cost of confirming existence to an unauthorized caller is not worth the marginal honesty benefit to a caller who mistyped an ID.
- Keeps a consistent signal for "not accessible to you" across both true-absence and ownership-violation cases, so client code doesn't need to special-case which kind of 404 it received.
- Matches the recommendation already reasoned through in the PAT-01 plan (§9/§10/§22); this ADR formalizes rather than introduces the call.

## Consequences
- `PatientService._authorize_access` raises the same `EntityNotFoundError` for "doesn't exist" and "exists but not yours" — call sites (API layer) don't need to distinguish these; both translate to HTTP 404 via the centralized error handler (TRD §11).
- Server-side logs must still capture the real reason (ownership violation vs. true absence) for audit/debugging purposes — the 404 is a caller-facing signal only, not a logging decision.
- Any future admin-facing audit UI that needs to show "this patient exists but belongs to Dr. X" must use a separate, explicitly-authorized admin query path — not the standard patient-detail endpoint's error semantics.

## Risks
- A legitimate CLINICIAN who mistypes a patient ID gets the same 404 as one probing another doctor's data — acceptable, since the caller-visible behavior should be identical in both cases by design.
- If a future feature needs to tell owners apart from strangers (e.g., "request access to this patient"), that will require a deliberate, separate endpoint — not a change to this decision.

## Alternatives Rejected
- **403 Forbidden** (Option A) — rejected for the reason above: confirms existence on a PHI-adjacent resource with no offsetting benefit for this system's users.
- **Route-level role gating instead of service-level ownership** — rejected in the underlying design decision (plan §9/§10), not re-litigated here; this ADR only concerns the status code once the service-level check fails.

## Testing Impact
- Integration tests must assert **404**, not 403, for: CLINICIAN A → CLINICIAN B's patient on `GET`, `PATCH`, `DELETE`.
- Integration tests must also assert 404 for a genuinely nonexistent patient ID, and that the two cases are response-indistinguishable (same status, same error shape).
- Role-exclusion tests (e.g., non-admin hitting an admin-only route) continue to assert 403 and are unaffected by this ADR.

## Migration / Rollback Impact
None. This is response-shape behavior in the service/API layer, not a schema or data change. Rollback (switching to 403 later) would only require changing the exception type raised in `_authorize_access` and is not expected to need a migration.
