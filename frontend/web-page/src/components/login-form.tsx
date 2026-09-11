"use client";

import { useRef, useState } from "react";
import { Eye, EyeOff, Loader2, Mail, ArrowLeft } from "lucide-react";
import { api, extractApiError } from "@/lib/api";
import { loginSchema, otpSchema } from "@/lib/validation";

type LoginFlowStep = "initial" | "otp-sent" | "otp-verify";

export function LoginForm() {
  const [step, setStep] = useState<LoginFlowStep>("initial");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [formError, setFormError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);
  const otpRef = useRef<HTMLInputElement>(null);

  const resetState = () => {
    setFieldErrors({});
    setFormError(null);
  };

  async function handleDirectLogin(event: React.FormEvent) {
    event.preventDefault();
    if (isSubmitting) return;
    resetState();

    const result = loginSchema.safeParse({ email, password });
    if (!result.success) {
      const errors: Record<string, string> = {};
      for (const issue of result.error.issues) {
        const key = issue.path[0] as string;
        if (!errors[key]) errors[key] = issue.message;
      }
      setFieldErrors(errors);
      (errors.email ? emailRef : passwordRef).current?.focus();
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await api.post<{ access_token: string }>(
        "/auth/login",
        { username: result.data.email, password: result.data.password }
      );
      api.setToken(response.access_token);
      window.location.href = "/dashboard";
    } catch (error) {
      setFormError(extractApiError(error));
      setIsSubmitting(false);
    }
  }

  async function handleRequestOtp(event: React.FormEvent) {
    event.preventDefault();
    if (isSubmitting) return;
    resetState();

    const result = loginSchema.safeParse({ email, password });
    if (!result.success) {
      const errors: Record<string, string> = {};
      for (const issue of result.error.issues) {
        const key = issue.path[0] as string;
        if (!errors[key]) errors[key] = issue.message;
      }
      setFieldErrors(errors);
      (errors.email ? emailRef : passwordRef).current?.focus();
      return;
    }

    setIsSubmitting(true);
    try {
      await api.post("/auth/request-otp", { email: result.data.email });
      setStep("otp-sent");
      setOtp("");
      setTimeout(() => otpRef.current?.focus(), 100);
    } catch (error) {
      setFormError(extractApiError(error));
      setIsSubmitting(false);
    }
  }

  async function handleVerifyOtp(event: React.FormEvent) {
    event.preventDefault();
    if (isSubmitting) return;
    resetState();

    const result = otpSchema.safeParse({ code: otp });
    if (!result.success) {
      const errors: Record<string, string> = {};
      for (const issue of result.error.issues) {
        const key = issue.path[0] as string;
        if (!errors[key]) errors[key] = issue.message;
      }
      setFieldErrors(errors);
      otpRef.current?.focus();
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await api.post<{ access_token: string }>(
        "/auth/verify-otp",
        { email, otp: result.data.code, password }
      );
      api.setToken(response.access_token);
      window.location.href = "/dashboard";
    } catch (error) {
      setFormError(extractApiError(error));
      setIsSubmitting(false);
    }
  }

  const handleBack = () => {
    setStep("initial");
    setOtp("");
    resetState();
  };

  if (step === "otp-verify") {
    return (
      <div>
        <div className="mb-4 flex items-center gap-2">
          <button
            type="button"
            onClick={handleBack}
            className="rounded p-1 hover:bg-product-border"
            aria-label="Back to email and password"
          >
            <ArrowLeft size={20} className="text-product-ink" />
          </button>
          <p className="text-sm text-product-ink-soft">Verify with code sent to {email}</p>
        </div>

        <form onSubmit={handleVerifyOtp} noValidate aria-busy={isSubmitting}>
          <div>
            <label htmlFor="otp" className="login-label">Verification Code</label>
            <input
              ref={otpRef}
              id="otp"
              name="otp"
              type="text"
              inputMode="numeric"
              autoComplete="one-time-code"
              required
              maxLength={6}
              placeholder="000000"
              className="login-input font-mono text-center text-lg tracking-widest"
              value={otp}
              onChange={(event) => setOtp(event.target.value.replace(/\D/g, ""))}
              aria-invalid={!!fieldErrors.code}
              aria-describedby={fieldErrors.code ? "otp-error" : undefined}
            />
            {fieldErrors.code && (
              <p id="otp-error" className="login-error" role="alert">
                {fieldErrors.code}
              </p>
            )}
          </div>

          <p className="mt-3 text-[13px] text-product-ink-soft">
            Code expires in 5 minutes
          </p>

          {formError && (
            <p className="mb-4 rounded border border-product-border bg-product-bg px-3 py-2 text-[13px] leading-5" role="alert">
              {formError}
            </p>
          )}

          <button type="submit" className="login-button login-primary mt-6" disabled={isSubmitting || otp.length !== 6}>
            {isSubmitting && <Loader2 size={18} className="animate-spin motion-reduce:animate-none" aria-hidden="true" />}
            {isSubmitting ? "Verifying…" : "Verify and Sign In"}
          </button>
        </form>

        <div className="mt-4 text-center text-[13px] text-product-ink-soft">
          <button
            type="button"
            onClick={handleBack}
            className="login-link hover:underline"
          >
            Use password login instead
          </button>
        </div>
      </div>
    );
  }

  return (
    <>
      <form onSubmit={handleDirectLogin} noValidate aria-busy={isSubmitting}>
        <div>
          <label htmlFor="email" className="login-label">Email</label>
          <input
            ref={emailRef}
            id="email"
            name="email"
            type="email"
            autoComplete="username"
            autoCapitalize="none"
            spellCheck={false}
            required
            className="login-input"
            placeholder="Enter your email address"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            aria-invalid={!!fieldErrors.email}
            aria-describedby={fieldErrors.email ? "email-error" : undefined}
          />
          {fieldErrors.email && (
            <p id="email-error" className="login-error" role="alert">
              {fieldErrors.email}
            </p>
          )}
        </div>
        <div className="mt-5">
          <label htmlFor="password" className="login-label">Password</label>
          <div className="relative">
            <input
              ref={passwordRef}
              id="password"
              name="password"
              type={showPassword ? "text" : "password"}
              autoComplete="current-password"
              required
              className="login-input pr-12"
              placeholder="Enter your password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              aria-invalid={!!fieldErrors.password}
              aria-describedby={fieldErrors.password ? "password-error" : undefined}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              aria-label={showPassword ? "Hide password" : "Show password"}
              aria-pressed={showPassword}
              className="password-toggle absolute right-0 top-0 flex h-12 w-12 items-center justify-center rounded text-product-ink-soft"
            >
              {showPassword ? <EyeOff size={18} aria-hidden="true" /> : <Eye size={18} aria-hidden="true" />}
            </button>
          </div>
          {fieldErrors.password && (
            <p id="password-error" className="login-error" role="alert">
              {fieldErrors.password}
            </p>
          )}
        </div>
        <div className="my-3 flex items-center justify-between gap-2 text-[13px] font-medium leading-5">
          <label className="flex min-h-11 items-center gap-2 text-product-ink-soft" title="Remember me is not available yet">
            <input
              type="checkbox"
              name="remember-me"
              checked={false}
              disabled
              aria-describedby="remember-me-help"
              className="h-4 w-4 shrink-0 cursor-not-allowed accent-product-primary"
            />
            Remember me
            <span id="remember-me-help" className="sr-only">
              Remember me is not available yet.
            </span>
          </label>
          <a className="login-link inline-flex min-h-11 items-center" href="/forgot-password">
            Forgot password?
          </a>
        </div>
        {formError && (
          <p className="mb-4 rounded border border-product-border bg-product-bg px-3 py-2 text-[13px] leading-5" role="alert">
            {formError}
          </p>
        )}
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
      <button
        type="button"
        onClick={handleRequestOtp}
        className="login-button login-secondary w-full"
        disabled={isSubmitting || !email || !password}
      >
        {isSubmitting
          ? <Loader2 size={18} className="animate-spin motion-reduce:animate-none" aria-hidden="true" />
          : <Mail size={18} aria-hidden="true" />}
        {isSubmitting ? "Sending code…" : "Sign in via OTP"}
      </button>
    </>
  );
}
