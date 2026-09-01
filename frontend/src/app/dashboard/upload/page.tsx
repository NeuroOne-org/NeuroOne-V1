"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { AlertTriangle } from "lucide-react";
import { Card, CardHeader, CardBody } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input, Label, FieldError } from "@/components/ui/input";
import { Select, Textarea, Checkbox } from "@/components/ui/select";
import { MriDropzone } from "@/components/mri-dropzone";
import { api, extractApiError } from "@/lib/api";
import {
  patientIntakeSchema,
  type PatientIntakeInput,
} from "@/lib/validation";
import type { Patient } from "@/lib/types";

export default function UploadPage() {
  const router = useRouter();
  const [mriFile, setMriFile] = useState<File | null>(null);
  const [fileError, setFileError] = useState<string | null>(null);
  const [serverError, setServerError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<PatientIntakeInput>({
    resolver: zodResolver(patientIntakeSchema),
    defaultValues: { family_history: false },
  });

  async function onSubmit(values: PatientIntakeInput) {
    if (!mriFile) {
      setFileError("Attach an MRI scan before analyzing.");
      return;
    }
    setFileError(null);
    setServerError(null);
    setIsSubmitting(true);

    try {
      const formData = new FormData();
      formData.append("full_name", values.full_name);
      formData.append("age", String(values.age));
      formData.append("gender", values.gender);
      if (values.mmse_score !== undefined) {
        formData.append("mmse_score", String(values.mmse_score));
      }
      formData.append("family_history", String(values.family_history));
      if (values.notes) formData.append("notes", values.notes);
      formData.append("mri_scan", mriFile);

      // Backend contract: creates the patient record, kicks off the
      // AI pipeline, and returns the patient with its (pending or
      // completed) latest_result.
      const { data } = await api.post<Patient>("/patients", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      router.push(`/dashboard/patients/${data.id}`);
    } catch (err) {
      setServerError(extractApiError(err));
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-3xl">
      <div className="mb-6">
        <p className="label-eyebrow mb-1">Intake</p>
        <h1 className="font-display text-2xl font-medium text-text">
          New scan
        </h1>
        <p className="mt-1 text-sm text-text-muted">
          Upload an MRI series and patient context. The model combines both to
          estimate stage and confidence.
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <Card className="mb-5">
          <CardHeader eyebrow="Step 1" title="MRI scan" />
          <CardBody>
            <MriDropzone file={mriFile} onChange={setMriFile} />
            <FieldError message={fileError ?? undefined} />
          </CardBody>
        </Card>

        <Card className="mb-5">
          <CardHeader eyebrow="Step 2" title="Patient information" />
          <CardBody className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div className="sm:col-span-2">
              <Label htmlFor="full_name">Full name</Label>
              <Input
                id="full_name"
                placeholder="Patient's full name"
                error={errors.full_name?.message}
                {...register("full_name")}
              />
              <FieldError message={errors.full_name?.message} />
            </div>

            <div>
              <Label htmlFor="age">Age</Label>
              <Input
                id="age"
                type="number"
                placeholder="68"
                error={errors.age?.message}
                {...register("age")}
              />
              <FieldError message={errors.age?.message} />
            </div>

            <div>
              <Label htmlFor="gender">Gender</Label>
              <Select id="gender" defaultValue="" error={errors.gender?.message} {...register("gender")}>
                <option value="" disabled>
                  Select
                </option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </Select>
              <FieldError message={errors.gender?.message} />
            </div>

            <div>
              <Label htmlFor="mmse_score">MMSE score (0–30)</Label>
              <Input
                id="mmse_score"
                type="number"
                placeholder="Optional"
                error={errors.mmse_score?.message}
                {...register("mmse_score")}
              />
              <FieldError message={errors.mmse_score?.message} />
            </div>

            <div className="flex items-center gap-2 pt-6">
              <Checkbox id="family_history" {...register("family_history")} />
              <label htmlFor="family_history" className="text-sm text-text-muted">
                Family history of neurodegenerative disease
              </label>
            </div>

            <div className="sm:col-span-2">
              <Label htmlFor="notes">Clinical notes</Label>
              <Textarea
                id="notes"
                rows={3}
                placeholder="Optional context for the record"
                {...register("notes")}
              />
            </div>
          </CardBody>
        </Card>

        {serverError && (
          <div className="mb-5 flex items-center gap-2 rounded border border-amber/30 bg-amber-soft px-4 py-3 text-[13px] text-amber">
            <AlertTriangle className="h-4 w-4 shrink-0" />
            {serverError}
          </div>
        )}

        <div className="flex justify-end gap-3">
          <Button
            type="submit"
            size="lg"
            isLoading={isSubmitting}
          >
            Run analysis
          </Button>
        </div>
      </form>
    </div>
  );
}
