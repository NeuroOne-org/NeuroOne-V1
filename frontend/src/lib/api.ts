import axios, { AxiosError } from "axios";

// TEMPORARY: with no NEXT_PUBLIC_API_URL, target port 8000 on whatever host
// the page was opened on (localhost, 127.0.0.1, a LAN IP). The session
// cookie is SameSite=Strict, so the API must share the page's host.
const defaultApiUrl =
  typeof window !== "undefined"
    ? `${window.location.protocol}//${window.location.hostname}:8000/api/v1`
    : "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL ?? defaultApiUrl,
  // Sends the HttpOnly session cookie the backend set at sign-in. This code
  // never handles the token itself (see lib/session.ts).
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
    // The backend refuses cookie-authenticated writes without it: a
    // cross-site form cannot add a custom header, so it marks the request
    // as coming from this app rather than from a forged submission.
    "X-Requested-With": "XMLHttpRequest",
  },
});

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // The backend already cleared a rejected session cookie on this 401, so
    // proxy.ts will not bounce /login straight back to the dashboard.
    if (error.response?.status === 401 && typeof window !== "undefined") {
      if (!window.location.pathname.startsWith("/login")) {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export function extractApiError(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data as
      | { message?: string; detail?: unknown }
      | undefined;

    // Every error this API raises goes through the centralised envelope in
    // backend/app/utils/handlers.py, which carries the readable text in
    // `message` -- FastAPI's own validation errors included.
    if (typeof data?.message === "string" && data.message) return data.message;

    // Reached only for responses that never entered the app, such as
    // Starlette's default 404 for an unrouted path.
    if (typeof data?.detail === "string" && data.detail) return data.detail;

    if (error.message === "Network Error") {
      return "Can't reach the server. Check that the backend is running.";
    }
  }
  return "Something went wrong. Please try again.";
}
