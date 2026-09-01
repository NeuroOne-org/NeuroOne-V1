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
  const { login } = useAuth();
  const router = useRouter();
  const params = useSearchParams();
  const next = params.get("next") ?? "/dashboard";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fieldErrors, setFieldErrors] = useState<{ email?: string; password?: string }>({});
  const [formError, setFormError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setFormError(null);

    const result = loginSchema.safeParse({ email, password });
    if (!result.success) {
      const errors: { email?: string; password?: string } = {};
      for (const issue of result.error.issues) {
        const key = issue.path[0] as "email" | "password";
        if (!errors[key]) errors[key] = issue.message;
      }
      setFieldErrors(errors);
      return;
    }
    setFieldErrors({});

    setIsSubmitting(true);
    try {
      await login(result.data);
      router.push(`/verify-otp?username=${encodeURIComponent(email)}&next=${encodeURIComponent(next)}`);
    } catch (err) {
      setFormError((err as Error).message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthShell title="Sign in" subtitle="Access your patient queue and analyses.">
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
            </Link>          </div>
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
      </form>

      <div className="mt-6 text-center text-[13px] text-text-muted">
        New here?{" "}
        <Link href="/signup" className="text-indigo hover:underline">
          Create an account
        </Link>
      </div>
    </AuthShell>
  );
}