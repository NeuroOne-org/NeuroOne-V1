/**
 * Wire types for the NeuroOne API.
 *
 * These mirror `backend-routes.json` (the generated OpenAPI contract) rather
 * than any UI convenience shape. When a field is optional here it is because
 * the backend marks it optional, so the UI has to render the missing case.
 *
 * The domain is Patient -> Visit -> (Scan, Symptoms) -> Analysis -> Report.
 * There is no "prediction attached to a patient": a patient has visits, and a
 * visit is what gets analysed.
 */

/* -- primitives ------------------------------------------------------- */

export interface Pagination {
  page: number;
  page_size: number;
  total_pages: number;
  total_records: number;
}

export interface Paginated<T> {
  items: T[];
  pagination: Pagination;
}

export interface PhoneNumber {
  phone_number: string;
}

/* -- auth ------------------------------------------------------------- */

export type UserRole = "admin" | "clinician";

export interface User {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

/* -- patients --------------------------------------------------------- */

export interface Patient {
  id: string;
  first_name: string;
  last_name: string | null;
  dob: string;
  gender: string;
  email: string;
  phone: PhoneNumber[];
  address: string;
  blood_group: string;
  allergies: string[];
  emergency_contact: string;
  doctor_id: string;
  doctor: User;
  created_at: string;
  updated_at: string;
}

export interface PatientCreate {
  first_name: string;
  last_name?: string | null;
  dob: string;
  gender: string;
  email: string;
  phone: PhoneNumber[];
  address: string;
  blood_group: string;
  allergies: string[];
  emergency_contact: string;
  doctor_id?: string | null;
}

export type PatientUpdate = Partial<PatientCreate>;

/* -- visits ----------------------------------------------------------- */

/** ANALYZED is written by the AI pipeline, never through the visits API. */
export type VisitStatus = "draft" | "submitted" | "analyzed" | "closed";

export type SymptomOnset =
  | "sudden"
  | "subacute"
  | "gradual"
  | "insidious"
  | "unknown";

export interface Vitals {
  bp_systolic?: number | null;
  bp_diastolic?: number | null;
  heart_rate?: number | null;
  respiratory_rate?: number | null;
  temperature_c?: number | null;
  spo2?: number | null;
  height_cm?: number | null;
  weight_kg?: number | null;
}

export interface Symptom {
  id: string;
  visit_id: string;
  symptom_name: string;
  severity: number;
  onset?: SymptomOnset | null;
  duration_days?: number | null;
  observation?: string | null;
  created_at: string;
  updated_at: string;
}

export interface SymptomCreate {
  symptom_name: string;
  severity: number;
  onset?: SymptomOnset | null;
  duration_days?: number | null;
  observation?: string | null;
}

export interface Visit {
  id: string;
  patient_id: string;
  chief_complaint: string;
  visit_date: string;
  status: VisitStatus;
  history?: string | null;
  notes?: string | null;
  vitals?: Vitals;
  symptoms?: Symptom[];
  created_at: string;
  updated_at: string;
}

export interface VisitCreate {
  chief_complaint: string;
  visit_date?: string | null;
  status?: VisitStatus | null;
  history?: string | null;
  notes?: string | null;
  vitals?: Vitals;
  symptoms?: SymptomCreate[];
}

export interface VisitHistory {
  patient_id: string;
  order: "asc" | "desc";
  total_visits: number;
  returned: number;
  visits: Visit[];
}

/* -- scans ------------------------------------------------------------ */

export interface Scan {
  id: string;
  visit_id: string;
  original_filename: string;
  content_type: string;
  size_bytes: number;
  checksum: string;
  dimensions?: Record<string, unknown>;
  uploaded_at: string;
  uploaded_by_id: string;
  created_at: string;
  updated_at: string;
}

/* -- analyses --------------------------------------------------------- */

export type FindingCategory = "differential_diagnosis" | "early_watch";
export type LikelihoodBand = "low" | "moderate" | "high";

export interface Evidence {
  citation: string;
  source: string;
  relevant_passage: string;
  source_url?: string | null;
  source_tier?: string | null;
  published_year?: number | null;
  relevance_score?: number | null;
  document_id?: string | null;
  chunk_id?: string | null;
}

export interface Finding {
  id: string;
  rank: number;
  name: string;
  category: FindingCategory;
  confidence: number;
  likelihood_band: LikelihoodBand;
  explanation: string;
  supporting_findings: string[];
  contradicting_findings: string[];
  evidence?: Evidence[];
  trend_basis?: Record<string, unknown>[];
}

export interface Analysis {
  id: string;
  visit_id: string;
  model_name: string;
  provider_mode: string;
  pipeline_note: string;
  disclaimer: string;
  findings?: Finding[];
  generated_at: string;
  /** Null until a clinician signs off via POST /analyses/{id}/review. */
  reviewed_at?: string | null;
  reviewed_by_id?: string | null;
  created_at: string;
  updated_at: string;
}

/* -- reports ---------------------------------------------------------- */

export interface Report {
  id: string;
  analysis_id: string;
  filename: string;
  generated_at: string;
  generated_by_id: string;
  created_at: string;
  updated_at: string;
}

/* -- triage ----------------------------------------------------------- */

/**
 * One row of the ranked queue. The three booleans are the whole ranking
 * signal — the backend does not send a score, so the UI derives urgency
 * from the flags rather than inventing a number.
 */
export interface TriageEntry {
  patient_id: string;
  patient_first_name: string;
  patient_last_name?: string | null;
  latest_visit_id?: string | null;
  latest_analysis_id?: string | null;
  latest_analysis_generated_at?: string | null;
  awaiting_sign_off: boolean;
  has_open_early_watch: boolean;
  has_worsening_trend: boolean;
}
