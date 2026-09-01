"use client";

import { Suspense, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { AuthShell } from "@/components/auth-shell";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/components/auth-provider";

export default function VerifyOtpPage() {
  return (
    <Suspense fallback={null}>
      <VerifyOtpForm />
    </Suspense>
  );
}

function VerifyOtpForm() {
  const { verifyLoginOtp } = useAuth();
  const router = useRouter();
  const params = useSearchParams();
  const username = params.get("username") ?? "";
  const next = params.get("next") ?? "/dashboard";

  const [digits, setDigits] = useState<string[]>(Array(6).fill(""));
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const inputsRef = useRef<(HTMLInputElement | null)[]>([]);

  useEffect(() => {
    inputsRef.current[0]?.focus();
  }, []);

  function handleChange(index: number, value: string) {
    const clean = value.replace(/\D/g, "").slice(-1);
    const next = [...digits];
    next[index] = clean;
    setDigits(next);
    if (clean && index < 5) inputsRef.current[index + 1]?.focus();
  }

  function handleKeyDown(index: number, e: React.KeyboardEvent) {
    if (e.key === "Backspace" && !digits[index] && index > 0) {
      inputsRef.current[index - 1]?.focus();
    }
  }

  function handlePaste(e: React.ClipboardEvent) {
    const pasted = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, 6);
    if (!pasted) return;
    e.preventDefault();
    const next = Array(6).fill("");
    for (let i = 0; i < pasted.length; i++) next[i] = pasted[i];
    setDigits(next);
    inputsRef.current[Math.min(pasted.length, 5)]?.focus();
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const code = digits.join("");
    if (code.length !== 6) {
      setError("Enter all 6 digits");
      return;
    }
    setError(null);
    setIsSubmitting(true);
    try {
      await verifyLoginOtp(username, code);
      router.replace(next);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthShell
      title="Check your email"
      subtitle={
        username
          ? `Enter the 6-digit code sent to the email on file for ${username}. It expires in 5 minutes.`
          : "Enter the 6-digit code sent to your email. It expires in 5 minutes."
      }
    >
      <form onSubmit={handleSubmit} noValidate>
        <div className="flex justify-between gap-2" onPaste={handlePaste}>
          {digits.map((digit, i) => (
            <input
              key={i}
              ref={(el) => {
                inputsRef.current[i] = el;
              }}
              type="text"
              inputMode="numeric"
              maxLength={1}
              value={digit}
              onChange={(e) => handleChange(i, e.target.value)}
              onKeyDown={(e) => handleKeyDown(i, e)}
              className="h-12 w-11 rounded border border-line bg-raised text-center font-mono text-lg text-text focus:outline-none focus:ring-1 focus:ring-indigo focus:border-indigo"
            />
          ))}
        </div>

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