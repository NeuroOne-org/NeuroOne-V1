# REPORT-01D — Frontend Requirements & Backend Mapping Checklist

**Status:** Current. Reconciled against the backend on September 12, 2026, at `89b4a8d`.

This document is the **contract map**: what the API actually accepts and returns, read from schemas and routers rather than from `docs/PRD.md`/`APP-FLOW.md`. The companion [`frontend-checklist.md`](../frontend-checklist.md) at the repository root is the **build checklist** — which screens, states and design foundations to produce. Where the two disagree about the API, this file wins.

It previously carried a "partially superseded" banner because the auth surface had grown and [ADR-006](decisions/ADR-006-mri-primary-with-symptoms-as-context.md) had admitted MRI. Both are now folded into the body below, along with the triage queue and clinician sign-off that ADR-006 added. Two sections are lettered rather than renumbered — §1A (triage) and §3A (scan intake) — so existing references to §1 through §9 keep pointing at the same material.

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
| `login`, `forgot-password`, `reset-password`, `verify-otp` pages | Assume OTP + password reset flows exist | **Now true, and rebuilt against them.** Password login no longer forces an OTP; OTP is opt-in or for reset. `signup` remains unbacked — there is still no `/auth/register`, and a regression test asserts it 404s. |
| [frontend/src/lib/api.ts](../frontend/src/lib/api.ts) | axios client, JWT cookie interceptor, `extractApiError` | Client and interceptor reusable. `extractApiError` **was** wrong — it read `data.detail`, but this API always returns `{message, error_code, details}`. Fixed: it now reads `message` first and falls back to `detail` only for responses that never entered the app, such as Starlette's own 404 for an unrouted path. |
| [frontend/src/app/dashboard/page.tsx](../frontend/src/app/dashboard/page.tsx) | Hardcoded `PATIENTS` array, stat tiles including "Avg. confidence / Model certainty", `Critical`/`Stable` status vocabulary | None of it is backed by the API, and the framing is what ADR-006 decision 7 and FR-04 forbid. **Replace with the triage queue (§1A), do not repoint.** |

Net: keep the axios client and the shared `components/ui/*` kit; rebuild everything else. There are currently **zero** pages for Case/Visit, Symptom entry, Analysis, or Report.

---

## 1. Auth

**Backend reality** ([backend/app/api/v1/auth.py](../backend/app/api/v1/auth.py), [backend/app/api/v1/admin.py](../backend/app/api/v1/admin.py)):

| Endpoint | Method | Auth | Notes |
|---|---|---|---|
| `/api/v1/auth/login` | POST | none | `{username, password}` → `{access_token, token_type}` |
| `/api/v1/auth/me` | GET | Bearer | → `UserResponse` |
| `/api/v1/auth/request-otp` | POST | none | Issues an OTP for the opt-in OTP sign-in path |
| `/api/v1/auth/verify-otp` | POST | none | → `Token`, same shape as login |
| `/api/v1/auth/forgot-password` | POST | none | Starts the hardened OTP reset flow |
| `/api/v1/auth/reset-password` | POST | none | Completes it |
| `/api/v1/admin/users` | POST | Bearer, ADMIN only | Provisions an ADMIN or CLINICIAN account. Not self-service. |

**The OTP and password-reset endpoints are real.** An earlier edition of this document said they were dead schemas with no router — that was true when it was written and is not true now. Password login does **not** force an OTP: OTP is an opt-in sign-in path and the mechanism behind password reset.

**Self-registration is still absent and deliberately so.** There is no `/auth/register`; AUTH-01 removed it and a regression test asserts it returns 404. Accounts are admin-provisioned through `POST /admin/users`.

There is no public bootstrap route: the first ADMIN is created by `AuthService.bootstrap_admin`, called from a script rather than over HTTP. Two scripts exist for demo data: `scripts/bootstrap_admin.py` and `scripts/seed_demo_case.py`. The seed follows ADR-006.

- **`demo-clinician`** gets five synthetic patients, one per queue state. Every visit carries a scan and symptoms.
  - Early watch, worsening trend and awaiting sign-off together.
  - An imaging-only worsening trend (MRI stage CN → MCI → Mild).
  - Awaiting sign-off only.
  - Signed off.
  - A returning patient whose latest visit is deliberately left unanalysed for a live run.
- **`demo-clinician-2`** owns one patient, for the cross-clinician isolation check.

Seeded analyses always use the mock providers. Re-running replaces only the two demo accounts' data. `backend/tests/test_seed_demo_case.py` replays every scenario through the real mock pipeline and asserts its queue flags.

