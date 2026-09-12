"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { AuthShell } from "@/components/auth-shell";
import { Button } from "@/components/ui/button";
import { Input, Label, FieldError } from "@/components/ui/input";
import { useAuth } from "@/components/auth-provider";
import { loginSchema } from "@/lib/validation";

export default function LoginPage() {
  return (
    <Suspense fallback={null}>
      <LoginForm />
    </Suspense>
  );
}

function LoginForm() {
  const { login, beginOtpLogin } = useAuth();
  const router = useRouter();
  const params = useSearchParams();
  const next = params.get("next") ?? "/dashboard";
  const justReset = params.get("reset") === "1";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fieldErrors, setFieldErrors] = useState<{ email?: string; password?: string }>({});
  const [formError, setFormError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isRequestingCode, setIsRequestingCode] = useState(false);

  function validate() {
    const result = loginSchema.safeParse({ email, password });
    if (!result.success) {
      const errors: { email?: string; password?: string } = {};
      for (const issue of result.error.issues) {
        const key = issue.path[0] as "email" | "password";
        if (!errors[key]) errors[key] = issue.message;
      }
      setFieldErrors(errors);
      return null;
    }
    setFieldErrors({});
    return result.data;
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setFormError(null);

    const credentials = validate();
    if (!credentials) return;

    setIsSubmitting(true);
    try {
      await login(credentials);
      router.replace(next);
    } catch (err) {
      setFormError((err as Error).message);
    } finally {
      setIsSubmitting(false);
    }
  }

  // The second factor is opt-in. /auth/verify-otp checks the password and the
  // code together, so the password is collected here and held in memory by
  // the provider rather than travelling to the next screen in the URL.
  async function handleOtpLogin() {
    setFormError(null);

    const credentials = validate();
    if (!credentials) return;

    setIsRequestingCode(true);
    try {
      await beginOtpLogin(credentials);
      router.push(`/verify-otp?next=${encodeURIComponent(next)}`);
    } catch (err) {
      setFormError((err as Error).message);
    } finally {
      setIsRequestingCode(false);
    }
  }

  return (
    <AuthShell title="Sign in" subtitle="Access your patient queue and analyses.">
      {justReset && (
        <p className="mb-4 rounded border border-line bg-raised px-3 py-2 text-[13px] text-text-muted">
          Your password has been reset. Sign in with your new password.
        </p>
      )}

      <form onSubmit={handleSubmit} noValidate>
        <div>
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            autoComplete="username"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            error={fieldErrors.email}
          />
          <FieldError message={fieldErrors.email} />
        </div>

        <div className="mt-4">
          <div className="flex items-center justify-between">
            <Label htmlFor="password">Password</Label>
            <Link href="/forgot-password" className="text-[13px] text-indigo hover:underline">
              Forgot password?
            </Link>
          </div>
          <Input
            id="password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            error={fieldErrors.password}
          />
          <FieldError message={fieldErrors.password} />
        </div>

        {formError && (
          <p className="mt-4 rounded border border-amber/30 bg-amber-soft px-3 py-2 text-[13px] text-amber">
            {formError}
          </p>
        )}

        <Button type="submit" className="mt-6 w-full" isLoading={isSubmitting}>
          Sign in
        </Button>

        <button
          type="button"
          onClick={handleOtpLogin}
          disabled={isSubmitting || isRequestingCode}
          className="mt-3 w-full text-[13px] text-text-muted hover:text-indigo hover:underline disabled:opacity-50"
        >
          {isRequestingCode ? "Sending code…" : "Sign in with an email code instead"}
        </button>
      </form>
    </AuthShell>
  );
}