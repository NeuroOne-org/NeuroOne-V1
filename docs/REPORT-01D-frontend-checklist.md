# REPORT-01D — Frontend Requirements & Backend Mapping Checklist

**Status:** Reference for future work, **partially superseded.** Written after AI-01C, CASE-01C, and REPORT-01A/B/C landed (backend HEAD includes `dcfbc7d5b2c9`).

Two things have changed since, and the tables below are stale where they conflict:

- **The auth surface grew.** `forgot-password`, `reset-password`, `request-otp` and `verify-otp` now exist, and the corresponding pages have been rebuilt against them. §1 understates the surface.
- **MRI is no longer excluded.** [ADR-006](decisions/ADR-006-mri-primary-with-symptoms-as-context.md) makes the scan a primary input attached to a visit, so guidance here that rests on the old PRD §7 exclusion no longer applies.

The §0 baseline finding — that this is mostly new pages, not a reconcile — still holds, and so does its central point that the existing frontend targets a different product than the backend serves.

**Purpose:** every field, endpoint, and error case the frontend needs to reproduce, taken directly from the current backend code (schemas/routers actually read, not assumed) — not from `docs/PRD.md`/`APP-FLOW.md` alone, per `AGENTS.md` §16.

---

## 0. Baseline finding: this is not a "reconcile," it's mostly new pages

Only these frontend files exist today, and all of them target a different product:

| File | Current contract | Reality |
|---|---|---|
| [frontend/src/lib/types.ts](../frontend/src/lib/types.ts) | `UserRole = "doctor"\|"admin"\|"receptionist"\|"researcher"`, `Patient` (with `mmse_score`, `latest_result`), `PredictionResult`, `DiseaseLabel`, `DiseaseStage` | None of this exists in the backend. Real roles are `ADMIN`/`CLINICIAN` only. |
| [frontend/src/app/dashboard/upload/page.tsx](../frontend/src/app/dashboard/upload/page.tsx) | POSTs an MRI file to `/patients`, expects a `latest_result` prediction back | No such endpoint — `POST /patients` takes `PatientCreate` JSON, so this 422s every time. **Rebuild, don't delete:** MRI intake is now in scope (ADR-006), but it belongs on a visit, not on patient creation. |
| [frontend/src/app/dashboard/patients/[id]/page.tsx](../frontend/src/app/dashboard/patients/[id]/page.tsx) | Renders `PredictionResult`/disease staging | Rewrite against the real `Patient`/`Visit` shape. |
| `login`, `forgot-password`, `reset-password`, `verify-otp` pages | Assume OTP + password reset flows exist | **Now true, and rebuilt against them.** Password login no longer forces an OTP; OTP is opt-in or for reset. `signup` remains unbacked — there is still no `/auth/register`. |
| [frontend/src/lib/api.ts](../frontend/src/lib/api.ts) | axios client, JWT cookie interceptor, `extractApiError` | Client and interceptor reusable. `extractApiError` **was** wrong — it read `data.detail`, but this API always returns `{message, error_code, details}`, so every backend message was replaced with a generic string. Since fixed. |

Net: keep the axios client and the shared `components/ui/*` kit; rebuild everything else. There are currently **zero** pages for Case/Visit, Symptom entry, Analysis, or Report.

---

## 1. Auth — smaller surface than the current pages assume

**Backend reality** ([backend/app/api/v1/auth.py](../backend/app/api/v1/auth.py), [backend/app/api/v1/admin.py](../backend/app/api/v1/admin.py)):

| Endpoint | Method | Auth | Notes |
|---|---|---|---|
| `/api/v1/auth/login` | POST | none | `{username, password}` → `{access_token, token_type}` |
| `/api/v1/auth/me` | GET | Bearer | → `UserResponse` |
| `/api/v1/admin/users` | POST | Bearer, ADMIN only | Provisions an ADMIN or CLINICIAN account. Not self-service. |

