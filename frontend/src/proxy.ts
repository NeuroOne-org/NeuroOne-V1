import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { SESSION_COOKIE, isProtectedPath } from "@/lib/session";

const AUTH_PAGES = ["/login", "/verify-otp"];

// Presence only: the backend validates the token on every API call. This runs
// on the frontend's host, so it sees the cookie only when the API shares that
// host -- true for localhost:3000 and localhost:8000, since cookies are not
// scoped by port, and for a deployment that serves the API under the same
// domain.
export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get(SESSION_COOKIE)?.value;

  if (pathname === "/") {
    if (token) {
      const url = request.nextUrl.clone();
      url.pathname = "/dashboard";
      return NextResponse.redirect(url);
    }
    return NextResponse.next();
  }

  const isProtected = isProtectedPath(pathname);
  const isAuthPage = AUTH_PAGES.some((p) => pathname.startsWith(p));

  if (isProtected && !token) {
    const url = request.nextUrl.clone();
    url.pathname = "/login";
    url.searchParams.set("next", pathname);
    return NextResponse.redirect(url);
  }

  if (isAuthPage && token) {
    const url = request.nextUrl.clone();
    url.pathname = "/dashboard";
    url.search = "";
    return NextResponse.redirect(url);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/", "/dashboard/:path*", "/login", "/verify-otp"],
};
