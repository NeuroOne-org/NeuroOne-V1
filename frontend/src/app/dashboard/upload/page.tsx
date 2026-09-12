"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { CircleAlert, CircleCheck, Loader } from "@/components/icons";
import { Card, CardHeader, CardBody } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input, Label, FieldError } from "@/components/ui/input";
import { Select, Textarea } from "@/components/ui/select";
import { MriDropzone } from "@/components/mri-dropzone";
import { extractApiError } from "@/lib/api";
import { patients as patientsApi, visits as visitsApi } from "@/lib/endpoints";
import { cn } from "@/lib/utils";
import {
  BLOOD_GROUPS,
  patientIntakeSchema,
  visitIntakeSchema,
  type PatientIntakeInput,
  type VisitIntakeInput,
} from "@/lib/validation";
import { z } from "zod";

const intakeSchema = patientIntakeSchema.and(visitIntakeSchema);
type IntakeInput = PatientIntakeInput & VisitIntakeInput;

/** The steps the submit actually performs, in order, so progress can be shown. */
const STEPS = [
  { key: "patient", label: "Creating patient record" },
  { key: "visit", label: "Opening visit" },
  { key: "scan", label: "Uploading MRI scan" },
  { key: "analysis", label: "Running analysis" },
] as const;

type StepKey = (typeof STEPS)[number]["key"];

