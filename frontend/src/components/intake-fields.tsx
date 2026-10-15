"use client";

import { useFieldArray, useFormContext } from "react-hook-form";
import { CircleCheck, Loader, Plus, X } from "@/components/icons";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { FieldError, Input, Label } from "@/components/ui/input";
import { Select, Textarea } from "@/components/ui/select";
import { MriDropzone } from "@/components/mri-dropzone";
import { cn } from "@/lib/utils";
import {
  EMPTY_SYMPTOM,
  SYMPTOM_ONSETS,
  type VisitWithSymptomsInput,
} from "@/lib/validation";

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

/**
 * The structured symptom rows FR-03 asks for: name, severity, onset,
 * duration and observation. Reads the surrounding form from its
 * FormProvider, which must hold a `symptoms` array.
 */
export function SymptomsCard({ eyebrow }: { eyebrow: string }) {
  const {
    control,
    register,
    formState: { errors },
  } = useFormContext<Pick<VisitWithSymptomsInput, "symptoms">>();
  const symptoms = useFieldArray({ control, name: "symptoms" });

  return (
    <Card className="mb-5">
      <CardHeader
        eyebrow={eyebrow}
        title="Symptoms"
        action={
          <Button
            type="button"
            size="sm"
            variant="secondary"
            onClick={() => symptoms.append({ ...EMPTY_SYMPTOM })}
          >
            <Plus className="h-4 w-4" />
            Add symptom
          </Button>
        }
      />
      <CardBody className="space-y-5">
        {symptoms.fields.length === 0 && (
          <p className="text-[13px] text-text-muted">
            No symptoms recorded. A trend needs the same symptom recorded on
            more than one visit.
          </p>
        )}
        {symptoms.fields.map((field, index) => {
          const fieldErrors = errors.symptoms?.[index];
          const id = `symptom-${index}`;
          return (
            <div key={field.id} className="space-y-3">
              <div className="grid grid-cols-1 items-start gap-3 sm:grid-cols-[1fr_6rem_8rem_7rem_auto]">
                <Field
                  label="Symptom"
                  htmlFor={`${id}-name`}
                  error={fieldErrors?.symptom_name?.message}
                >
                  <Input
                    id={`${id}-name`}
                    placeholder="memory loss"
                    error={fieldErrors?.symptom_name?.message}
                    {...register(`symptoms.${index}.symptom_name`)}
                  />
                </Field>
                <Field
                  label="Severity"
                  htmlFor={`${id}-severity`}
                  error={fieldErrors?.severity?.message}
                >
                  <Input
                    id={`${id}-severity`}
                    type="number"
                    min={1}
                    max={10}
                    error={fieldErrors?.severity?.message}
                    {...register(`symptoms.${index}.severity`, {
                      valueAsNumber: true,
                    })}
                  />
                </Field>
                <Field label="Onset" htmlFor={`${id}-onset`} optional>
                  <Select id={`${id}-onset`} {...register(`symptoms.${index}.onset`)}>
                    <option value="">Not specified</option>
                    {SYMPTOM_ONSETS.map((onset) => (
                      <option key={onset} value={onset}>
                        {onset}
                      </option>
                    ))}
                  </Select>
                </Field>
                <Field
                  label="Duration (days)"
                  htmlFor={`${id}-duration`}
                  error={fieldErrors?.duration_days?.message}
                  optional
                >
                  <Input
                    id={`${id}-duration`}
                    type="number"
                    min={0}
                    error={fieldErrors?.duration_days?.message}
                    {...register(`symptoms.${index}.duration_days`, {
                      setValueAs: (value) =>
                        value === "" || value === null ? null : Number(value),
                    })}
                  />
                </Field>
                <button
                  type="button"
                  onClick={() => symptoms.remove(index)}
                  aria-label={`Remove symptom ${index + 1}`}
                  className="mt-7 flex h-10 w-10 items-center justify-center rounded border border-line text-text-faint transition-colors duration-150 hover:border-text-faint hover:text-text"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
              <Field
                label="Observation"
                htmlFor={`${id}-observation`}
                error={fieldErrors?.observation?.message}
                optional
              >
                <Textarea
                  id={`${id}-observation`}
                  rows={2}
                  placeholder="What was seen or reported"
                  {...register(`symptoms.${index}.observation`)}
                />
              </Field>
            </div>
          );
        })}
      </CardBody>
    </Card>
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
