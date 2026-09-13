# NeuroONE Frontend Redesign (parked)

> **Status: parked design reference, not a build target.**
> `frontend/src` remains the application. This directory is kept for its design
> work — `DESIGN.md`, the auth shell, the token set and the self-hosted fonts —
> and is not where the clinician journey gets built. Do not add routes here.
> Porting the design work into `frontend/src` is the expected path; see the
> "Parked state" section below for what is unfinished.

This directory contains the isolated Next.js login redesign. The existing
application in `frontend/src` remains unchanged. All redesign files, assets,
configuration and dependencies live here. `DESIGN.md` is a verbatim copy of
the supplied document: the repository root did not contain that file.

## Preview

From this directory:

```sh
npm install
npm run dev
```

Open http://localhost:3100/login. `/` redirects to `/login`.
Run `npm run build`, `npm run lint` and `npm run typecheck` to verify.
`npm start` serves a production build on port 3100.

The preview reuses the existing frontend's API client and loginSchema;
it is intentionally kept in this repository rather than being a standalone
copy of the auth implementation. Its dependency list is a subset of the
existing frontend/package.json; no new library was introduced.

## Account-flow handoff

Run the existing frontend separately on port 3000 to use its OTP,
and forgot-password screens. Successful credential submission hands
off to that app's existing `/verify-otp` route. For another deployment,
set `NEXT_PUBLIC_EXISTING_APP_URL` to that frontend's origin before building.
The shared API client uses `NEXT_PUBLIC_API_URL` (default
`http://localhost:8000/api/v1`). Use only synthetic demo credentials.

The secondary button is now "Sign in via OTP", replacing Google sign-in at
the user's request. It submits the same validated email/password form as
Log In, then hands off to OTP verification; it is not a passwordless flow.
Both buttons disable during submission. Registration has been removed from
the login screen. Remember-me remains disabled with an accessible explanation.
No credentials are saved and no cookie lifetime is changed.

This explicit follow-up supersedes DESIGN.md's original Google and register
elements; the supplied design document is retained unchanged for provenance.

## Design implementation

- Product colors, Brand colors, wordmark stack and type sizes follow DESIGN.md.
- IBM Plex Sans (400–600) and Cormorant Garamond (400) are self-hosted Latin
  WOFF2 fonts; source URLs and licenses are in `public/fonts/README.md`.
- The Seira declaration is copied exactly from DESIGN.md. Add the licensed
  `Seira.woff2` or `Seira.otf` to `public/fonts` when available. Until then the
  browser falls back to the bundled Cormorant Garamond. Missing Seira requests
  may show ordinary 404s in developer tools; they do not block rendering or
  trigger an application error.
- The static SVG branches/nodes are explicitly commented as placeholder
  artwork pending a commissioned asset. Amber appears at exactly one node.
- Below 768px the art is hidden. The form stays in normal document flow,
  including validation errors and short-screen scrolling.
- The emil-design-eng skill informed 48px controls, visible keyboard focus,
  pointer-only press feedback and reduced-motion handling. No entrance or
  looping decorative animation delays the form.

## Files in this change

Final production build (including lint/types), responsive browser checks,
failure/retry behavior and independent source review passed. Full verification
details and limits are recorded at the end of `PLAN.md`.

`DESIGN.md`, `PLAN.md`, `README.md`, `.gitignore`, `eslint.config.mjs`,
`package.json`, `package-lock.json`, `next-env.d.ts`, `next.config.mjs`,
`tsconfig.json`, `postcss.config.js`, `tailwind.config.ts`,
`src/app/layout.tsx`, `src/app/page.tsx`, `src/app/login/page.tsx`,
`src/app/globals.css`, `src/components/auth-shell.tsx`,
`src/components/login-form.tsx`, `src/components/password-strength.tsx`,
`src/components/synapse-artwork.tsx`,
`public/fonts/README.md`, `public/fonts/cormorant-garamond-latin.woff2`,
`public/fonts/ibm-plex-sans-latin.woff2`,
`public/fonts/OFL-Cormorant-Garamond.txt`, `public/fonts/OFL-IBM-Plex-Sans.txt`.

## Parked state

Two changes were in progress when this directory was parked. Both are committed
so nothing is lost, but neither was verified by a build:

- `LoginShell` was generalised into `AuthShell`, taking `heading`, `headingId`
  and `subtitle` props so a second auth screen could reuse the split layout.
  `login-shell.tsx` is deleted and nothing references it.
- `PasswordStrength` (`src/components/password-strength.tsx`) exists but is
  imported by nothing. It was started for a reset-password screen that was
  never built. It is dead code until that screen exists — delete it or wire it
  up, but do not assume it works.

The last verification recorded in `PLAN.md` predates both changes.

## Required product journey

Revised by [ADR-006](../../docs/decisions/ADR-006-mri-primary-with-symptoms-as-context.md)
after this directory was written:

`Login -> Triage Queue -> Patient -> Visit (Scan + Symptoms) -> AI Analysis -> Ranked Differential + Evidence -> Clinician Sign-off -> PDF Report`

## Design boundaries

- Build a clinician-assist interface, never an autonomous diagnosis product.
- **MRI/image analysis is now in scope** as a primary input (ADR-006). The
  earlier exclusion recorded here is superseded. A stage estimate may appear
  only as the top-ranked candidate in a ranked differential — never as a lone
  verdict, and never beside a confidence above 92%.
- Do not add uploaded diagnostic-report analysis, treatment decisions,
  self-service signup, or the deferred `RECEPTIONIST` role.
- Keep patient history (`trend_basis`) visually distinct from external medical
  evidence and citations.
- Show simulated/live provider state, pipeline notes, uncertainty language, and
  the clinical disclaimer prominently wherever analysis results appear.
- Preserve the current FastAPI contracts documented in
  `docs/REPORT-01D-frontend-checklist.md`.

The implementation plan and checks are recorded in `PLAN.md`. No backend
files or existing frontend source files were edited. The root graph was not
regenerated because the final instruction confines work to this folder.
