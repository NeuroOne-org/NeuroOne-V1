export type DiseaseLabel = "healthy" | "alzheimers" | "parkinsons";

export type DiseaseStage =
  | "CN"
  | "MCI"
  | "MILD"
  | "MODERATE"
  | "SEVERE";

export type UserRole = "doctor" | "admin" | "receptionist" | "researcher";

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

export interface AuthTokens {
  access_token: string;
  token_type: string;
}

export interface Patient {
  id: string;
  full_name: string;
  age: number;
  gender: "male" | "female" | "other";
  mmse_score: number | null;
  family_history: boolean;
  notes: string | null;
  created_at: string;
  latest_result?: PredictionResult | null;
}

export interface PredictionRegion {
  label: string;
  contribution: number;
}

export interface PredictionResult {
  id: string;
  patient_id: string;
  label: DiseaseLabel;
  stage: DiseaseStage;
  confidence: number;
  regions: PredictionRegion[];
  heatmap_url: string | null;
  created_at: string;
}

export interface ApiError {
  detail: string;
}