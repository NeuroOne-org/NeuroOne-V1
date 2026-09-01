"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { AuthShell } from "@/components/auth-shell";
import { Button } from "@/components/ui/button";
import { Input, Label, FieldError } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { PasswordStrength } from "@/components/password-strength";
import { useAuth } from "@/components/auth-provider";
import { signupSchema, type SignupInput } from "@/lib/validation";

export default function SignupPage() {
  const { signup } = useAuth();
  const router = useRouter();
  const [serverError, setServerError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<SignupInput>({ resolver: zodResolver(signupSchema) });

  const password = watch("password") ?? "";

  async function onSubmit(values: SignupInput) {
    setServerError(null);
    setIsSubmitting(true);
    try {
      await signup(values);
      router.push(`/verify-otp?email=${encodeURIComponent(values.email)}`);
    } catch (err) {
      setServerError((err as Error).message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthShell
      title="Create an account"
      subtitle="For clinicians and researchers on the care team."
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
        <div>
          <Label htmlFor="full_name">Full name</Label>
          <Input
            id="full_name"
            placeholder="Dr. Asha Verma"
            error={errors.full_name?.message}
            {...register("full_name")}
          />
          <FieldError message={errors.full_name?.message} />
        </div>

        <div>
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            placeholder="you@hospital.org"
            error={errors.email?.message}
            {...register("email")}
          />
          <FieldError message={errors.email?.message} />
        </div>

        <div>
          <Label htmlFor="role">Role</Label>
          <Select id="role" defaultValue="" error={errors.role?.message} {...register("role")}>
            <option value="" disabled>
              Select a role
            </option>
            <option value="doctor">Doctor</option>
            <option value="researcher">Researcher</option>
          </Select>
          <FieldError message={errors.role?.message} />
        </div>

        <div>
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            type="password"
            placeholder="••••••••"
            error={errors.password?.message}
            {...register("password")}
          />
          <FieldError message={errors.password?.message} />
          <PasswordStrength value={password} />
        </div>

        <div>
          <Label htmlFor="confirm_password">Confirm password</Label>
          <Input
            id="confirm_password"
            type="password"
            placeholder="••••••••"
            error={errors.confirm_password?.message}
            {...register("confirm_password")}
          />
          <FieldError message={errors.confirm_password?.message} />
        </div>

        {serverError && (
          <p className="rounded border border-amber/30 bg-amber-soft px-3 py-2 text-[13px] text-amber">
            {serverError}
          </p>
        )}

        <Button type="submit" className="w-full" isLoading={isSubmitting}>
          Create account
        </Button>
      </form>

      <p className="mt-6 text-center text-[13px] text-text-muted">
        Already have an account?{" "}
        <Link href="/login" className="text-indigo hover:underline">
          Sign in
        </Link>
      </p>
    </AuthShell>
  );
}
