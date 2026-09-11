/**
 * API client for communicating with the NeuroOne backend.
 * Handles authentication, error extraction, and request/response formatting.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface ApiResponse<T = unknown> {
  data?: T;
  error?: string;
  detail?: string | { msg?: string };
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface OtpResponse {
  message: string;
}

export interface OtpVerifyResponse {
  access_token: string;
  token_type: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    // Add auth token if available
    const token = this.getToken();
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiError(
        extractApiError(errorData) || `HTTP ${response.status}`,
        response.status,
        errorData
      );
    }

    return response.json() as Promise<T>;
  }

  async post<T>(
    endpoint: string,
    data?: unknown,
    options?: RequestInit
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: "POST",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async get<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: "GET",
    });
  }

  private getToken(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("auth_token");
  }

  setToken(token: string): void {
    if (typeof window === "undefined") return;
    localStorage.setItem("auth_token", token);
  }

  clearToken(): void {
    if (typeof window === "undefined") return;
    localStorage.removeItem("auth_token");
  }
}

class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public response: unknown
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * Extract a user-friendly error message from various API response formats.
 */
export function extractApiError(errorData: unknown): string {
  if (!errorData || typeof errorData !== "object") {
    return "An error occurred. Please try again.";
  }

  const data = errorData as Record<string, unknown>;

  // Handle FastAPI ValidationError
  if (Array.isArray(data.detail) && data.detail[0]?.msg) {
    return data.detail[0].msg;
  }

  // Handle custom error message
  if (typeof data.detail === "string") {
    return data.detail;
  }

  if (typeof data.message === "string") {
    return data.message;
  }

  if (typeof data.error === "string") {
    return data.error;
  }

  return "An error occurred. Please try again.";
}

// Export singleton instance
export const api = new ApiClient();
