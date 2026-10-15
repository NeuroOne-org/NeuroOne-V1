"use client";

import { useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { FormProvider, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { ChevronLeft, CircleAlert } from "@/components/icons";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/select";
import {
  Field,
  ScanUploadField,
  StepProgress,
  SymptomsCard,
  type IntakeStep,
} from "@/components/intake-fields";
import { usePatient } from "@/hooks/use-patients";
import { extractApiError } from "@/lib/api";
import { patients as patientsApi, visits as visitsApi } from "@/lib/endpoints";
import { fullName } from "@/lib/utils";
import {
  EMPTY_SYMPTOM,
  toSymptomCreate,
  visitWithSymptomsSchema,
  type VisitWithSymptomsInput,
} from "@/lib/validation";

type StepKey = "visit" | "scan" | "analysis";

const STEPS: readonly IntakeStep<StepKey>[] = [
  { key: "visit", label: "Opening visit with symptoms" },
  { key: "scan", label: "Uploading MRI scan" },
  { key: "analysis", label: "Running analysis" },
];

/**
 * A follow-up visit for a patient already on file (ADR-006 decision 8).
 *
 * This is the only intake that can produce a trend: a returning patient's
 * second visit is what gives early_watch something to compare against, so
 * symptoms are captured here with their severities rather than left for
 * later.
 */
export default function NewVisitPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const patient = usePatient(id);

  const [mriFile, setMriFile] = useState<File | null>(null);
  const [serverError, setServerError] = useState<string | null>(null);
  const [activeStep, setActiveStep] = useState<StepKey | null>(null);
  const [doneSteps, setDoneSteps] = useState<StepKey[]>([]);
  const [uploadPct, setUploadPct] = useState(0);

  // A failure after the visit exists must not create a second visit on
  // retry, so each completed step is remembered and skipped next time.
  const [createdVisitId, setCreatedVisitId] = useState<string | null>(null);

  const form = useForm<VisitWithSymptomsInput>({
    resolver: zodResolver(visitWithSymptomsSchema),
    defaultValues: {
      chief_complaint: "",
      history: "",
      notes: "",
      symptoms: [{ ...EMPTY_SYMPTOM }],
    },
  });
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = form;

  const isSubmitting = activeStep !== null;
  const isResuming = createdVisitId !== null;
  const markDone = (step: StepKey) => setDoneSteps((s) => [...s, step]);

  async function onSubmit(values: VisitWithSymptomsInput) {
    setServerError(null);

    try {
      let visitId = createdVisitId;
      if (!visitId) {
        setActiveStep("visit");
        const visit = await patientsApi.createVisit(id, {
          chief_complaint: values.chief_complaint,
          history: values.history || null,
          notes: values.notes || null,
          status: "submitted",
          symptoms: values.symptoms.map(toSymptomCreate),
        });
        visitId = visit.id;
        setCreatedVisitId(visit.id);
        markDone("visit");
      }

      if (mriFile && !doneSteps.includes("scan")) {
        setActiveStep("scan");
        setUploadPct(0);
        await visitsApi.uploadScan(visitId, mriFile, setUploadPct);
        markDone("scan");
      }

      setActiveStep("analysis");
      await visitsApi.runAnalysis(visitId);
      markDone("analysis");

      router.push(`/dashboard/patients/${id}?visit=${visitId}`);
    } catch (err) {
      setServerError(extractApiError(err));
      setActiveStep(null);
    }
  }

  const name = patient.data ? fullName(patient.data) : "";

  return (
    <div className="mx-auto max-w-3xl">
      <Link
        href={`/dashboard/patients/${id}`}
        className="mb-5 inline-flex items-center gap-1.5 text-[13px] text-text-muted transition-colors duration-150 hover:text-text"
      >
        <ChevronLeft className="h-4 w-4" />
        Back to patient
      </Link>

      <header className="mb-6">
        <p className="label-eyebrow mb-1.5">Follow-up</p>
        <h1 className="font-display text-2xl font-medium text-text">
          New visit{name ? ` for ${name}` : ""}
        </h1>
        <p className="mt-1 text-sm text-text-muted">
          Records the visit and its symptoms, attaches the scan, and runs the
          analysis against this patient&apos;s earlier visits.
        </p>
      </header>

      <FormProvider {...form}>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <fieldset disabled={isSubmitting || isResuming} className="contents">
          <Card className="mb-5">
            <CardHeader eyebrow="Step 1" title="Visit" />
            <CardBody className="space-y-4">
              <Field
                label="Chief complaint"
                htmlFor="chief_complaint"
                error={errors.chief_complaint?.message}
              >
                <Input
                  id="chief_complaint"
                  placeholder="Forgetfulness getting worse"
                  error={errors.chief_complaint?.message}
                  {...register("chief_complaint")}
                />
              </Field>

              <Field label="History" htmlFor="history" optional>
                <Textarea id="history" rows={2} {...register("history")} />
              </Field>

              <Field label="Clinical notes" htmlFor="notes" optional>
                <Textarea id="notes" rows={2} {...register("notes")} />
              </Field>
            </CardBody>
          </Card>

          <SymptomsCard eyebrow="Step 2" />

          <Card className="mb-5">
            <CardHeader eyebrow="Step 3" title="MRI scan" />
            <CardBody>
              <ScanUploadField
                file={mriFile}
                onChange={setMriFile}
                isUploading={activeStep === "scan"}
                uploadPct={uploadPct}
              />
            </CardBody>
          </Card>
        </fieldset>

        {serverError && (
          <div
            role="alert"
            className="mb-5 flex items-start gap-2 rounded border border-amber/30 bg-amber-soft px-4 py-3 text-[13px] text-amber"
          >
            <CircleAlert className="mt-0.5 h-4 w-4 shrink-0" />
            <span>
              {serverError}
              {isResuming &&
                " The visit itself was saved — retrying continues from the step that failed."}
            </span>
          </div>
        )}

        {(isSubmitting || doneSteps.length > 0) && (
          <StepProgress
            steps={STEPS.filter((step) => step.key !== "scan" || mriFile)}
            activeStep={activeStep}
            doneSteps={doneSteps}
          />
        )}

        <div className="flex justify-end">
          <Button type="submit" size="lg" isLoading={isSubmitting}>
            {isResuming ? "Retry" : "Save and analyse"}
          </Button>
        </div>
      </form>
      </FormProvider>
    </div>
  );
}