**There is no signup, forgot-password, reset-password, or OTP endpoint.** `app/schemas/auth.py` defines `OtpVerifyRequest`, `ForgotPasswordRequest`, `ForgotPasswordResponse`, `ResetPasswordRequest` as schemas, but **no router uses them** — they're dead contract, not a hidden feature. Do not build a frontend flow against them.

There is also no public bootstrap route: the first ADMIN is created by `AuthService.bootstrap_admin`, called only from a script/service context, not HTTP. **No seed script exists yet in this repo** — creating one (or documenting a manual `python -c` bootstrap step) is a backend prerequisite for demo data, not a frontend task. Flag this back before frontend work starts if no seed data exists.

### Checklist
- [ ] `POST /auth/login` — form with `username`, `password`. Store `access_token` in the existing cookie (`TOKEN_COOKIE` in `api.ts`), matching what's already wired.
- [ ] `GET /auth/me` on load / after login to populate the current user (id, role, name) for role-gated UI.
- [ ] **Delete** `signup`, `forgot-password`, `reset-password`, `verify-otp` pages and any link to them — there is nothing to call.
- [ ] Update `UserRole` type to `"admin" | "clinician"` only (matches `backend/app/models/user.py:UserRole`). Remove `"doctor"`, `"receptionist"`, `"researcher"`.
- [ ] 401 handling already exists in `api.ts`'s response interceptor (redirects to `/login`) — keep it, verify it still fires against the real `/auth/me`/token-expiry behavior.
- [ ] Decide (product question, not yours to invent): does the demo need an ADMIN-only "create clinician" screen against `POST /admin/users`? Not required by PRD §8's acceptance journey — only needed if there's no other way to get a demo clinician account. Confirm before building it.

---

## 2. Patients

**Backend reality** ([backend/app/api/v1/patients.py](../backend/app/api/v1/patients.py), [backend/app/schemas/patient.py](../backend/app/schemas/patient.py)):

| Endpoint | Method | Returns |
|---|---|---|
| `/api/v1/patients` | POST | `PatientResponse`, 201 |
| `/api/v1/patients` | GET (`page`, `page_size`, optional `doctor_id` for ADMIN) | `PatientListResponse` |
| `/api/v1/patients/search` | GET (`q`, `page`, `page_size`) | `PatientListResponse` |
| `/api/v1/patients/{id}` | GET | `PatientResponse` |
| `/api/v1/patients/{id}` | PATCH | `PatientResponse` |
| `/api/v1/patients/{id}` | DELETE | 204 (soft delete) |

**`PatientCreate` / `PatientResponse` fields** — build the TS type from exactly this, not from memory:

```ts
interface PhoneNumber { phone_number: string }  // 1-15 chars

interface PatientCreate {
  first_name: string;        // 1-20 chars
  last_name?: string | null; // 1-20 chars
  gender: string;            // exactly 1 char, e.g. "F"/"M"
  dob: string;                // ISO date
  phone: PhoneNumber[];       // min 1 entry
  email: string;              // valid email, <=255 chars
  address: string;            // 1-100 chars
  blood_group: string;        // 1-4 chars
  allergies: string[];        // required, [] is valid
  emergency_contact: string;  // 1-15 chars
  doctor_id?: string | null;  // only meaningful for ADMIN; CLINICIAN gets self-derived ownership
}

interface PatientResponse extends PatientCreate {
  id: string;
  doctor_id: string;
  doctor: UserResponse;      // nested, not just an id
  created_at: string;
  updated_at: string;
}
```

Note there is **no `mmse_score`, no `family_history`, no `latest_result`** — those were invented for the old MRI product. `allergies` is a plain string array, not free text.

