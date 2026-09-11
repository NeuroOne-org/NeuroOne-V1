"use client";

import { useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import { Eye, EyeOff, Loader2, Mail } from "lucide-react";
import { api, extractApiError } from "@/lib/api";
import { loginSchema } from "@/lib/validation";

// This isolated preview hands account flows back to the existing frontend.
const existingAppUrl = process.env.NEXT_PUBLIC_EXISTING_APP_URL ?? "http://localhost:3000";

export function LoginForm() {
  const params = useSearchParams();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<{ email?: string; password?: string }>({});
  const [formError, setFormError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (isSubmitting) return;
    setFormError(null);
    const result = loginSchema.safeParse({ email, password });
    if (!result.success) {
      const errors: { email?: string; password?: string } = {};
      for (const issue of result.error.issues) {
        const key = issue.path[0] as "email" | "password";
        if (!errors[key]) errors[key] = issue.message;
      }
      setFieldErrors(errors);
      (errors.email ? emailRef : passwordRef).current?.focus();
      return;
    }
    setFieldErrors({});
    setIsSubmitting(true);
    try {
      // Same payload as AuthProvider.login; OTP/session ownership stays in the existing app.
      await api.post("/auth/login", { username: result.data.email, password: result.data.password });
      const requestedNext = params.get("next");
      const next = requestedNext?.startsWith("/") && !requestedNext.startsWith("//") && !requestedNext.includes("\\")
        ? requestedNext : "/dashboard";
      const destination = new URL("/verify-otp", existingAppUrl);
      destination.searchParams.set("username", email);
      destination.searchParams.set("next", next);
      window.location.assign(destination.href);
    } catch (error) {
      setFormError(extractApiError(error));
      setIsSubmitting(false);
    }
  }

  return (
    <>
      <form id="login-form" onSubmit={handleSubmit} noValidate aria-busy={isSubmitting}>
        <div>
          <label htmlFor="email" className="login-label">Email</label>
          <input ref={emailRef} id="email" name="email" type="email" autoComplete="username" autoCapitalize="none" spellCheck={false} required
            className="login-input" placeholder="Enter your email address" value={email}
            onChange={(event) => setEmail(event.target.value)} aria-invalid={!!fieldErrors.email}
            aria-describedby={fieldErrors.email ? "email-error" : undefined} />
          {fieldErrors.email && <p id="email-error" className="login-error" role="alert">{fieldErrors.email}</p>}
        </div>
        <div className="mt-5">
          <label htmlFor="password" className="login-label">Password</label>
          <div className="relative">
            <input ref={passwordRef} id="password" name="password" type={showPassword ? "text" : "password"} autoComplete="current-password" required
              className="login-input pr-12" placeholder="Enter your password" value={password}
              onChange={(event) => setPassword(event.target.value)} aria-invalid={!!fieldErrors.password}
              aria-describedby={fieldErrors.password ? "password-error" : undefined} />
            <button type="button" onClick={() => setShowPassword(!showPassword)}
              aria-label={showPassword ? "Hide password" : "Show password"} aria-pressed={showPassword}
              className="password-toggle absolute right-0 top-0 flex h-12 w-12 items-center justify-center rounded text-product-ink-soft">
              {showPassword ? <EyeOff size={18} aria-hidden="true" /> : <Eye size={18} aria-hidden="true" />}
            </button>
          </div>
          {fieldErrors.password && <p id="password-error" className="login-error" role="alert">{fieldErrors.password}</p>}
        </div>
        <div className="my-3 flex items-center justify-between gap-2 text-[13px] font-medium leading-5">
          <label className="flex min-h-11 items-center gap-2 text-product-ink-soft" title="Remember me is not available yet">
            {/* No persistence option exists in the current auth contract. */}
            <input type="checkbox" name="remember-me" checked={false} disabled
              aria-describedby="remember-me-help"
              className="h-4 w-4 shrink-0 cursor-not-allowed accent-product-primary" />
            Remember me
            <span id="remember-me-help" className="sr-only">Remember me is not available yet.</span>
          </label>
          <a className="login-link inline-flex min-h-11 items-center" href={new URL("/forgot-password", existingAppUrl).href}>Forgot password?</a>
        </div>
        {formError && <p className="mb-4 rounded border border-product-border bg-product-bg px-3 py-2 text-[13px] leading-5" role="alert">{formError}</p>}
        <button type="submit" className="login-button login-primary" disabled={isSubmitting}>
          {isSubmitting && <Loader2 size={18} className="animate-spin motion-reduce:animate-none" aria-hidden="true" />}
          {isSubmitting ? "Logging in…" : "Log In"}
        </button>
      </form>
      <div className="my-6 flex items-center gap-4 text-[13px] font-medium leading-5 text-product-ink-soft">
        <span className="h-px flex-1 bg-product-border" aria-hidden="true" />
        Or, Login with
        <span className="h-px flex-1 bg-product-border" aria-hidden="true" />
      </div>
      <button type="submit" form="login-form" className="login-button login-secondary" disabled={isSubmitting}>
        {isSubmitting
          ? <Loader2 size={18} className="animate-spin motion-reduce:animate-none" aria-hidden="true" />
          : <Mail size={18} aria-hidden="true" />}
        {isSubmitting ? "Sending code…" : "Sign in via OTP"}
      </button>
    </>
  );
}
