# NeuroOne — Frontend

Next.js 16 (App Router) + TypeScript frontend for the NeuroOne clinical
decision-support platform, built against the team's FastAPI backend.

## Stack

- **Next.js 16** (App Router, proxy-based route protection)
- **TypeScript**
- **Tailwind CSS** — custom design tokens in `tailwind.config.ts` (no shadcn
  dependency; a small set of hand-built primitives lives in
  `src/components/ui/`, styled to the same effect)
- **React Hook Form + Zod** — all forms are schema-validated
- **Axios** — API client with an auth-token interceptor and centralized
  401 handling

## Getting started

```bash
cd frontend
npm install
cp .env.local.example .env.local   # point NEXT_PUBLIC_API_URL at your backend
npm run dev
```

Visit `http://localhost:3000`. You'll land on `/login` until authenticated;
`/dashboard/*` is protected by `src/proxy.ts` (Next 16's renamed middleware).

## Backend contract this frontend expects

The backend's auth/patient/model modules aren't built yet as of this
writing, so the frontend is coded against the following **assumed**
contract. Whoever builds the backend should either match this, or the
frontend should be updated to match whatever's actually implemented —
whichever is easier for the team.

| Endpoint | Method | Body | Returns |
|---|---|---|---|
| `/auth/login` | POST | form-encoded `username`, `password` (OAuth2 password flow) | `{ access_token, token_type }` |
| `/auth/signup` | POST | JSON `{ full_name, email, role, password }` | creates an **unverified** user and emails a 6-digit OTP; no token yet |
| `/auth/verify-otp` | POST | JSON `{ email, otp }` | `{ access_token, token_type }` on success |
| `/auth/resend-otp` | POST | JSON `{ email }` | 204/200, triggers a new email |
| `/users/me` | GET | — (Bearer token) | `User` |
| `/patients` | GET | — | `Patient[]` |
| `/patients` | POST | `multipart/form-data`: `full_name, age, gender, mmse_score?, family_history, notes?, mri_scan` | created `Patient` (with `latest_result` if the pipeline finishes synchronously, or `null` if it's still processing) |
| `/patients/{id}` | GET | — | `Patient` (including `latest_result`) |

**Password rule enforced client-side:** 8+ characters, at least one
uppercase, one lowercase, one digit, one special character. The backend
should enforce the same rule server-side too — client-side validation is
UX, not security.

**On OTP / email verification:** sending the actual code requires a real
email provider on the backend (SMTP via Gmail, SendGrid, etc.) — the
frontend can't send email itself. `requirements.txt` already has
`email-validator`, so this was clearly already on the radar; someone just
needs to wire up the actual send step and a way to store/expire OTPs
(e.g. a short-lived `otp_code` + `otp_expires_at` column on the user, or
a separate table).

Types for all of these are in `src/lib/types.ts`. If the real backend
shapes differ (field names, nesting, etc.), that file plus
`src/lib/api.ts` and the two data-fetching hooks/pages are the only
places that need to change — the rest of the UI consumes the typed
`Patient` / `PredictionResult` objects, not raw API responses.

## Structure

```
src/
  app/
    login/, signup/          — auth pages (public)
    dashboard/
      layout.tsx              — sidebar shell
      page.tsx                — patient list
      upload/page.tsx         — MRI upload + intake form
      patients/[id]/page.tsx  — patient record + prediction results
  components/
    ui/                       — Button, Input, Select, Card, Badge, etc.
    auth-provider.tsx          — auth context (login/signup/logout, current user)
    auth-shell.tsx              — split-panel layout for login/signup
    confidence-dial.tsx         — radial confidence gauge (results page)
    mri-dropzone.tsx             — drag/drop MRI upload with scan-line state
    region-bars.tsx               — contributing-region bar chart
  lib/
    api.ts        — axios instance, token interceptor, error helper
    types.ts      — shared TS types (Patient, PredictionResult, User…)
    validation.ts — Zod schemas for every form
    utils.ts      — cn(), formatters
  proxy.ts        — redirects based on auth cookie
```

## Design notes

The UI leans into a radiology-viewer aesthetic (dark, high-contrast,
mono-spaced data readouts) rather than a generic SaaS dashboard look,
since the primary users are reading MRI-derived data. The confidence
gauge on the results page is a custom SVG instrument dial rather than a
donut chart, deliberately evoking a monitoring display.

## Docker

The repo's root `docker-compose.yml` runs Postgres, a one-shot `migrate`
job and the `api` service, but not the frontend yet. To wire it in, add
something like this:

```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - api
```

`NEXT_PUBLIC_API_URL` is read by the browser, so it must be an address the
browser can reach, not the in-network `api` hostname.

`frontend/Dockerfile` is a standard multi-stage Next.js build
(`output: "standalone"` is already set in `next.config.mjs` to keep the
final image small).

## Known gaps / next steps

- No file-type validation beyond the browser `accept` attribute — worth
  tightening once the backend's actual accepted MRI formats are locked in
  (NIfTI vs DICOM vs flat images changes the upload/preview logic a fair
  bit).
- Pagination on the patient list is currently client-side (fine at
  mini-project scale, fetches the whole list and paginates in the
  browser). Once the backend is real, swap `usePatients` to accept
  `page`/`limit` query params instead.
- Polling: the patient detail page now polls `/patients/{id}` every 4s
  (capped at ~2 minutes) while `latest_result` is null, so it updates
  itself once the pipeline finishes. If the backend later exposes a
  websocket or SSE endpoint for job status, that'd be a cleaner
  replacement.