### Checklist
- [ ] Patient list page: paginated table/list against `GET /patients`, with a search box wired to `GET /patients/search`.
- [ ] Patient create form matching the exact `PatientCreate` shape above, including the nested `phone[]` array (at least one row) and `allergies[]` (chip/tag input or comma-separated, but submit as an array).
- [ ] Patient detail page replacing [`patients/[id]/page.tsx`](../frontend/src/app/dashboard/patients/[id]/page.tsx): show `PatientResponse` fields, then the patient's visit list (see §3) — this is where the clinician navigates into a Case.
- [ ] Patient update (PATCH) — partial payload, all fields optional.
- [ ] Delete (soft-delete) with confirmation; ownership violations return 404 (ADR-001) — a patient belonging to another clinician must not be visible at all, not "403 forbidden."
- [ ] `doctor_id` filter/field is ADMIN-only in practice — don't expose it in the CLINICIAN create/list UI.

---

## 3. Clinical Case (Visit) + Symptoms

**Backend reality** ([backend/app/api/v1/patient_visits.py](../backend/app/api/v1/patient_visits.py), [backend/app/api/v1/visits.py](../backend/app/api/v1/visits.py), [backend/app/schemas/visit.py](../backend/app/schemas/visit.py), [backend/app/schemas/symptom.py](../backend/app/schemas/symptom.py)):

| Endpoint | Method | Notes |
|---|---|---|
| `/api/v1/patients/{patient_id}/visits` | POST | Open a case, optionally with `symptoms[]` inline. 201. |
| `/api/v1/patients/{patient_id}/visits/history` | GET (`limit`≤50, `order`=asc\|desc, `exclude_visit_id`) | Bounded window for cross-visit comparison — **not paginated**, different response shape than the list. |
| `/api/v1/patients/{patient_id}/visits` | GET (`page`, `page_size`, `status`) | Paginated. |
| `/api/v1/visits/{id}` | GET / PATCH | Flat, not nested — visit ids are globally unique. |
| `/api/v1/visits/{id}` | DELETE | 204, cascades to symptoms. |
| `/api/v1/visits/{id}/symptoms` | GET (paginated) / POST | |
| `/api/v1/visits/{id}/symptoms/{symptom_id}` | PATCH / DELETE | |

**Types:**

```ts
interface Vitals {
  bp_systolic?: number | null;    // 0-300
  bp_diastolic?: number | null;   // 0-200
  heart_rate?: number | null;     // 0-300
  respiratory_rate?: number | null; // 0-100
  temperature_c?: number | null;  // 25-45
  spo2?: number | null;           // 0-100
  weight_kg?: number | null;      // 0-700
  height_cm?: number | null;      // 0-300
}

type VisitStatus = "draft" | "submitted" | "analyzed" | "closed";
// "analyzed" is AI-owned: the create/update forms must reject/disable setting
// it manually. Setting it directly is a 422 (test_setting_the_ai_owned_status_is_rejected).

type SymptomOnset = "sudden" | "subacute" | "gradual" | "insidious" | "unknown";

interface SymptomCreate {
  symptom_name: string;    // 1-100 chars
  severity: number;        // 1-10, integer
  duration_days?: number | null;
  onset?: SymptomOnset | null;
  observation?: string | null;   // NEW (CASE-01C): 0-2000 chars, rejected if whitespace-only
}

interface SymptomResponse extends SymptomCreate {
  id: string;
  visit_id: string;
  created_at: string;
  updated_at: string;
}

interface VisitCreate {
  chief_complaint: string;   // 1-255 chars
  history?: string | null;
  vitals?: Vitals;
  notes?: string | null;
  visit_date?: string | null;  // defaults server-side if omitted
  status?: VisitStatus | null; // omit or leave undefined; never send "analyzed"
  symptoms?: SymptomCreate[];  // can create the case and its symptoms in one request
}

interface VisitResponse extends VisitCreate {
  id: string;
  patient_id: string;
  visit_date: string;
  status: VisitStatus;
  symptoms: SymptomResponse[];
  created_at: string;
  updated_at: string;
}
```

