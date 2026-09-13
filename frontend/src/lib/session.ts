/**
 * The browser session, as far as the frontend can see it.
 *
 * The access token lives in an HttpOnly cookie that the backend sets on
 * sign-in and clears on sign-out or rejection (backend/app/core/session.py).
 * Page scripts cannot read it -- that is the point, so an XSS payload cannot
 * steal it -- which leaves proxy.ts, running on the server, as the only code
 * here that checks whether it is present.
 */
export const SESSION_COOKIE = "neuroone_session";

export const PROTECTED_PREFIXES = ["/dashboard"];

export function isProtectedPath(pathname: string): boolean {
  return PROTECTED_PREFIXES.some((prefix) => pathname.startsWith(prefix));
}
