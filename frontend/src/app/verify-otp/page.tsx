"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { AuthShell } from "@/components/auth-shell";
import { Button } from "@/components/ui/button";
import { OtpInput } from "@/components/otp-input";
import { useAuth } from "@/components/auth-provider";

export default function VerifyOtpPage() {
  return (
    <Suspense fallback={null}>
      <VerifyOtpForm />
    </Suspense>
  );
}

function VerifyOtpForm() {
  const { completeOtpLogin, pendingOtpEmail } = useAuth();
  const router = useRouter();
  const params = useSearchParams();
  const next = params.get("next") ?? "/dashboard";

  const [otp, setOtp] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const code = otp;
    if (code.length !== 6) {
      setError("Enter all 6 digits");
      return;
    }
    setError(null);
    setIsSubmitting(true);
    try {
      await completeOtpLogin(code);
      router.replace(next);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setIsSubmitting(false);
    }
  }

  // Reached directly, or after a refresh dropped the in-memory credentials.
  // There is nothing to verify against, so say so instead of failing on submit.
  if (!pendingOtpEmail) {
    return (
      <AuthShell
        title="Start again"
        subtitle="This sign-in attempt expired. Request a new code from the sign-in page."
      >
        <Button type="button" className="w-full" onClick={() => router.replace("/login")}>
          Back to sign in
        </Button>
      </AuthShell>
    );
  }

  return (
    <AuthShell
      title="Check your email"
      subtitle={`Enter the 6-digit code sent to ${pendingOtpEmail}. It expires in 5 minutes.`}
    >
      <form onSubmit={handleSubmit} noValidate>
        <OtpInput value={otp} onChange={setOtp} />

        {error && (
          <p className="mt-4 rounded border border-amber/30 bg-amber-soft px-3 py-2 text-[13px] text-amber">
            {error}
          </p>
        )}

        <Button type="submit" className="mt-6 w-full" isLoading={isSubmitting}>
          Verify &amp; sign in
        </Button>
      </form>

      <div className="mt-6 text-center text-[13px] text-text-muted">
        <Link href="/login" className="text-indigo hover:underline">
          ← Back to sign in
        </Link>
      </div>
    </AuthShell>
  );
}