### Checklist
- [ ] "New case" form under a patient: `chief_complaint` (required), optional `history`/`notes`/vitals block, and an inline symptom builder (repeatable rows: name, severity slider 1-10, duration, onset dropdown, **observation textarea**). Submitting creates the visit and its symptoms in one `POST`.
- [ ] Case detail page: visit metadata + symptom list, with add/edit/delete symptom actions hitting the item-level symptom endpoints. **The observation field must be visible and editable** — it's the field CASE-01C added specifically so this isn't lost.
- [ ] Case history view for a patient (distinct component from the paginated list) using `GET /patients/{id}/visits/history` — this is what cross-visit trend context (the `early_watch` demo case) depends on, so the demo journey needs at least 2 prior visits before triggering analysis.
- [ ] Never render a control that lets the user set `status` to `"analyzed"` directly — that transition is written by the AI pipeline only.
- [ ] Symptom validation client-side should mirror the server: severity 1-10, name required, observation rejected if it's only whitespace or over 2000 chars (the API 422s on both; show the message, don't just guess).

---

## 4. AI Analysis + Differential Diagnosis + Evidence

**Backend reality** ([backend/app/api/v1/visits.py](../backend/app/api/v1/visits.py) for trigger/list, [backend/app/api/v1/analysis.py](../backend/app/api/v1/analysis.py) for item reads, [backend/app/schemas/analysis.py](../backend/app/schemas/analysis.py)):

| Endpoint | Method | Notes |
|---|---|---|
| `/api/v1/visits/{visit_id}/analyses` | POST | Body: `{history_limit?: number}` (0-50, default 10). `{}` is valid. Runs the pipeline synchronously; 201 on success, **502** on any AI/RAG failure. |
| `/api/v1/visits/{visit_id}/analyses/latest` | GET | 404 before any analysis exists. |
| `/api/v1/visits/{visit_id}/analyses` | GET (paginated) | History of re-runs — re-running never overwrites a prior analysis. |
| `/api/v1/analyses/{id}` | GET | Flat, not nested — analysis ids are globally unique. |

**Types** — this is the safety-boundary-sensitive part; field names are load-bearing, not cosmetic:

```ts
type DiagnosisCategory = "differential_diagnosis" | "early_watch";
type LikelihoodBand = "low" | "moderate" | "high";  // render this, never the raw number as a percentage

interface EvidenceResponse {
  source: string;
  citation: string;
  relevant_passage: string;
  document_id?: string | null;       // added by AI-01C
  chunk_id?: string | null;          // added by AI-01C
  source_url?: string | null;
  source_tier?: string | null;       // "guideline" | "systematic_review" | "primary_study" | "reference_text"
  published_year?: number | null;
  relevance_score?: number | null;   // added by AI-01C
}

interface TrendBasisRef {
  visit_id: string;
  symptom_id?: string | null;
  symptom_name: string;
  visit_date: string;
  severity?: number | null;
  observation: string;
}

interface FindingResponse {
  id: string;
  rank: number;
  name: string;               // maps from condition_name server-side; NOT "diagnosis"
  category: DiagnosisCategory;
  confidence: number;          // 0-1; DO NOT display as a raw percentage as if it were certainty
  likelihood_band: LikelihoodBand;  // display THIS as the primary confidence language
  supporting_findings: string[];
  contradicting_findings: string[];
  trend_basis: TrendBasisRef[];     // patient's OWN history — render visually distinct from evidence
  evidence: EvidenceResponse[];     // EXTERNAL literature — never merge with trend_basis in the UI
}

interface AnalysisResponse {
  id: string;
  visit_id: string;
  model_name: string;
  provider_mode: "simulated" | "live";
  pipeline_note: string;   // e.g. "pipeline complete, evidence retrieval simulated" — show this prominently
  disclaimer: string;      // show this prominently, always
  generated_at: string;
  findings: FindingResponse[];
  created_at: string;
  updated_at: string;
  // context_snapshot is intentionally NOT on the wire — don't expect it
}
```

