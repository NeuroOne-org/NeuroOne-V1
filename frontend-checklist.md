# NeuroOne Frontend — Redesign Checklist

Frontend rebuild from scratch. `API ready` = backend endpoint already exists for that page.

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
- [ ] OTP verification (resend + expiry countdown) — **not implemented.** Login issues a JWT
      directly; no OTP step exists in the current backend.
- [ ] Forgot / reset password — **not implemented.** No backend endpoint exists for this yet;
      flag to product/backend before designing this screen.
- [ ] Session-expired / 401 handling

## Account & Settings
- [ ] Profile / account settings page `API ready`
- [ ] Change password
- [ ] Notification preferences

## Patient Management
- [ ] Patient list (search, filter, pagination) `API ready`
- [ ] Patient create (intake form) `API ready`
- [ ] Patient detail (profile + visit history) `API ready`

## Clinical Input
- [ ] Visit detail (symptoms, MRI upload/status, linked analysis) `API ready`
- [ ] Symptom entry/edit form `API ready`
- [ ] MRI upload + processing status `API ready`

## Diagnosis & Explainability
- [ ] Analysis/results view per visit `API ready`
- [ ] Confidence gauge `API ready`
- [ ] Contributing regions visualization `API ready`
- [ ] Trend view across visits `API ready`
- [ ] Literature/evidence panel (citations) `API ready`

## Reports
- [ ] Report preview page `API ready`
- [ ] PDF download action `API ready`
- [ ] Report history per patient/visit `API ready`

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
- [ ] API client & types for full backend contract (Visit/Symptom/Analysis/Report/Admin)
- [ ] Server-verified route/session protection (not just middleware cookie)
- [ ] Responsive/mobile & tablet behavior
- [ ] Accessibility audit against baseline
- [ ] Performance budget (bundle size, Lighthouse targets)
