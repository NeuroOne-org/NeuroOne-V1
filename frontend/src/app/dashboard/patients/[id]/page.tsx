"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  Activity,
  Calendar,
  ChevronLeft,
  CircleCheck,
  FileArrowDown,
  FileText,
  Scan,
  Sparkles,
} from "@/components/icons";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardBody } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { EmptyState, ErrorState, Skeleton } from "@/components/ui/state";
import { AnalysisFindings } from "@/components/analysis-findings";
import { AnalysisProvenance } from "@/components/analysis-provenance";
import { useAsync } from "@/hooks/use-api";
import { usePatient, usePatientVisits } from "@/hooks/use-patients";
import { analyses as analysesApi, reports as reportsApi, visits as visitsApi } from "@/lib/endpoints";
import { extractApiError } from "@/lib/api";
import {
  ageFromDob,
  cn,
  formatDate,
  formatDateTime,
  fullName,
  visitStatusLabel,
} from "@/lib/utils";
import type { Analysis, Visit } from "@/lib/types";

export default function PatientDetailPage() {
  const { id } = useParams<{ id: string }>();
  const patient = usePatient(id);
  const visits = usePatientVisits(id);

  const [selectedVisitId, setSelectedVisitId] = useState<string | null>(null);

  const visitItems = visits.data?.items ?? [];
  // Default to the most recent visit once they land, without clobbering a
  // visit the clinician has since picked.
  const activeVisitId = selectedVisitId ?? visitItems[0]?.id ?? null;

  if (patient.isLoading && patient.isInitialLoad) {
    return <DetailSkeleton />;
  }

  if (patient.error || !patient.data) {
    return (
      <div className="mx-auto max-w-5xl">
        <BackLink />
        <Card>
          <ErrorState
            message={patient.error ?? "Patient not found."}
            onRetry={patient.refetch}
          />
        </Card>
      </div>
    );
  }

  const record = patient.data;
  const name = fullName(record) || "Unnamed patient";
  const age = ageFromDob(record.dob);

  return (
    <div className="mx-auto max-w-5xl">
      <BackLink />

      <header className="mb-6">
        <p className="label-eyebrow mb-1.5">Patient record</p>
        <h1 className="font-display text-2xl font-medium text-text">{name}</h1>
        <p className="mt-1 text-sm text-text-muted">
          {age !== null ? `${age} yrs · ` : ""}
          <span className="capitalize">{record.gender}</span>
          {record.blood_group ? ` · ${record.blood_group}` : ""} · on file since{" "}
          {formatDate(record.created_at)}
        </p>
      </header>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <div className="space-y-5 lg:col-span-1">
          <Card>
            <CardHeader eyebrow="Patient" title="Contact & context" />
            <CardBody className="space-y-2.5 text-[13px]">
              <Row label="Email" value={record.email || "—"} />
              <Row
                label="Phone"
                value={record.phone?.[0]?.phone_number ?? "—"}
              />
              <Row label="Date of birth" value={formatDate(record.dob)} />
              <Row label="Emergency" value={record.emergency_contact || "—"} />
              <Row
                label="Clinician"
                value={
                  record.doctor
                    ? `${record.doctor.first_name} ${record.doctor.last_name}`.trim()
                    : "—"
                }
              />
              {record.allergies?.length > 0 && (
                <div className="pt-1">
                  <p className="mb-1.5 text-text-faint">Allergies</p>
                  <div className="flex flex-wrap gap-1.5">
                    {record.allergies.map((allergy) => (
                      <Badge key={allergy} tone="amber">
                        {allergy}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
              {record.address && (
                <div className="pt-1">
                  <p className="mb-1 text-text-faint">Address</p>
                  <p className="leading-relaxed text-text-muted">
                    {record.address}
                  </p>
                </div>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader
              eyebrow={
                visits.data ? `${visits.data.pagination.total_records} total` : "Loading"
              }
              title="Visits"
            />
            {visits.isLoading && visits.isInitialLoad ? (
              <CardBody className="space-y-2">
                <Skeleton className="h-12 w-full" />
                <Skeleton className="h-12 w-full" />
              </CardBody>
            ) : visits.error ? (
              <ErrorState message={visits.error} onRetry={visits.refetch} />
            ) : visitItems.length === 0 ? (
              <EmptyState
                icon={Calendar}
                title="No visits recorded"
                hint="Start one from the intake form."
              />
            ) : (
              <div className="max-h-[380px] overflow-y-auto">
                {visitItems.map((visit) => (
                  <VisitButton
                    key={visit.id}
                    visit={visit}
                    active={visit.id === activeVisitId}
                    onSelect={() => setSelectedVisitId(visit.id)}
                  />
                ))}
              </div>
            )}
          </Card>
        </div>

        <div className="lg:col-span-2">
          {activeVisitId ? (
            <VisitAnalysis key={activeVisitId} visitId={activeVisitId} />
          ) : (
            <Card>
              <CardHeader eyebrow="AI analysis" title="Nothing to show" />
              <EmptyState
                icon={Scan}
                title="No visit selected"
                hint="Analyses are attached to a visit, not to the patient."
              />
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}

/* -- analysis panel --------------------------------------------------- */

function VisitAnalysis({ visitId }: { visitId: string }) {
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [status, setStatus] = useState<"loading" | "none" | "ready" | "error">(
    "loading"
  );
  const [error, setError] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [isSigningOff, setIsSigningOff] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  const cancelled = useRef(false);
  useEffect(() => {
    cancelled.current = false;
    return () => {
      cancelled.current = true;
    };
  }, []);

  const load = useCallback(async () => {
    setStatus("loading");
    setError(null);
    try {
      const latest = await visitsApi.latestAnalysis(visitId);
      if (cancelled.current) return;
      setAnalysis(latest);
      setStatus("ready");
    } catch (err) {
      if (cancelled.current) return;
      // A visit with no analysis yet is a 404, which is a normal state
      // here rather than a failure worth showing as one.
      const message = extractApiError(err);
      if (/not found/i.test(message)) {
        setAnalysis(null);
        setStatus("none");
      } else {
        setError(message);
        setStatus("error");
      }
    }
  }, [visitId]);

  useEffect(() => {
    load();
  }, [load]);

  async function runAnalysis() {
    setActionError(null);
    setIsRunning(true);
    try {
      const result = await visitsApi.runAnalysis(visitId);
      setAnalysis(result);
      setStatus("ready");
    } catch (err) {
      setActionError(extractApiError(err));
    } finally {
      setIsRunning(false);
    }
  }

  async function signOff() {
    if (!analysis) return;
    setActionError(null);
    setIsSigningOff(true);
    try {
      setAnalysis(await analysesApi.signOff(analysis.id));
    } catch (err) {
      setActionError(extractApiError(err));
    } finally {
      setIsSigningOff(false);
    }
  }

  async function downloadReport() {
    if (!analysis) return;
    setActionError(null);
    setIsDownloading(true);
    try {
      // Reuse an existing report for this analysis rather than generating a
      // second one every time the button is pressed.
      const existing = await analysesApi.reports(analysis.id, { page_size: 1 });
      const report = existing.items[0] ?? (await analysesApi.createReport(analysis.id));
      const blob = await reportsApi.downloadPdf(report.id);

      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = report.filename || `analysis-${analysis.id}.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      setActionError(extractApiError(err));
    } finally {
      setIsDownloading(false);
    }
  }

  const isSignedOff = Boolean(analysis?.reviewed_at);

  return (
    <Card>
      <CardHeader
        eyebrow="AI analysis"
        title={analysis ? "Latest findings" : "Analysis"}
        action={
          analysis && (
            <Badge tone={isSignedOff ? "teal" : "indigo"}>
              {isSignedOff ? "Signed off" : "Awaiting sign-off"}
            </Badge>
          )
        }
      />

      {status === "loading" ? (
        <CardBody className="space-y-3">
          <Skeleton className="h-4 w-40" />
          <Skeleton className="h-16 w-full" />
          <Skeleton className="h-16 w-full" />
        </CardBody>
      ) : status === "error" ? (
        <ErrorState message={error ?? "Could not load the analysis."} onRetry={load} />
      ) : status === "none" ? (
        <EmptyState
          icon={Sparkles}
          title="This visit has not been analysed"
          hint="Run the pipeline to generate ranked findings with citations."
          action={
            <Button size="sm" onClick={runAnalysis} isLoading={isRunning}>
              <Sparkles className="h-4 w-4" />
              Run analysis
            </Button>
          }
        />
      ) : analysis ? (
        <CardBody>
          <div className="mb-5 flex flex-wrap items-center gap-x-4 gap-y-1 text-[12px] text-text-faint">
            <span className="flex items-center gap-1.5">
              <Activity className="h-3.5 w-3.5" />
              {analysis.model_name}
            </span>
            <span className="data-num">
              Generated {formatDateTime(analysis.generated_at)}
            </span>
            {analysis.reviewed_at && (
              <span className="data-num flex items-center gap-1.5 text-teal">
                <CircleCheck className="h-3.5 w-3.5" />
                Signed off {formatDateTime(analysis.reviewed_at)}
              </span>
            )}
          </div>

          <AnalysisProvenance analysis={analysis} />

          {analysis.findings && analysis.findings.length > 0 ? (
            <AnalysisFindings findings={analysis.findings} />
          ) : (
            <p className="py-6 text-center text-[13px] text-text-muted">
              The pipeline returned no findings for this visit.
            </p>
          )}

          {actionError && (
            <p className="mt-5 rounded border border-amber/30 bg-amber-soft px-3 py-2 text-[13px] text-amber">
              {actionError}
            </p>
          )}

          <div className="mt-6 flex flex-wrap gap-2 border-t border-line pt-5">
            {!isSignedOff && (
              <Button size="sm" onClick={signOff} isLoading={isSigningOff}>
                <CircleCheck className="h-4 w-4" />
                Sign off
              </Button>
            )}
            <Button
              size="sm"
              variant="secondary"
              onClick={downloadReport}
              isLoading={isDownloading}
              // The backend gates report generation on sign-off, so the
              // button says why it is unavailable instead of failing.
              disabled={!isSignedOff}
              title={isSignedOff ? undefined : "Sign off before generating a report"}
            >
              <FileArrowDown className="h-4 w-4" />
              Download report
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={runAnalysis}
              isLoading={isRunning}
            >
              <Sparkles className="h-4 w-4" />
              Re-run
            </Button>
          </div>
        </CardBody>
      ) : null}
    </Card>
  );
}

/* -- pieces ----------------------------------------------------------- */

function VisitButton({
  visit,
  active,
  onSelect,
}: {
  visit: Visit;
  active: boolean;
  onSelect: () => void;
}) {
  return (
    <button
      onClick={onSelect}
      aria-current={active ? "true" : undefined}
      className={cn(
        "flex w-full items-start gap-3 border-b border-line px-5 py-3 text-left last:border-b-0",
        "transition-[background-color,transform] duration-150 ease-out active:scale-[0.99]",
        active ? "bg-raised" : "hover:bg-raised/60"
      )}
    >
      <FileText
        className={cn(
          "mt-0.5 h-4 w-4 shrink-0",
          active ? "text-teal" : "text-text-faint"
        )}
      />
      <div className="min-w-0 flex-1">
        <p className="truncate text-[13px] text-text">{visit.chief_complaint}</p>
        <p className="data-num mt-0.5 text-[11px] text-text-faint">
          {formatDate(visit.visit_date)} · {visitStatusLabel(visit.status)}
        </p>
      </div>
    </button>
  );
}

function Row({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex items-start justify-between gap-4">
      <span className="shrink-0 text-text-faint">{label}</span>
      <span className="truncate text-right text-text">{value}</span>
    </div>
  );
}

function BackLink() {
  return (
    <Link
      href="/dashboard"
      className="mb-5 inline-flex items-center gap-1.5 text-[13px] text-text-muted transition-colors duration-150 hover:text-text"
    >
      <ChevronLeft className="h-4 w-4" />
      Back to queue
    </Link>
  );
}

function DetailSkeleton() {
  return (
    <div className="mx-auto max-w-5xl">
      <Skeleton className="mb-5 h-4 w-28" />
      <Skeleton className="mb-2 h-3 w-24" />
      <Skeleton className="mb-2 h-7 w-64" />
      <Skeleton className="mb-6 h-4 w-80" />
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <Skeleton className="h-64 lg:col-span-1" />
        <Skeleton className="h-64 lg:col-span-2" />
      </div>
    </div>
  );
}
