"use client";

import { useState } from "react";
import { ShieldCheck, UserCheck, Eye, Lock, FileCheck, CheckCircle2, XCircle } from "lucide-react";
import { cn } from "@/lib/utils";

export function ClinicianTrustCard() {
  const [activeTab, setActiveTab] = useState<"neuroone" | "blackbox">("neuroone");

  return (
    <div className="rounded-lg border border-line bg-panel p-6 md:p-8 shadow-2xl backdrop-blur-md">
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4 border-b border-line pb-4">
        <div>
          <span className="label-eyebrow text-teal">Trust & Transparency Framework</span>
          <h3 className="font-display text-xl font-medium text-text">
            Designed for Clinical Governance
          </h3>
        </div>

        {/* Tab Switcher */}
        <div className="flex rounded-md border border-line bg-ink p-1">
          <button
            onClick={() => setActiveTab("neuroone")}
            className={cn(
              "flex items-center gap-1.5 rounded px-3 py-1.5 font-mono text-xs transition-all",
              activeTab === "neuroone"
                ? "bg-raised text-teal font-medium shadow-sm"
                : "text-text-muted hover:text-text"
            )}
          >
            <ShieldCheck className="h-3.5 w-3.5 text-teal" />
            NeuroOne Decision Support
          </button>
          <button
            onClick={() => setActiveTab("blackbox")}
            className={cn(
              "flex items-center gap-1.5 rounded px-3 py-1.5 font-mono text-xs transition-all",
              activeTab === "blackbox"
                ? "bg-raised text-amber font-medium shadow-sm"
                : "text-text-muted hover:text-text"
            )}
          >
            <XCircle className="h-3.5 w-3.5 text-amber" />
            Opaque "Black-Box" AI
          </button>
        </div>
      </div>

      {/* Main Content Comparison Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        {/* Left Column: Interactive Tab Showcase (7 cols) */}
        <div className="lg:col-span-7 flex flex-col justify-between rounded-md border border-line bg-ink p-6">
          {activeTab === "neuroone" ? (
            <div className="space-y-4 animate-fade-up">
              <div className="flex items-center justify-between">
                <span className="label-eyebrow text-teal">Human-in-the-Loop Architecture</span>
                <span className="inline-flex items-center gap-1 rounded bg-teal/10 px-2 py-0.5 font-mono text-[10px] text-teal border border-teal/30">
                  <CheckCircle2 className="h-3 w-3" /> Clinician Approved
                </span>
              </div>

              <h4 className="font-display text-lg font-medium text-text">
                Quantitative Evidence, Full Regional Attribution
              </h4>

              <p className="text-xs leading-relaxed text-text-muted">
                NeuroOne never issues standalone diagnoses. It quantifies volumetric change across 14 cortical and subcortical regions, presenting an explainable heat-mapped breakdown so the attending physician can inspect every data point.
              </p>

              <div className="space-y-2.5 pt-2">
                <div className="flex items-start gap-2.5 text-xs text-text">
                  <CheckCircle2 className="h-4 w-4 text-teal shrink-0 mt-0.5" />
                  <span><strong>Explainable AI (XAI):</strong> Displays exact anatomical drivers behind every stage estimation.</span>
                </div>
                <div className="flex items-start gap-2.5 text-xs text-text">
                  <CheckCircle2 className="h-4 w-4 text-teal shrink-0 mt-0.5" />
                  <span><strong>Clinician Sign-Off Required:</strong> Results serve strictly as diagnostic decision support.</span>
                </div>
                <div className="flex items-start gap-2.5 text-xs text-text">
                  <CheckCircle2 className="h-4 w-4 text-teal shrink-0 mt-0.5" />
                  <span><strong>Audit Trail & Repeatability:</strong> Every scan run preserves exact parameters for longitudinal tracking.</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-4 animate-fade-up">
              <div className="flex items-center justify-between">
                <span className="label-eyebrow text-amber">Traditional Opaque Models</span>
                <span className="inline-flex items-center gap-1 rounded bg-amber/10 px-2 py-0.5 font-mono text-[10px] text-amber border border-amber/30">
                  <XCircle className="h-3 w-3" /> High Risk
                </span>
              </div>

              <h4 className="font-display text-lg font-medium text-text text-amber/90">
                Unexplainable Stage Predictions Without Context
              </h4>

              <p className="text-xs leading-relaxed text-text-muted">
                Generic AI tools output a single percentage without highlighting which brain regions drove the calculation, forcing clinicians to blindly trust or discard the output.
              </p>

              <div className="space-y-2.5 pt-2">
                <div className="flex items-start gap-2.5 text-xs text-text-muted">
                  <XCircle className="h-4 w-4 text-amber shrink-0 mt-0.5" />
                  <span><strong>No Region Attribution:</strong> Black-box outputs provide zero visibility into underlying anatomical rationale.</span>
                </div>
                <div className="flex items-start gap-2.5 text-xs text-text-muted">
                  <XCircle className="h-4 w-4 text-amber shrink-0 mt-0.5" />
                  <span><strong>Unverifiable Risk:</strong> Increases legal liability and diagnostic uncertainty for medical staff.</span>
                </div>
              </div>
            </div>
          )}

          <div className="mt-6 pt-4 border-t border-line flex items-center justify-between font-mono text-[11px] text-text-faint">
            <span>CLINICAL ETHOS</span>
            <span className="text-text-muted">Supports Doctor Judgment • Never Replaces It</span>
          </div>
        </div>

        {/* Right Column: Key Trust Pillars (5 cols) */}
        <div className="lg:col-span-5 grid grid-cols-1 gap-3">
          <div className="rounded-md border border-line bg-ink p-4 space-y-1.5">
            <div className="flex items-center gap-2 text-teal">
              <UserCheck className="h-4 w-4" />
              <span className="font-display text-sm font-medium text-text">Doctor Control First</span>
            </div>
            <p className="text-xs text-text-muted leading-relaxed">
              Designed alongside radiologists and neurologists so that AI insights complement expert clinical evaluations.
            </p>
          </div>

          <div className="rounded-md border border-line bg-ink p-4 space-y-1.5">
            <div className="flex items-center gap-2 text-indigo">
              <FileCheck className="h-4 w-4" />
              <span className="font-display text-sm font-medium text-text">DICOM / NIfTI Standard</span>
            </div>
            <p className="text-xs text-text-muted leading-relaxed">
              Direct ingestion of raw 3D T1-weighted structural MRI sequences without manual pre-formatting required.
            </p>
          </div>

          <div className="rounded-md border border-line bg-ink p-4 space-y-1.5">
            <div className="flex items-center gap-2 text-teal">
              <Lock className="h-4 w-4" />
              <span className="font-display text-sm font-medium text-text">HIPAA-Grade Security</span>
            </div>
            <p className="text-xs text-text-muted leading-relaxed">
              End-to-end tokenized authentication and encrypted data transport for patient privacy compliance.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
