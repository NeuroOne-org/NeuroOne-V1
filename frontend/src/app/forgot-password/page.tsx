"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { AuthShell } from "@/components/auth-shell";
import { Button } from "@/components/ui/button";
import { Input, Label, FieldError } from "@/components/ui/input";
import { useAuth } from "@/components/auth-provider";
import { forgotPasswordSchema, type ForgotPasswordInput } from "@/lib/validation";

export default function ForgotPasswordPage() {
  const { requestPasswordReset } = useAuth();
  const router = useRouter();
  const [serverError, setServerError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ForgotPasswordInput>({ resolver: zodResolver(forgotPasswordSchema) });

  async function onSubmit(values: ForgotPasswordInput) {
    setServerError(null);
    setIsSubmitting(true);
    try {
      await requestPasswordReset(values.email);
      router.push(`/reset-password?email=${encodeURIComponent(values.email)}`);
    } catch (err) {
      setServerError((err as Error).message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthShell
      title="Reset your password"
      subtitle="Enter your email and we'll send you a 6-digit code."
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
        <div>
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            autoComplete="email"
            placeholder="you@hospital.org"
            error={errors.email?.message}
            {...register("email")}
          />
          <FieldError message={errors.email?.message} />
        </div>

        {serverError && (
          <p className="rounded border border-amber/30 bg-amber-soft px-3 py-2 text-[13px] text-amber">
            {serverError}
          </p>
        )}

        <Button type="submit" className="w-full" isLoading={isSubmitting}>
          Send reset code
        </Button>
      </form>

      <p className="mt-6 text-center text-[13px] text-text-muted">
        Remembered your password?{" "}
        <Link href="/login" className="text-indigo hover:underline">
          Sign in
        </Link>
      </p>
    </AuthShell>
  );
}