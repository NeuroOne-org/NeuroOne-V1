"use client";

import { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";

export function OtpInput({
  value,
  onChange,
  error,
  autoFocus = true,
  length = 6,
}: {
  value: string;
  onChange: (value: string) => void;
  error?: string;
  autoFocus?: boolean;
  length?: number;
}) {
  const [digits, setDigits] = useState<string[]>(
    Array.from({ length }, (_, i) => value[i] ?? "")
  );
  const inputsRef = useRef<(HTMLInputElement | null)[]>([]);

  useEffect(() => {
    if (autoFocus) inputsRef.current[0]?.focus();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function commit(next: string[]) {
    setDigits(next);
    onChange(next.join(""));
  }

  function handleChange(index: number, raw: string) {
    const clean = raw.replace(/\D/g, "").slice(-1);
    const next = [...digits];
    next[index] = clean;
    commit(next);
    if (clean && index < length - 1) inputsRef.current[index + 1]?.focus();
  }

  function handleKeyDown(index: number, e: React.KeyboardEvent) {
    if (e.key === "Backspace" && !digits[index] && index > 0) {
      inputsRef.current[index - 1]?.focus();
    }
  }

  function handlePaste(e: React.ClipboardEvent) {
    const pasted = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, length);
    if (!pasted) return;
    e.preventDefault();
    const next = Array.from({ length }, (_, i) => pasted[i] ?? "");
    commit(next);
    inputsRef.current[Math.min(pasted.length, length - 1)]?.focus();
  }

  return (
    <div>
      <div className="flex justify-between gap-2" onPaste={handlePaste}>
        {digits.map((digit, i) => (
          <input
            key={i}
            ref={(el) => {
              inputsRef.current[i] = el;
            }}
            type="text"
            inputMode="numeric"
            autoComplete="one-time-code"
            maxLength={1}
            value={digit}
            onChange={(e) => handleChange(i, e.target.value)}
            onKeyDown={(e) => handleKeyDown(i, e)}
            className={cn(
              "h-12 w-11 rounded border bg-raised text-center font-mono text-lg text-text transition-colors",
              "focus:outline-none focus:ring-1 focus:ring-indigo focus:border-indigo",
              error ? "border-amber/60" : "border-line"
            )}
          />
        ))}
      </div>
      {error && <p className="mt-1.5 text-[12px] text-amber">{error}</p>}
    </div>
  );
}
