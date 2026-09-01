export type DiseaseLabel = "healthy" | "alzheimers" | "parkinsons";

export type DiseaseStage =
  | "CN" // cognitively normal
  | "MCI" // mild cognitive impairment
  | "MILD"
  | "MODERATE"
  | "SEVERE";

export interface User {
  id: string;
  full_name: string;
  email: string;
  role: "doctor" | "researcher" | "admin";
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
  contribution: number; // 0-1, how much this region influenced the prediction
}

export interface PredictionResult {
  id: string;
  patient_id: string;
  label: DiseaseLabel;
  stage: DiseaseStage;
  confidence: number; // 0-1
  regions: PredictionRegion[];
  heatmap_url: string | null;
  created_at: string;
}

export interface ApiError {
  detail: string;
}