### Checklist
- [ ] "Run analysis" action on a case (POST with default/optional `history_limit`), with a loading state — this can take a moment and any AI/RAG failure is a controlled 502 (see error mapping in §6), not a silent failure.
- [ ] Differential diagnosis review screen ("Clinician Review" step of PRD §8): ranked findings, each showing `name`, `category`, `likelihood_band` (not the raw `confidence` float as a headline number), `explanation`... wait, check: is `explanation` on `FindingResponse`? **Yes** — it's in the schema (`explanation: str`), include it in the type above (omitted by oversight — add `explanation: string;` to `FindingResponse`), supporting/contradicting findings, and evidence with citations.
- [ ] **Visually separate `trend_basis` from `evidence`** in the finding card — e.g., a distinct "Patient History" panel vs. an "External Evidence / Citations" panel. This is not a styling nicety; AGENTS.md §8.2 treats conflating them as a contract violation.
- [ ] `provider_mode`/`pipeline_note` must be visible on every analysis view — this is how a clinician (and a demo audience) can tell simulated evidence from live evidence. Don't hide it in a tooltip.
- [ ] `disclaimer` must be visible on every analysis view, not just in the eventual PDF.
- [ ] Never use "diagnosis," "confirmed," "certainty," or treatment language anywhere in the UI copy around this data — mirror the vocabulary the backend already enforces (`AGENTS.md` §8.2, §15 Clinical Safety).
- [ ] Analysis history for a case (list of past runs) so a clinician can see prior differentials, not just the latest.

---

## 5. Clinician Review → PDF Report

**Backend reality** ([backend/app/api/v1/analysis.py](../backend/app/api/v1/analysis.py) for the nested create/list, [backend/app/api/v1/reports.py](../backend/app/api/v1/reports.py) for item reads/download, [backend/app/schemas/report.py](../backend/app/schemas/report.py)):

| Endpoint | Method | Notes |
|---|---|---|
| `/api/v1/analyses/{analysis_id}/reports` | POST | No request body. Builds a snapshot, proves it renders, persists metadata. 201 `ReportResponse`. Renders **before** persisting — a render failure is a 500 with `error_code: "report_render_error"` and nothing is saved. |
| `/api/v1/analyses/{analysis_id}/reports` | GET (paginated) | An analysis can have multiple reports; none are ever overwritten. |
| `/api/v1/reports/{id}` | GET | Metadata only — no snapshot on the wire. |
| `/api/v1/reports/{id}/pdf` | GET | Binary PDF. Re-renders from the stored snapshot on every call (never cached, never stale). |

**Types:**

```ts
interface ReportResponse {
  id: string;
  analysis_id: string;
  generated_by_id: string;
  generated_at: string;
  filename: string;         // "neuroone-report-{id}.pdf" — safe to display, no PHI in it
  created_at: string;
  updated_at: string;
  // NOTE: no `snapshot` field on the wire, by design
}
```

**PDF download headers to respect, not fight:**
- `Content-Disposition: attachment; filename="neuroone-report-{id}.pdf"` — use this filename, don't invent one.
- `Cache-Control: private, no-store` — don't cache the blob in a service worker or browser cache layer; re-fetch each time.
- `Content-Type: application/pdf`.