### Checklist
- [ ] `POST /auth/login` — form with `username`, `password`. Store `access_token` in the existing cookie (`TOKEN_COOKIE` in `api.ts`), matching what's already wired.
- [ ] `GET /auth/me` on load / after login to populate the current user (id, role, name) for role-gated UI.
- [ ] **Delete the `signup` page** and any link to it — `POST /auth/register` does not exist and will not. Point account creation at admin provisioning instead.
- [ ] **Keep** `forgot-password`, `reset-password` and `verify-otp` and verify each against its real endpoint above. These were previously listed for deletion; that instruction is withdrawn.
- [ ] Update `UserRole` type to `"admin" | "clinician"` only (matches `backend/app/models/user.py:UserRole`). Remove `"doctor"`, `"receptionist"`, `"researcher"`.
- [ ] 401 handling already exists in `api.ts`'s response interceptor (redirects to `/login`) — keep it, verify it still fires against the real `/auth/me`/token-expiry behavior.
- [ ] Decide (product question, not yours to invent): does the demo need an ADMIN-only "create clinician" screen against `POST /admin/users`? Not required by PRD §8's acceptance journey — only needed if there's no other way to get a demo clinician account. Confirm before building it.

---

## 1A. Triage queue — the dashboard (ADR-006 decision 7)

**Backend reality** ([backend/app/api/v1/triage.py](../backend/app/api/v1/triage.py), [backend/app/schemas/triage.py](../backend/app/schemas/triage.py)):

| Endpoint | Method | Returns |
|---|---|---|
| `/api/v1/triage` | GET (`page`, `page_size`<=100) | `TriageListResponse` — paginated, ranked |

The route is deliberately not called `/dashboard`. It replaces stat tiles with a ranked queue, and the entries carry booleans rather than numbers on purpose: an aggregate confidence average across patients is clinically meaningless and is a step back toward the framing FR-04 forbids.

```ts
interface TriageEntry {
  patient_id: string;
  patient_first_name: string;
  patient_last_name?: string | null;

  // Ranked in exactly this order. Render the reason a row is high in the
  // queue, not a score.
  has_open_early_watch: boolean;
  has_worsening_trend: boolean;
  awaiting_sign_off: boolean;

  latest_visit_id?: string | null;
  latest_analysis_id?: string | null;
  latest_analysis_generated_at?: string | null;
}
```

### Checklist
- [ ] Replace `dashboard/page.tsx` wholesale. The hardcoded `PATIENTS` array, the stat-tile row, the `Critical`/`Stable`/`Monitoring`/`Reviewing` vocabulary and the scan-volume chart all go — none has any backing in the API.
- [ ] Render the queue in server order. Do not re-sort client-side; the ordering is the clinical judgment the endpoint exists to express.
- [ ] Show *why* each row is ranked where it is, from the three booleans. No composite score, no percentage.
- [ ] Empty state: a clinician with no patients gets a real empty state, not a zeroed tile row.
- [ ] Each row links to the patient (§2) and, where present, the latest analysis (§4).

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

## 3A. Scan intake (ADR-006 decisions 1, 2, 5)

**Backend reality** ([backend/app/api/v1/visits.py](../backend/app/api/v1/visits.py), [backend/app/schemas/scan.py](../backend/app/schemas/scan.py), [backend/app/services/scan_service.py](../backend/app/services/scan_service.py)):

| Endpoint | Method | Notes |
|---|---|---|
| `/api/v1/visits/{visit_id}/scan` | POST | `multipart/form-data`, single `file` field. 201 `ScanResponse`. **One scan per visit.** |
| `/api/v1/visits/{visit_id}/scan` | GET | `ScanResponse`, 404 before a scan is attached |

The scan attaches to a **visit**, not a patient. A returning patient's follow-up scan is a new visit, not a replacement of the existing one — that is what makes cross-visit comparison possible, and it is the whole basis of the trend story. Upload size is capped by `MAX_SCAN_SIZE_BYTES` (200 MB by default).

The bytes live in file storage, not the database. `storage_key` is deliberately absent from the wire schema: it is an internal reference and exposing it would leak filesystem layout.

```ts
interface ScanResponse {
  id: string;
  visit_id: string;
  uploaded_by_id: string;
  original_filename: string;
  content_type: string;
  size_bytes: number;
  checksum: string;
  dimensions: Record<string, unknown>;  // shape depends on what was parsed
  uploaded_at: string;
  created_at: string;
  updated_at: string;
  // no storage_key, by design
}
```