export default function UploadPage() {
  const router = useRouter();
  const [mriFile, setMriFile] = useState<File | null>(null);
  const [fileError, setFileError] = useState<string | null>(null);
  const [serverError, setServerError] = useState<string | null>(null);
  const [activeStep, setActiveStep] = useState<StepKey | null>(null);
  const [doneSteps, setDoneSteps] = useState<StepKey[]>([]);
  const [uploadPct, setUploadPct] = useState(0);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<IntakeInput>({
    resolver: zodResolver(intakeSchema as unknown as z.ZodType<IntakeInput>),
  });

  const isSubmitting = activeStep !== null;

  async function onSubmit(values: IntakeInput) {
    setFileError(null);
    setServerError(null);
    setDoneSteps([]);
    setUploadPct(0);

    try {
      setActiveStep("patient");
      const patient = await patientsApi.create({
        first_name: values.first_name,
        last_name: values.last_name || null,
        dob: values.dob,
        gender: values.gender,
        email: values.email,
        phone: [{ phone_number: values.phone }],
        address: values.address,
        blood_group: values.blood_group,
        allergies: splitList(values.allergies),
        emergency_contact: values.emergency_contact,
      });
      setDoneSteps((s) => [...s, "patient"]);

      setActiveStep("visit");
      const visit = await patientsApi.createVisit(patient.id, {
        chief_complaint: values.chief_complaint,
        history: values.history || null,
        notes: values.notes || null,
        status: "submitted",
      });
      setDoneSteps((s) => [...s, "visit"]);

      // The scan is optional: the pipeline reads symptoms and history too,
      // and an intake without imaging is still a real visit.
      if (mriFile) {
        setActiveStep("scan");
        await visitsApi.uploadScan(visit.id, mriFile, setUploadPct);
        setDoneSteps((s) => [...s, "scan"]);
      }

      setActiveStep("analysis");
      await visitsApi.runAnalysis(visit.id);
      setDoneSteps((s) => [...s, "analysis"]);

      router.push(`/dashboard/patients/${patient.id}`);
    } catch (err) {
      setServerError(extractApiError(err));
      setActiveStep(null);
    }
  }

  return (
    <div className="mx-auto max-w-3xl">
      <header className="mb-6">
        <p className="label-eyebrow mb-1.5">Intake</p>
        <h1 className="font-display text-2xl font-medium text-text">
          New patient &amp; visit
        </h1>
        <p className="mt-1 text-sm text-text-muted">
          Creates the patient record, opens a visit, attaches the scan, and runs
          the analysis pipeline.
        </p>
      </header>

      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <Card className="mb-5">
          <CardHeader eyebrow="Step 1" title="Patient" />
          <CardBody className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="First name" error={errors.first_name?.message}>
              <Input
                id="first_name"
                placeholder="Jane"
                error={errors.first_name?.message}
                {...register("first_name")}
              />
            </Field>

            <Field label="Last name" error={errors.last_name?.message} optional>
              <Input id="last_name" placeholder="Okafor" {...register("last_name")} />
            </Field>

            <Field label="Date of birth" error={errors.dob?.message}>
              <Input
                id="dob"
                type="date"
                error={errors.dob?.message}
                {...register("dob")}
              />
            </Field>

            <Field label="Gender" error={errors.gender?.message}>
              <Select
                id="gender"
                defaultValue=""
                error={errors.gender?.message}
                {...register("gender")}
              >
                <option value="" disabled>
                  Select
                </option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </Select>
            </Field>

            <Field label="Email" error={errors.email?.message}>
              <Input
                id="email"
                type="email"
                placeholder="jane@example.com"
                error={errors.email?.message}
                {...register("email")}
              />
            </Field>

            <Field label="Phone" error={errors.phone?.message}>
              <Input
                id="phone"
                placeholder="+1 555 0100"
                error={errors.phone?.message}
                {...register("phone")}
              />
            </Field>

            <Field label="Blood group" error={errors.blood_group?.message}>
              <Select
                id="blood_group"
                defaultValue=""
                error={errors.blood_group?.message}
                {...register("blood_group")}
              >
                <option value="" disabled>
                  Select
                </option>
                {BLOOD_GROUPS.map((group) => (
                  <option key={group} value={group}>
                    {group}
                  </option>
                ))}
              </Select>
            </Field>

            <Field
              label="Emergency contact"
              error={errors.emergency_contact?.message}
            >
              <Input
                id="emergency_contact"
                placeholder="Name and number"
                error={errors.emergency_contact?.message}
                {...register("emergency_contact")}
              />
            </Field>

            <div className="sm:col-span-2">
              <Field label="Address" error={errors.address?.message}>
                <Input
                  id="address"
                  placeholder="Street, city, postcode"
                  error={errors.address?.message}
                  {...register("address")}
                />
              </Field>
            </div>

            <div className="sm:col-span-2">
              <Field
                label="Allergies"
                error={errors.allergies?.message}
                hint="Comma separated"
                optional
              >
                <Input
                  id="allergies"
                  placeholder="Penicillin, latex"
                  {...register("allergies")}
                />
              </Field>
            </div>
          </CardBody>
        </Card>

        <Card className="mb-5">
          <CardHeader eyebrow="Step 2" title="Visit" />
          <CardBody className="space-y-4">
            <Field
              label="Chief complaint"
              error={errors.chief_complaint?.message}
            >
              <Input
                id="chief_complaint"
                placeholder="Progressive memory loss over six months"
                error={errors.chief_complaint?.message}
                {...register("chief_complaint")}
              />
            </Field>

            <Field label="History" error={errors.history?.message} optional>
              <Textarea
                id="history"
                rows={3}
                placeholder="Relevant medical and family history"
                {...register("history")}
              />
            </Field>

            <Field label="Clinical notes" error={errors.notes?.message} optional>
              <Textarea
                id="notes"
                rows={3}
                placeholder="Anything the pipeline should have as context"
                {...register("notes")}
              />
            </Field>
          </CardBody>
        </Card>

        <Card className="mb-5">
          <CardHeader eyebrow="Step 3" title="MRI scan" />
          <CardBody>
            <MriDropzone file={mriFile} onChange={setMriFile} />
            <FieldError message={fileError ?? undefined} />
            {activeStep === "scan" && (
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
          </CardBody>
        </Card>

        {serverError && (
          <div className="mb-5 flex items-start gap-2 rounded border border-amber/30 bg-amber-soft px-4 py-3 text-[13px] text-amber">
            <CircleAlert className="mt-0.5 h-4 w-4 shrink-0" />
            {serverError}
          </div>
        )}

        {isSubmitting && (
          <div className="mb-5 rounded border border-line bg-panel px-4 py-3">
            <ul className="space-y-2">
              {STEPS.filter((step) => step.key !== "scan" || mriFile).map(
                (step) => {
                  const done = doneSteps.includes(step.key);
                  const current = activeStep === step.key;
                  return (
                    <li
                      key={step.key}
                      className={cn(
                        "flex items-center gap-2.5 text-[13px] transition-colors duration-200",
                        done
                          ? "text-teal"
                          : current
                            ? "text-text"
                            : "text-text-faint"
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
                }
              )}
            </ul>
          </div>
        )}

        <div className="flex justify-end">
          <Button type="submit" size="lg" isLoading={isSubmitting}>
            Create and analyse
          </Button>
        </div>
      </form>
    </div>
  );
}

/* -- pieces ----------------------------------------------------------- */

function Field({
  label,
  error,
  hint,
  optional,
  children,
}: {
  label: string;
  error?: string;
  hint?: string;
  optional?: boolean;
  children: React.ReactNode;
}) {
  return (
    <div>
      <div className="flex items-baseline justify-between">
        <Label>{label}</Label>
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

function splitList(value?: string): string[] {
  if (!value) return [];
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}
