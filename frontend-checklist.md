# NeuroOne Frontend — Redesign Checklist

Frontend rebuild from scratch. `API ready` = backend endpoint already exists for that page.

This is the **build checklist**: which screens, states and design foundations to
produce. The contract map — what each endpoint actually accepts and returns,
read from the schemas — is
[`docs/REPORT-01D-frontend-checklist.md`](docs/REPORT-01D-frontend-checklist.md).
Where the two disagree about the API, that file wins.

Reconciled against the backend on September 12, 2026. Several `API ready`
labels below were wrong in both directions and have been corrected; the notes
say which.

## Design Foundations
- [ ] Brand & visual direction (mood board, aesthetic sign-off)
- [ ] Color system (light + dark tokens)
- [ ] Typography system (type scale, font pairing)
- [ ] Spacing/grid & responsive breakpoints
- [ ] Component library (buttons, inputs, cards, modals, tables, badges)
- [ ] Iconography set
- [ ] Motion & interaction principles
- [ ] Accessibility baseline (WCAG target, contrast, focus states)

## Information Architecture & Nav
- [ ] Full sitemap (every route enumerated)
- [ ] Primary nav structure (sidebar/topbar) per role
- [ ] Role-based nav differences (CLINICIAN vs ADMIN)
- [ ] URL/routing structure & breadcrumbs

## Marketing / Landing
- [ ] Hero, value prop, clinician trust signals
- [ ] Product/feature overview sections
- [ ] Login/signup CTAs, no gated content leakage
- [ ] Footer (legal links, contact)

## Auth
- [ ] Login `API ready`
- [ ] Signup (role selection) — **not applicable.** AUTH-01 deliberately removed self-service
      registration (`POST /auth/register` is guarded by a regression test asserting it 404s).
      Accounts are admin-provisioned only, via `POST /admin/users`.
- [ ] OTP verification (resend + expiry countdown) `API ready` — `POST /auth/request-otp`
      and `POST /auth/verify-otp`. Password login does **not** force an OTP; this is an
      opt-in sign-in path and the mechanism behind password reset.
- [ ] Forgot / reset password `API ready` — `POST /auth/forgot-password` and
      `POST /auth/reset-password`. A previous edition of this file said no endpoint
      existed; that was true when written and is false now.
- [ ] Session-expired / 401 handling

## Account & Settings
- [ ] Profile / account settings page `API ready`
- [ ] Change password
- [ ] Notification preferences

## Triage Queue (the dashboard)
- [ ] Triage queue `API ready` — `GET /triage`, ranked and paginated. This **replaces**
      the dashboard; the route is deliberately not called `/dashboard`.
- [ ] Render the reason each row ranks where it does, from `has_open_early_watch`,
      `has_worsening_trend` and `awaiting_sign_off`. Server order, no client re-sort.
- [ ] Empty state for a clinician with no patients.
- [ ] **Delete, do not repoint:** the hardcoded `PATIENTS` array, the stat-tile row
      (including "Avg. confidence / Model certainty"), the `Critical`/`Stable`/
      `Monitoring`/`Reviewing` vocabulary and the scan-volume chart. None is backed by
      the API, and ADR-006 decision 7 rules out aggregate tiles on this screen.

## Patient Management
- [ ] Patient list (search, filter, pagination) `API ready`
- [ ] Patient create (intake form) `API ready`
- [ ] Patient detail (profile + visit history) `API ready`

## Clinical Input
- [ ] Visit detail (symptoms, scan, linked analysis) `API ready`
- [ ] Symptom entry/edit form `API ready`
- [ ] MRI upload `API ready` — `POST /visits/{id}/scan`, multipart, one scan per visit,
      attached to the **visit** not the patient. There is no processing-status endpoint:
      upload is synchronous and returns the stored metadata.
- [ ] Rebuild `dashboard/upload/page.tsx` rather than adapting it — it posts multipart
      to `POST /patients`, which takes JSON, and has never worked.

## Diagnosis & Explainability
- [ ] Analysis/results view per visit `API ready`
- [ ] Likelihood band per candidate `API ready` — render `likelihood_band`, not the raw
      `confidence` float as a headline. Nothing may display above 92%: `MAX_CONFIDENCE`
      is 0.92 and exists so output cannot express certainty.
- [ ] Contributing regions visualization — **no API.** Staging inputs are internal to the
      pipeline and are not on the wire. The existing region bars are backed by nothing.
      Do not build this until a contract exists for it.
- [ ] Stage estimate as the top-ranked candidate only `API ready` — never a lone badge
      beside a confidence figure (ADR-006 decision 3).
- [ ] Trend view across visits `API ready` — `GET /patients/{id}/visits/history`.
- [ ] Literature/evidence panel (citations) `API ready` — keep `evidence` (external)
      visually distinct from `trend_basis` (the patient's own history).
- [ ] `provider_mode`, `pipeline_note` and `disclaimer` visible on every analysis view.
- [ ] Clinician sign-off `API ready` — `POST /analyses/{id}/review`, no request body.

## Reports
- [ ] Report preview page — **no API.** There is no preview-data endpoint; the PDF bytes
      are the only representation of a report's content.
- [ ] PDF download action `API ready` — `GET /reports/{id}/pdf`, an authenticated blob
      fetch, not a plain link. Respect the returned filename and `no-store`.
- [ ] Report history per analysis `API ready` — `GET /analyses/{id}/reports`.
- [ ] Generation is gated on sign-off: `POST /analyses/{id}/reports` returns 409
      `analysis_not_reviewed` until a clinician has signed. Disable the control and say
      why, rather than surfacing the 409 as a generic failure.

## Admin
- [ ] User management (create/list, assign roles) `API ready`
- [ ] Role-gated route protection (server-verified)

## System States
- [ ] 404 / not-found page
- [ ] 500 / error boundary page
- [ ] Empty states for every list/table
- [ ] Loading/skeleton states
- [ ] Offline/network-error handling

## Engineering & Cross-Cutting
- [ ] Confirm tech stack (Next.js/Tailwind or alternatives)
- [ ] Design tokens implemented in code
- [ ] Component library implemented in code
- [ ] API client & types for the full backend contract (Triage/Patient/Visit/Symptom/
      Scan/Analysis/Report/Admin). Generate from the live `openapi.json` via
      `scripts/dump_backend_routes.py` rather than hand-writing them.
- [ ] Server-verified route/session protection (not just middleware cookie)
- [ ] Responsive/mobile & tablet behavior
- [ ] Accessibility audit against baseline
- [ ] Performance budget (bundle size, Lighthouse targets)
- [ ] A CI job that runs the frontend build and tests. `backend-tests.yml` is currently
      the only workflow, so nothing here is enforced.
- [ ] No "certainty", "diagnosis", "confirmed" or treatment language anywhere in UI copy.