### Checklist
- [ ] "Generate report" button on the analysis review screen, calling `POST /analyses/{id}/reports`. On success, immediately offer the download (don't make the clinician navigate away and back).
- [ ] Report history list per analysis (multiple reports are allowed and expected — e.g., regenerate after further review).
- [ ] Download action: `GET /reports/{id}/pdf` as an **authenticated** blob fetch (the browser can't just link to it directly, since it needs the `Authorization: Bearer` header the axios client already attaches) — fetch as blob, then trigger a save via an object URL. This is the one place the existing `api.ts` axios instance needs a `responseType: "blob"` call, not a new client.
- [ ] Handle the render-failure case (500, `report_render_error`) distinctly from a 404 — retain the review screen and offer retry, per the plan's failure-behavior requirement; don't show a generic error page.
- [ ] Do not attempt to preview the PDF's content anywhere except via the actual downloaded/rendered file — there is no separate "preview data" endpoint; the PDF bytes are the only representation.

---

## 6. Cross-cutting: error handling contract

Every backend error follows one shape ([backend/app/schemas/common.py](../backend/app/schemas/common.py) `ErrorResponse`, wired in [backend/app/utils/handlers.py](../backend/app/utils/handlers.py)):

```ts
interface ApiError {
  message: string;
  error_code: string | null;
  details?: unknown;
}
```

`extractApiError` in `api.ts` already reads `.detail`... **check this**: the actual field is `message`, not `detail`. This existing helper was written against the old (different) backend and needs to be fixed to read `error.response.data.message` (falling back to `error_code`), not `.detail`. This is a real, verified bug in the code that's supposedly "reusable as-is" from §0 — the axios plumbing is reusable, but `extractApiError`'s field name is not.

| HTTP | Meaning here | UI treatment |
|---|---|---|
| 401 | Expired/invalid token | Already handled: redirect to `/login` (verify it still works against the real flow). |
| 403 | Wrong role for an admin-only action | Show a permission message; don't offer a retry. |
| 404 | Entity missing **or** owned by another clinician (ADR-001/002/004 all mask this identically) | Show "not found," never imply "you don't have permission" — the backend deliberately hides which case it is. |
| 422 | Validation failure | `details` carries per-field pydantic errors — surface them against form fields where practical, not just a toast. |
| 502 | AI/RAG pipeline failure (`error_code`: `ai_error`, `rag_error`, `rag_no_evidence`, `ai_contract_error`, `ai_no_candidates`) | The clinical record is guaranteed untouched (AGENTS.md §8.5) — message should invite retry, not suggest data was lost. |
| 500 | Report render failure (`error_code: "report_render_error"`) or truly unexpected | Retry-safe for the render case; generic error otherwise. |

### Checklist
- [ ] Fix `extractApiError` to read the real error shape (`message`, `error_code`), not `detail`.
- [ ] A shared "empty analysis" state (case exists, no analysis run yet) distinct from "loading" and "error."
- [ ] A shared 404 component used identically for patient/visit/analysis/report — don't let any of them leak more detail than the backend already chose to hide.

---

## 7. Explicit non-goals (do not build these)

Carried over from `AGENTS.md` §19 and confirmed still true by reading the current backend:

- No MRI/image upload or display, anywhere.
- No treatment recommendations or "confirmed diagnosis" language.
- No clinician e-signature or report approval workflow — "Clinician Review" is just the screen where findings are shown before generating a report, not a sign-off step with its own state machine.
- No RECEPTIONIST role UI.
- No self-service signup/password-reset UI (see §1) — the backend genuinely does not support it yet.

---

## 8. Suggested build order (mirrors the dependency chain, not equal-sized steps)

1. Fix `api.ts`'s `extractApiError` + confirm `login`/`me` against the real contract; delete the dead auth pages.
2. Types file rewrite (`types.ts`) against §2-§5 above, in full, before any page work — every page below depends on this being right once.
3. Patient list/create/detail (§2).
4. Case creation + symptom entry, including the case history view (§3) — history is required before analysis can demonstrate `early_watch`.
5. Analysis trigger + review screen (§4) — this is the highest-value screen for the demo; get the `trend_basis`/`evidence` visual separation right here.
6. Report generation + download (§5).
7. Delete `upload/page.tsx` and `mri-dropzone` last (or first — order doesn't matter, but don't ship with it still linked from navigation at any point).

---

## 9. Verification before calling REPORT-01D done

- [ ] Frontend production build passes.
- [ ] Manual browser run of the full PRD §8 journey: login → create patient → create case with 2+ visits (to get a real `early_watch`) → enter symptoms with observations → run analysis → review differential with evidence/trend_basis visually separated → generate report → download and open the PDF.
- [ ] No MRI/upload flow reachable from any nav path.
- [ ] A second clinician account cannot see the first clinician's patients/cases/analyses/reports through the UI (matches the backend's 404 masking).
