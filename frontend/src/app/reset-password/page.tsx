"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { AuthShell } from "@/components/auth-shell";
import { Button } from "@/components/ui/button";
import { Input, Label, FieldError } from "@/components/ui/input";
import { OtpInput } from "@/components/otp-input";
import { PasswordStrength } from "@/components/password-strength";
import { useAuth } from "@/components/auth-provider";
import { resetPasswordSchema, type ResetPasswordInput } from "@/lib/validation";

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={null}>
      <ResetPasswordForm />
    </Suspense>
  );
}

function ResetPasswordForm() {
  const { resetPassword } = useAuth();
  const router = useRouter();
  const params = useSearchParams();
  const email = params.get("email") ?? "";

  const [serverError, setServerError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    trigger,
    formState: { errors },
  } = useForm<ResetPasswordInput>({
    resolver: zodResolver(resetPasswordSchema),
    defaultValues: { otp: "" },
  });

  const newPassword = watch("new_password") ?? "";

  async function onSubmit(values: ResetPasswordInput) {
    setServerError(null);
    setIsSubmitting(true);
    try {
      await resetPassword(email, values.otp, values.new_password);
      // Resetting does not issue a token, so sign in with the new password.
      router.replace("/login?reset=1");
    } catch (err) {
      setServerError((err as Error).message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthShell
      title="Set a new password"
      subtitle={
        email
          ? `Enter the code sent to ${email} and choose a new password.`
          : "Enter the code sent to your email and choose a new password."
      }
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
        <div>
          <Label htmlFor="otp">6-digit code</Label>
          <OtpInput
            value={watch("otp") ?? ""}
            onChange={(value) => {
              setValue("otp", value, { shouldValidate: false });
              if (value.length === 6) trigger("otp");
            }}
            error={errors.otp?.message}
          />
        </div>

        <div>
          <Label htmlFor="new_password">New password</Label>
          <Input
            id="new_password"
            type="password"
            placeholder="••••••••"
            error={errors.new_password?.message}
            {...register("new_password")}
          />
          <FieldError message={errors.new_password?.message} />
          <PasswordStrength value={newPassword} />
        </div>

        <div>
          <Label htmlFor="confirm_new_password">Confirm new password</Label>
          <Input
            id="confirm_new_password"
            type="password"
            placeholder="••••••••"
            error={errors.confirm_new_password?.message}
            {...register("confirm_new_password")}
          />
          <FieldError message={errors.confirm_new_password?.message} />
        </div>

        {serverError && (
          <p className="rounded border border-amber/30 bg-amber-soft px-3 py-2 text-[13px] text-amber">
            {serverError}
          </p>
        )}

        <Button type="submit" className="w-full" isLoading={isSubmitting}>
          Reset password
        </Button>
      </form>

      <p className="mt-6 text-center text-[13px] text-text-muted">
        <Link href="/forgot-password" className="text-indigo hover:underline">
          Didn't get a code? Request a new one
        </Link>
      </p>
    </AuthShell>
  );
}