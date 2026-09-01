"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { AlertTriangle, ScanLine } from "lucide-react";
import { Card, CardHeader, CardBody } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ConfidenceDial } from "@/components/confidence-dial";
import { RegionBars } from "@/components/region-bars";
import { api, extractApiError } from "@/lib/api";
import { formatDate, stageLabel } from "@/lib/utils";
import type { Patient } from "@/lib/types";

export default function PatientDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [patient, setPatient] = useState<Patient | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    let pollTimer: ReturnType<typeof setTimeout> | null = null;
    let attempts = 0;
    const MAX_ATTEMPTS = 30; // ~2 minutes at 4s intervals
    const POLL_INTERVAL_MS = 4000;

    async function load(isPoll: boolean) {
      if (!isPoll) setIsLoading(true);
      setError(null);
      try {
        const { data } = await api.get<Patient>(`/patients/${id}`);
        if (cancelled) return;
        setPatient(data);

        // Analysis still pending: keep polling until it resolves or we
        // hit the attempt cap, so the page updates itself without a
        // manual refresh once the backend finishes the pipeline.
        if (!data.latest_result && attempts < MAX_ATTEMPTS) {
          attempts += 1;
          pollTimer = setTimeout(() => load(true), POLL_INTERVAL_MS);
        }
      } catch (err) {
        if (!cancelled) setError(extractApiError(err));
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }

    load(false);
    return () => {
      cancelled = true;
      if (pollTimer) clearTimeout(pollTimer);
    };
  }, [id]);

  if (isLoading) {
    return <p className="text-sm text-text-muted">Loading patient record…</p>;
  }

  if (error || !patient) {
    return (
      <div className="flex items-center gap-2 rounded border border-amber/30 bg-amber-soft px-4 py-3 text-[13px] text-amber">
        <AlertTriangle className="h-4 w-4" />
        {error ?? "Patient not found."}
      </div>
    );
  }

  const result = patient.latest_result;
  const tone = result?.label === "healthy" ? "teal" : "amber";

  return (
    <div className="mx-auto max-w-5xl">
      <div className="mb-6">
        <p className="label-eyebrow mb-1">Patient record</p>
        <h1 className="font-display text-2xl font-medium text-text">
          {patient.full_name}
        </h1>
        <p className="mt-1 text-sm text-text-muted">
          {patient.age} yrs &middot; {patient.gender} &middot; added{" "}
          {formatDate(patient.created_at)}
        </p>
      </div>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <Card className="lg:col-span-1">
          <CardHeader eyebrow="Patient" title="Clinical context" />
          <CardBody className="space-y-3 text-[13px]">
            <Row label="MMSE score" value={patient.mmse_score ?? "—"} />
            <Row
              label="Family history"
              value={patient.family_history ? "Yes" : "No"}
            />
            {patient.notes && (
              <div>
                <p className="mb-1 text-text-faint">Notes</p>
                <p className="text-text-muted">{patient.notes}</p>
              </div>
            )}
          </CardBody>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader
            eyebrow="AI analysis"
            title="Prediction"
            action={
              result && (
                <Badge tone={tone}>{stageLabel(result.stage)}</Badge>
              )
            }
          />
          <CardBody>
            {!result ? (
              <div className="flex flex-col items-center gap-3 py-10 text-center">
                <div className="relative flex h-12 w-12 items-center justify-center rounded-full border border-line">
                  <ScanLine className="h-5 w-5 text-teal" />
                  <div className="absolute inset-0 animate-ping rounded-full border border-teal/30" />
                </div>
                <p className="text-sm text-text-muted">
                  Analysis in progress — this page updates automatically.
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-8 sm:grid-cols-2">
                <div className="flex flex-col items-center justify-center">
                  <ConfidenceDial
                    value={result.confidence}
                    tone={tone}
                    label={result.label}
                  />
                </div>
                <div>
                  <p className="label-eyebrow mb-3">Contributing regions</p>
                  <RegionBars regions={result.regions} />
                </div>
              </div>
            )}
          </CardBody>
        </Card>

        {result?.heatmap_url && (
          <Card className="lg:col-span-3">
            <CardHeader eyebrow="Explainability" title="MRI heatmap" />
            <CardBody>
              <img
                src={result.heatmap_url}
                alt="MRI attention heatmap"
                className="max-h-[420px] w-full rounded bg-black object-contain"
              />
            </CardBody>
          </Card>
        )}
      </div>
    </div>
  );
}

function Row({
  label,
  value,
}: {
  label: string;
  value: string | number;
}) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-text-faint">{label}</span>
      <span className="data-num text-text">{value}</span>
    </div>
  );
}
