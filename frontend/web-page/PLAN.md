MODE: PLAN

1. Objective: rebuild login to the supplied DESIGN.md and reference layout.
2. Current state: branch codex/frontend-redesign at 42e6d1b; web-page contains only a README. Existing src uses Next 14 App Router, Tailwind, local React state, Zod and an AuthProvider. Root DESIGN.md and docs/references/login-reference.png are absent; use the attached design document and screenshot.
3. Relevant requirements: DESIGN §§1–5; PRD FR-01 and §7; APP-FLOW §2; existing frontend auth contracts.
4. Resolved decisions: user explicitly requested implementation inside web-page. Keep the exact supplied palette, fonts and element order. Existing frontend remains the account-flow destination.
5. Assumptions: preview runs at localhost:3100; existing app runs at localhost:3000, configurable through NEXT_PUBLIC_EXISTING_APP_URL. Synthetic credentials only for verification.
6. Scope: isolated login preview, typed components, scoped Tailwind/CSS, self-hosted open fonts, setup notes.
7. Out of scope: backend, existing src changes, OAuth, persistence-policy changes, dashboard and other auth redesigns.
8. Architecture impact: isolated Next preview shares the existing API client and validation through a TS alias. The login payload matches AuthProvider.login; OTP/session handling stays in the existing app. No backend layer changes.
9. Design options: modify shared AuthShell (affects all auth screens) or isolate the redesign (requested). Choose isolation.
10. Recommended design: two equal desktop panels, 360px maximum form measure, white surface on Product bg, hidden artwork below 768px; 6/8px incumbent corners; static SVG branches and nodes.
11. Data/schema impact: N/A; no stored data or schema changes.
12. API/contract impact: unchanged credential submission and OTP handoff. Google displays unavailable feedback and remember-me is disabled with an accessible explanation; no fabricated provider or storage semantics.
13. AI/RAG impact: N/A; no analysis changes.
14. Security/privacy impact: reuse auth; never store passwords, change cookies, or log credentials. Clamp return paths to local routes.
15. Clinical safety impact: preserve clinician-assist framing; no diagnostic or MRI claims added.
16. Failure/recovery: visible linked field errors, preserved entries, server-error alert, retry after failure; absent Seira falls back to bundled Cormorant.
17. Implementation tasks: AUTH-UI-01 scaffold/config and fonts; AUTH-UI-02 shell and SVG; AUTH-UI-03 form/feedback; AUTH-UI-04 verify and document. Each task is complete when its declared files compile and the corresponding criteria below pass.
18. Dependencies: config/fonts before shell, shell before visual checks; existing API client/loginSchema before form.
19. Testing strategy: typecheck, lint, production build; desktop/mobile screenshots; check keyboard focus, password toggle, validation, pending/error behavior, account destinations, token values, missing-font fallback and overflow.
20. Acceptance criteria: all requested elements in order; exact tokens and type scale; desktop split/mobile form; named placeholder comment; no new library outside parent package.json; backend untouched. Full PRD journey is outside this visual change.
21. Documentation updates: preserve supplied DESIGN.md verbatim inside web-page; README setup, handoff and known gaps; font provenance/licenses.
22. Risks/open issues: Seira and commissioned artwork remain open by instruction. Existing auth implementation differs from source-of-truth flow (OTP); preserve it for this visual task. Google/session persistence are unsupported. No root graph update because the final user instruction confines writes to web-page.
23. Build readiness: user supplied the design and explicitly requested implementation; no unresolved visual decision.

BUILD READY

## Implementation result — 2026-09-11

The isolated preview was implemented inside frontend/web-page. The initial
shared AuthProvider import produced a duplicate React runtime during server
rendering. The preview now imports only the existing API client, error helper
and loginSchema, submitting the same username/password payload; OTP and
session handling remain in the original app. Type roots and explicit module
resolution keep dependency installation confined to web-page. No validation
or build checks were disabled.

MODE: TEST

Scope: login preview, responsive layout, form interaction and build.
Requirements Verified: DESIGN §§1–4; explicitly marked §5 artwork placeholder;
requested element order; no new library/version range relative to frontend.
Tests Run: production build with lint and TypeScript validation; standalone
typecheck; UI detector; browser checks at 1440×960, 390×844 and 320×740;
font HTTP checks; exact Seira declaration and supplied-document comparison;
independent source finish review.
Passed: build/lint/types; no detector findings; exact declared colors/type
scale; two-panel desktop and hidden mobile art; no horizontal overflow;
password show/hide; empty-form validation and first-invalid focus; Google
unavailable feedback; native disabled remember-me; loading disables submit;
network error preserves inputs and re-enables retry; both WOFF2 assets HTTP200;
Seira HTTP404 falls back without blocking the UI. Source reviewer: SHIP.
Failed: none outstanding in the scoped checks.
Regression Status: existing frontend src and backend unchanged.
Logic Assessment: existing credential request shape and OTP parameter handoff
preserved. Account-flow destinations verified by source/DOM, not successful
live authentication.
Security Assessment: no credentials persisted or logged by the new code;
no session lifetime or authorization changes; local return-path guard present.
Clinical Safety Assessment: no autonomous diagnosis, treatment or MRI claims
introduced by the login preview.
Known Gaps: live authentication/OTP success not exercised (backend unreachable);
real Seira and commissioned artwork pending; Google sign-in and remember-me
unsupported. Independent review was source-only; main agent inspected renders.
Final Verdict: PASS WITH KNOWN LIMITATIONS

## Follow-up: OTP button and registration removal

User requested replacing Google sign-in with "Sign in via OTP" and removing
registration. The secondary button submits the existing form through its HTML
form association, preserving validation, pending state, error handling and
credential-to-OTP handoff. Both submit buttons disable while pending. The Google
icon/notice and entire register paragraph are removed. No passwordless endpoint,
backend change, or auth contract change is introduced. This follow-up supersedes
the original Google/register layout requirement and related verification notes.