### Checklist
- [ ] Rebuild the scan upload as part of the **new visit** flow (§3), not patient creation. The existing [`dashboard/upload/page.tsx`](../frontend/src/app/dashboard/upload/page.tsx) posts `mri_scan`, `mmse_score` and `family_history` as multipart to `POST /patients`, which accepts `PatientCreate` JSON — it cannot ever have worked, and its comment describes a pipeline contract that does not exist. Rebuild, do not adapt.
- [ ] `mri-dropzone.tsx` is reusable as a file input. What is around it is not.
- [ ] Upload progress and a clear failure state. A 200 MB cap means slow uploads are normal, not a hang.
- [ ] Show the scan as attached evidence on the visit (filename, size, uploaded time). Do not render the checksum as though it meant something clinical.
- [ ] Do not build a re-upload/replace control on an existing visit. One scan per visit is a modelling decision, not a limitation to work around.

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
  pipeline_note: string;   // e.g. "pipeline complete, live model reasoning, evidence retrieval simulated" — show this prominently
  disclaimer: string;      // show this prominently, always
  generated_at: string;
  findings: FindingResponse[];

  // Clinician sign-off (ADR-006 decision 6). Null until POST /analyses/{id}/review.
  // Report generation is gated on these being set — see §5.
  reviewed_by_id?: string | null;
  reviewed_at?: string | null;

  created_at: string;
  updated_at: string;
  // context_snapshot is intentionally NOT on the wire — don't expect it
}
```

### Checklist
- [ ] "Run analysis" action on a case (POST with default/optional `history_limit`), with a loading state — this can take a moment and any AI/RAG failure is a controlled 502 (see error mapping in §6), not a silent failure.
- [ ] Differential diagnosis review screen ("Clinician Review" step of PRD §8): ranked findings, each showing `name`, `category`, `likelihood_band` (not the raw `confidence` float as a headline number), `explanation`, supporting/contradicting findings, and evidence with citations. `explanation` is present on `FindingResponse` and is included in the type above.
- [ ] **Visually separate `trend_basis` from `evidence`** in the finding card — e.g., a distinct "Patient History" panel vs. an "External Evidence / Citations" panel. This is not a styling nicety; AGENTS.md §8.2 treats conflating them as a contract violation.
- [ ] `provider_mode`/`pipeline_note` must be visible on every analysis view — this is how a clinician (and a demo audience) can tell simulated evidence from live evidence. Don't hide it in a tooltip.
- [ ] `disclaimer` must be visible on every analysis view, not just in the eventual PDF.
- [ ] Never use "diagnosis," "confirmed," "certainty," or treatment language anywhere in the UI copy around this data — mirror the vocabulary the backend already enforces (`AGENTS.md` §8.2, §15 Clinical Safety).
- [ ] Analysis history for a case (list of past runs) so a clinician can see prior differentials, not just the latest.
- [ ] **A stage estimate is never a headline.** `CN / MCI / Mild / Moderate / Severe` may appear only as the top-ranked candidate inside the ranked differential, with its likelihood band, contradicting findings and citations attached (ADR-006 decision 3). The single stage badge and `stageLabel` headline in [`patients/[id]/page.tsx`](../frontend/src/app/dashboard/patients/[id]/page.tsx) are exactly the framing this forbids and must go.
- [ ] **Never display a confidence above 92%.** `MAX_CONFIDENCE` is 0.92 and is enforced server-side precisely so output cannot express certainty. The audited dashboard displayed 96% and 97%; those numbers were fabricated.
- [ ] The word "certainty" does not appear in UI copy. Neither does "diagnosis", "confirmed", or treatment language.
- [ ] Sign-off action on this screen: `POST /analyses/{analysis_id}/review`, **no request body**, returns the updated `AnalysisResponse` with `reviewed_by_id`/`reviewed_at` populated. Show clearly whether an analysis is signed off and by whom — the report button depends on it (§5).
- [ ] Staging inputs (`imaging`, `scan_trend`) are internal to the pipeline and are **not** on the wire. Do not expect a region-attribution payload; the contributing-region bars in the current UI are not backed by anything the API returns.

---

## 5. Clinician Sign-off → PDF Report

**Backend reality** ([backend/app/api/v1/analysis.py](../backend/app/api/v1/analysis.py) for the nested create/list, [backend/app/api/v1/reports.py](../backend/app/api/v1/reports.py) for item reads/download, [backend/app/schemas/report.py](../backend/app/schemas/report.py)):

| Endpoint | Method | Notes |
|---|---|---|
| `/api/v1/analyses/{analysis_id}/reports` | POST | No request body. **Gated on clinician sign-off:** 409 `error_code: "analysis_not_reviewed"` if `reviewed_at` is null (ADR-006 decision 6). Otherwise builds a snapshot, proves it renders, persists metadata, 201 `ReportResponse`. Renders **before** persisting — a render failure is a 500 with `error_code: "report_render_error"` and nothing is saved. |
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
- [ ] **Disable it until the analysis is signed off**, and say why. An unreviewed analysis returns 409 `analysis_not_reviewed`; surfacing that as a generic failure would make the sign-off gate look like a bug rather than the safety boundary it is. Sign-off is the step that makes "a clinician reviewed it" structural instead of a disclaimer.
- [ ] The provenance line (`pipeline_note`) travels into the PDF. Do not present the download as validated clinical output.
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

`extractApiError` in `api.ts` reads `message` first and falls back to `detail` only for responses that never entered the application, such as Starlette's own 404 for an unrouted path. An earlier edition of this document flagged it as reading `.detail` and needing a fix; that has been done and the instruction is withdrawn.

| HTTP | Meaning here | UI treatment |
|---|---|---|
| 401 | Expired/invalid token | Already handled: redirect to `/login` (verify it still works against the real flow). |
| 403 | Wrong role for an admin-only action | Show a permission message; don't offer a retry. |
| 404 | Entity missing **or** owned by another clinician (ADR-001/002/004 all mask this identically) | Show "not found," never imply "you don't have permission" — the backend deliberately hides which case it is. |
| 422 | Validation failure | `details` carries per-field pydantic errors — surface them against form fields where practical, not just a toast. |
| 409 | Report requested for an analysis that has not been signed off (`error_code: "analysis_not_reviewed"`) | Not an error state to apologise for — it means the sign-off step has not happened. Point the clinician at it. Better still, disable the control so this is unreachable (§5). |
| 502 | AI/RAG pipeline failure (`error_code`: `ai_error`, `rag_error`, `rag_no_evidence`, `ai_contract_error`, `ai_no_candidates`) | The clinical record is guaranteed untouched (AGENTS.md §8.5) — message should invite retry, not suggest data was lost. |
| 500 | Report render failure (`error_code: "report_render_error"`) or truly unexpected | Retry-safe for the render case; generic error otherwise. |

### Checklist
- [ ] A shared "empty analysis" state (case exists, no analysis run yet) distinct from "loading" and "error".
- [ ] A shared 404 component used identically for patient/visit/analysis/report — don't let any of them leak more detail than the backend already chose to hide.

---

## 7. Explicit non-goals (do not build these)

Re-checked against the current backend. Three entries in the previous edition of this list are now **wrong and have been removed**: MRI upload, the sign-off workflow, and password-reset UI are all in scope and all backed by real endpoints. What remains:

- No **uploaded diagnostic-report** analysis. ADR-006 admitted MRI and only MRI; it is not a precedent for the other exclusions.
- No treatment recommendations, autonomous-diagnosis framing, or "confirmed diagnosis" language.
- No lone stage verdict. A stage estimate is the top-ranked candidate in a ranked differential or it does not ship (§4).
- No RECEPTIONIST role UI.
- No self-service signup — `POST /auth/register` is removed and guarded by a regression test.
- No region-attribution, segmentation or longitudinal-registration UI. ADR-006 names these as adjacent, individually reasonable, and collectively a different project.
- No aggregate stat tiles on the queue (§1A).

---

## 8. Suggested build order (mirrors the dependency chain, not equal-sized steps)

1. Confirm `login`/`me` against the real contract; delete the `signup` page; keep and verify the OTP and reset pages (§1).
2. Types file rewrite (`types.ts`) against §1A-§5 above, in full, before any page work — every page below depends on this being right once. Generating them from the live `openapi.json` (see `scripts/dump_backend_routes.py`) beats hand-writing them.
3. Triage queue replacing the dashboard (§1A). First screen that shows real data, and the one the demo opens on. Needs seed data covering more than one patient first.
4. Patient list/create/detail (§2).
5. Visit creation + symptom entry + scan upload, including the history view (§3, §3A) — history is required before analysis can demonstrate `early_watch`.
6. Analysis trigger + review screen + sign-off (§4) — the highest-value screen for the demo; get the `trend_basis`/`evidence` visual separation and the stage-as-candidate framing right here.
7. Report generation + download (§5).
8. Delete the old `upload/page.tsx` at whatever point step 5 replaces it. Do not ship with it linked from navigation at any point — it 422s on every submission.

---

## 9. Verification before calling REPORT-01D done

- [ ] Frontend production build passes.
- [ ] Manual browser run of the full journey as ADR-006 revised it: login → triage queue → patient → visit with scan + symptoms → 2+ visits so `early_watch` has a real trend → run analysis → review ranked differential with `trend_basis` and `evidence` visually separated → sign off → generate report → download and open the PDF.
- [ ] No hardcoded clinical data anywhere in the frontend.
- [ ] No stage badge, "certainty" copy, confidence above 92%, or `Critical`/`Stable` vocabulary rendering anywhere.
- [ ] `provider_mode`, `pipeline_note` and `disclaimer` visible on every analysis view.
- [ ] The report control is unreachable for an analysis that has not been signed off.
- [ ] A second clinician account cannot see the first clinician's patients/visits/scans/analyses/reports through the UI (matches the backend's 404 masking).
