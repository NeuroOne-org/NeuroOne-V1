"use client";

import { CircleCheck, Loader } from "@/components/icons";
import { FieldError, Label } from "@/components/ui/input";
import { MriDropzone } from "@/components/mri-dropzone";
import { cn } from "@/lib/utils";

/**
 * Pieces shared by the two intake forms: New patient & visit, and a
 * follow-up New visit for an existing patient (ADR-006 decision 8).
 */

export function Field({
  label,
  htmlFor,
  error,
  hint,
  optional,
  children,
}: {
  label: string;
  htmlFor?: string;
  error?: string;
  hint?: string;
  optional?: boolean;
  children: React.ReactNode;
}) {
  return (
    <div>
      <div className="flex items-baseline justify-between">
        <Label htmlFor={htmlFor}>{label}</Label>
        {optional && (
          <span className="mb-1.5 text-[11px] text-text-faint">Optional</span>
        )}
      </div>
      {children}
      {hint && !error && (
        <p className="mt-1 text-[11px] text-text-faint">{hint}</p>
      )}
      <FieldError message={error} />
    </div>
  );
}

export interface IntakeStep<K extends string> {
  key: K;
  label: string;
}

/** The steps a submit actually performs, ticked off as each one lands. */
export function StepProgress<K extends string>({
  steps,
  activeStep,
  doneSteps,
}: {
  steps: readonly IntakeStep<K>[];
  activeStep: K | null;
  doneSteps: readonly K[];
}) {
  return (
    <div className="mb-5 rounded border border-line bg-panel px-4 py-3">
      <ul className="space-y-2">
        {steps.map((step) => {
          const done = doneSteps.includes(step.key);
          const current = activeStep === step.key;
          return (
            <li
              key={step.key}
              className={cn(
                "flex items-center gap-2.5 text-[13px] transition-colors duration-200",
                done ? "text-teal" : current ? "text-text" : "text-text-faint"
              )}
            >
              {done ? (
                <CircleCheck className="h-4 w-4" />
              ) : current ? (
                <Loader className="h-4 w-4 animate-spin" />
              ) : (
                <span className="h-4 w-4 rounded-full border border-line" />
              )}
              {step.label}
            </li>
          );
        })}
      </ul>
    </div>
  );
}

/** The MRI dropzone plus its upload progress bar. The scan is optional. */
export function ScanUploadField({
  file,
  onChange,
  isUploading,
  uploadPct,
  error,
}: {
  file: File | null;
  onChange: (file: File | null) => void;
  isUploading: boolean;
  uploadPct: number;
  error?: string | null;
}) {
  return (
    <>
      <MriDropzone file={file} onChange={onChange} />
      <FieldError message={error ?? undefined} />
      {isUploading && (
        <div className="mt-3">
          <div className="h-1 w-full overflow-hidden rounded-full bg-raised">
            <div
              className="h-full rounded-full bg-teal transition-[width] duration-200 ease-out"
              style={{ width: `${uploadPct}%` }}
            />
          </div>
          <p className="data-num mt-1.5 text-[11px] text-text-faint">
            Uploading {uploadPct}%
          </p>
        </div>
      )}
      <p className="mt-3 text-[12px] text-text-faint">
        Optional. The pipeline also reads the visit history and symptoms.
      </p>
    </>
  );
}
