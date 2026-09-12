/**
 * Every call the app makes to the backend, in one file.
 *
 * Components and hooks import from here rather than reaching for `api` and a
 * string path, so the set of endpoints the frontend depends on can be read
 * against `backend-routes.json` without grepping the whole tree.
 */
import { api } from "@/lib/api";
import type {
  Analysis,
  Paginated,
  Patient,
  PatientCreate,
  PatientUpdate,
  Report,
  Scan,
  Symptom,
  SymptomCreate,
  TriageEntry,
  User,
  Token,
  Visit,
  VisitCreate,
  VisitHistory,
  VisitStatus,
} from "@/lib/types";

export interface PageParams {
  page?: number;
  page_size?: number;
}

/* -- auth ------------------------------------------------------------- */

export const auth = {
  login: (username: string, password: string) =>
    api.post<Token>("/auth/login", { username, password }).then((r) => r.data),

  requestOtp: (email: string) =>
    api.post("/auth/request-otp", { email }).then((r) => r.data),

  verifyOtp: (email: string, otp: string, password: string) =>
    api
      .post<Token>("/auth/verify-otp", { email, otp, password })
      .then((r) => r.data),

  forgotPassword: (email: string) =>
    api.post("/auth/forgot-password", { email }).then((r) => r.data),

  resetPassword: (email: string, otp: string, new_password: string) =>
    api
      .post("/auth/reset-password", { email, otp, new_password })
      .then((r) => r.data),

  me: () => api.get<User>("/auth/me").then((r) => r.data),
};

/* -- triage ----------------------------------------------------------- */

export const triage = {
  /** The ranked queue the dashboard is built around (ADR-006). */
  list: (params: PageParams = {}) =>
    api
      .get<Paginated<TriageEntry>>("/triage", { params })
      .then((r) => r.data),
};

/* -- patients --------------------------------------------------------- */

export const patients = {
  list: (params: PageParams & { doctor_id?: string } = {}) =>
    api.get<Paginated<Patient>>("/patients", { params }).then((r) => r.data),

  /** Server-side search. An empty `q` returns the unfiltered page. */
  search: (q: string, params: PageParams = {}) =>
    api
      .get<Paginated<Patient>>("/patients/search", { params: { q, ...params } })
      .then((r) => r.data),

  get: (patientId: string) =>
    api.get<Patient>(`/patients/${patientId}`).then((r) => r.data),

  create: (body: PatientCreate) =>
    api.post<Patient>("/patients", body).then((r) => r.data),

  update: (patientId: string, body: PatientUpdate) =>
    api.patch<Patient>(`/patients/${patientId}`, body).then((r) => r.data),

  remove: (patientId: string) =>
    api.delete(`/patients/${patientId}`).then((r) => r.data),

  visits: (patientId: string, params: PageParams & { status?: VisitStatus } = {}) =>
    api
      .get<Paginated<Visit>>(`/patients/${patientId}/visits`, { params })
      .then((r) => r.data),

  createVisit: (patientId: string, body: VisitCreate) =>
    api
      .post<Visit>(`/patients/${patientId}/visits`, body)
      .then((r) => r.data),

  /** Prior visits, as the AI pipeline sees them when building a trend. */
  history: (
    patientId: string,
    params: { limit?: number; order?: "asc" | "desc"; exclude_visit_id?: string } = {}
  ) =>
    api
      .get<VisitHistory>(`/patients/${patientId}/visits/history`, { params })
      .then((r) => r.data),
};

/* -- visits ----------------------------------------------------------- */

export const visits = {
  get: (visitId: string) =>
    api.get<Visit>(`/visits/${visitId}`).then((r) => r.data),

  update: (visitId: string, body: Partial<VisitCreate>) =>
    api.patch<Visit>(`/visits/${visitId}`, body).then((r) => r.data),

  remove: (visitId: string) =>
    api.delete(`/visits/${visitId}`).then((r) => r.data),

  getScan: (visitId: string) =>
    api.get<Scan>(`/visits/${visitId}/scan`).then((r) => r.data),

  uploadScan: (visitId: string, file: File, onProgress?: (pct: number) => void) => {
    const form = new FormData();
    form.append("file", file);
    return api
      .post<Scan>(`/visits/${visitId}/scan`, form, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (e) => {
          if (onProgress && e.total) {
            onProgress(Math.round((e.loaded / e.total) * 100));
          }
        },
      })
      .then((r) => r.data);
  },

  symptoms: (visitId: string, params: PageParams = {}) =>
    api
      .get<Paginated<Symptom>>(`/visits/${visitId}/symptoms`, { params })
      .then((r) => r.data),

  addSymptom: (visitId: string, body: SymptomCreate) =>
    api
      .post<Symptom>(`/visits/${visitId}/symptoms`, body)
      .then((r) => r.data),

  updateSymptom: (visitId: string, symptomId: string, body: Partial<SymptomCreate>) =>
    api
      .patch<Symptom>(`/visits/${visitId}/symptoms/${symptomId}`, body)
      .then((r) => r.data),

  removeSymptom: (visitId: string, symptomId: string) =>
    api.delete(`/visits/${visitId}/symptoms/${symptomId}`).then((r) => r.data),

  analyses: (visitId: string, params: PageParams = {}) =>
    api
      .get<Paginated<Analysis>>(`/visits/${visitId}/analyses`, { params })
      .then((r) => r.data),

  latestAnalysis: (visitId: string) =>
    api
      .get<Analysis>(`/visits/${visitId}/analyses/latest`)
      .then((r) => r.data),

  /** Kicks off the pipeline. `history_limit` caps the prior visits it reads. */
  runAnalysis: (visitId: string, history_limit?: number) =>
    api
      .post<Analysis>(`/visits/${visitId}/analyses`, { history_limit })
      .then((r) => r.data),
};

/* -- analyses & reports ----------------------------------------------- */

export const analyses = {
  get: (analysisId: string) =>
    api.get<Analysis>(`/analyses/${analysisId}`).then((r) => r.data),

  /** Clinician sign-off. Gates report generation (ADR-006, Decision 6). */
  signOff: (analysisId: string) =>
    api
      .post<Analysis>(`/analyses/${analysisId}/review`)
      .then((r) => r.data),

  reports: (analysisId: string, params: PageParams = {}) =>
    api
      .get<Paginated<Report>>(`/analyses/${analysisId}/reports`, { params })
      .then((r) => r.data),

  createReport: (analysisId: string) =>
    api
      .post<Report>(`/analyses/${analysisId}/reports`)
      .then((r) => r.data),
};

export const reports = {
  get: (reportId: string) =>
    api.get<Report>(`/reports/${reportId}`).then((r) => r.data),

  /** Returns the PDF bytes; the caller is responsible for the object URL. */
  downloadPdf: (reportId: string) =>
    api
      .get<Blob>(`/reports/${reportId}/pdf`, { responseType: "blob" })
      .then((r) => r.data),
};
