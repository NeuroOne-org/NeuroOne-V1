"use client";

import { useState } from "react";
import { Play, RotateCcw, Activity, ShieldCheck, Sparkles } from "lucide-react";
import { ConfidenceDial } from "@/components/confidence-dial";
import { RegionBars } from "@/components/region-bars";
import { NeuralNetwork } from "@/components/neural-network";
import type { PredictionRegion, DiseaseLabel, DiseaseStage } from "@/lib/types";
import { cn } from "@/lib/utils";

interface SampleCase {
  id: string;
  patientId: string;
  title: string;
  subtitle: string;
  diseaseLabel: DiseaseLabel;
  stage: DiseaseStage;
  stageDisplay: string;
  confidence: number;
  tone: "teal" | "amber";
  mmse: string;
  ageGender: string;
  regions: PredictionRegion[];
}

const CASESHOTS: SampleCase[] = [
  {
    id: "case-1",
    patientId: "PAT-8812",
    title: "Alzheimer's MCI Profile",
    subtitle: "72yo Female • MMSE 24/30 • Amnestic memory deficit",
    diseaseLabel: "alzheimers",
    stage: "MCI",
    stageDisplay: "Mild Cognitive Impairment (MCI)",
    confidence: 0.89,
    tone: "amber",
    mmse: "24 / 30",
    ageGender: "72 F",
    regions: [
      { label: "Hippocampus", contribution: 0.46 },
      { label: "Entorhinal Cortex", contribution: 0.31 },
      { label: "Temporal Pole", contribution: 0.14 },
      { label: "Ventricular Space", contribution: 0.09 },
    ],
  },
  {
    id: "case-2",
    patientId: "PAT-4409",
    title: "Parkinson's Early Stage Profile",
    subtitle: "65yo Male • Hoehn & Yahr Stage 2 • Unilateral tremor",
    diseaseLabel: "parkinsons",
    stage: "MILD",
    stageDisplay: "Early Stage Motor (H&Y II)",
    confidence: 0.92,
    tone: "teal",
    mmse: "29 / 30",
    ageGender: "65 M",
    regions: [
      { label: "Substantia Nigra", contribution: 0.54 },
      { label: "Putamen / Striatum", contribution: 0.26 },
      { label: "Caudate Nucleus", contribution: 0.12 },
      { label: "Locus Coeruleus", contribution: 0.08 },
    ],
  },
  {
    id: "case-3",
    patientId: "PAT-1102",
    title: "Cognitively Normal Control",
    subtitle: "68yo Male • MMSE 30/30 • Baseline Screening",
    diseaseLabel: "healthy",
    stage: "CN",
    stageDisplay: "Cognitively Normal (CN)",
    confidence: 0.97,
    tone: "teal",
    mmse: "30 / 30",
    ageGender: "68 M",
    regions: [
      { label: "Cortical Thickness", contribution: 0.42 },
      { label: "Subcortical Integrity", contribution: 0.35 },
      { label: "Ventricular Volume", contribution: 0.15 },
      { label: "Hippocampal Reserve", contribution: 0.08 },
    ],
  },
];

export function InteractivePipelineDemo() {
  const [activeCaseId, setActiveCaseId] = useState<string>("case-1");
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [analyzed, setAnalyzed] = useState<boolean>(true);

  const activeCase = CASESHOTS.find((c) => c.id === activeCaseId) || CASESHOTS[0];

  const handleRunAnalysis = () => {
    setIsAnalyzing(true);
    setAnalyzed(false);
    setTimeout(() => {
      setIsAnalyzing(false);
      setAnalyzed(true);
    }, 1100);
  };

  return (
    <div className="rounded-lg border border-line bg-panel p-5 md:p-8 shadow-2xl backdrop-blur-md">
      {/* Step Header */}
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4 border-b border-line pb-4">
        <div>
          <span className="label-eyebrow text-indigo">Interactive Live Simulation</span>
          <h3 className="font-display text-xl font-medium text-text">
            Standardized Pipeline Execution
          </h3>
        </div>

        {/* Case selector tabs */}
        <div className="flex flex-wrap gap-2">
          {CASESHOTS.map((c) => (
            <button
              key={c.id}
              onClick={() => {
                setActiveCaseId(c.id);
                setAnalyzed(true);
              }}
              className={cn(
                "rounded-md border px-3 py-1.5 font-mono text-xs transition-all",
                activeCaseId === c.id
                  ? "border-indigo/50 bg-indigo/10 text-indigo font-medium shadow-sm"
                  : "border-line bg-ink text-text-muted hover:border-line-soft hover:text-text"
              )}
            >
              {c.title}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-8 lg:grid-cols-12 lg:items-center">
        {/* Left Column: Patient Context & Neural Mesh Execution (5 cols) */}
        <div className="lg:col-span-5 space-y-5">
          {/* Patient Card Preview */}
          <div className="rounded-md border border-line bg-ink p-4 space-y-3">
            <div className="flex items-center justify-between text-xs font-mono text-text-faint border-b border-line/60 pb-2.5">
              <span>CASE REF: {activeCase.patientId}</span>
              <span className="text-teal">MRI T1w 3T Scan</span>
            </div>

            <div>
              <p className="font-display text-base font-medium text-text">
                {activeCase.title}
              </p>
              <p className="mt-1 text-xs text-text-muted">
                {activeCase.subtitle}
              </p>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs font-mono pt-1">
              <div className="rounded bg-raised p-2">
                <span className="text-[10px] text-text-faint uppercase block">Demographics</span>
                <span className="text-text font-medium mt-0.5 block">{activeCase.ageGender}</span>
              </div>
              <div className="rounded bg-raised p-2">
                <span className="text-[10px] text-text-faint uppercase block">Cognitive MMSE</span>
                <span className="text-text font-medium mt-0.5 block">{activeCase.mmse}</span>
              </div>
            </div>
          </div>

          {/* Neural Processing Canvas */}
          <div className="relative overflow-hidden rounded-md border border-line bg-ink p-4 text-center">
            <div className="pointer-events-none absolute inset-0 opacity-40">
              <NeuralNetwork className="h-full w-full" />
            </div>

            <div className="relative py-4 space-y-3">
              <p className="text-xs font-mono text-text-muted">
                3D Volumetric Neural Mesh Analysis
              </p>

              <button
                onClick={handleRunAnalysis}
                disabled={isAnalyzing}
                className={cn(
                  "inline-flex items-center gap-2 rounded-md px-4 py-2 font-mono text-xs font-medium transition-all shadow-lg",
                  isAnalyzing
                    ? "bg-indigo/20 text-indigo border border-indigo/40 cursor-wait animate-pulse"
                    : "bg-indigo text-ink hover:bg-indigo/90"
                )}
              >
                {isAnalyzing ? (
                  <>
                    <Activity className="h-4 w-4 animate-spin text-indigo" />
                    Segmenting Brain Regions...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4 fill-current" />
                    Simulate AI Stage Estimation
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Output Results (7 cols) */}
        <div className="lg:col-span-7">
          <div className="relative min-h-[320px] rounded-md border border-line bg-ink p-6">
            {isAnalyzing ? (
              <div className="absolute inset-0 flex flex-col items-center justify-center space-y-3 bg-ink/90 backdrop-blur-sm z-10 rounded-md">
                <div className="h-10 w-10 animate-spin rounded-full border-2 border-teal border-t-transparent" />
                <p className="font-mono text-xs text-teal uppercase tracking-widest animate-pulse">
                  Analyzing Cortical Features...
                </p>
              </div>
            ) : null}

            {analyzed ? (
              <div className="space-y-6 animate-fade-up">
                {/* Result Top Badge */}
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-line pb-4">
                  <div>
                    <span className="label-eyebrow text-text-faint">Estimated Disease Stage</span>
                    <h4 className="font-display text-lg font-semibold text-text">
                      {activeCase.stageDisplay}
                    </h4>
                  </div>
                  <div className="flex items-center gap-1.5 rounded border border-teal/30 bg-teal/10 px-2.5 py-1 text-xs font-mono text-teal">
                    <ShieldCheck className="h-3.5 w-3.5" />
                    <span>Clinician Decision Support</span>
                  </div>
                </div>

                {/* Main Results Grid: Dial + Region Attribution */}
                <div className="grid grid-cols-1 sm:grid-cols-12 gap-6 items-center">
                  {/* Dial (5 cols) */}
                  <div className="sm:col-span-5 flex flex-col items-center justify-center">
                    <ConfidenceDial
                      value={activeCase.confidence}
                      tone={activeCase.tone}
                      label="Model Certainty"
                      size={150}
                    />
                  </div>

                  {/* Region Bars (7 cols) */}
                  <div className="sm:col-span-7 space-y-2">
                    <div className="flex items-center justify-between text-xs font-mono mb-2">
                      <span className="text-text-muted">Primary Driving Regions</span>
                      <span className="text-text-faint">Influence %</span>
                    </div>
                    <RegionBars regions={activeCase.regions} />
                  </div>
                </div>

                {/* Clinician Rationale Note */}
                <div className="rounded bg-raised p-3 border border-line-soft text-xs text-text-muted leading-relaxed">
                  <span className="font-semibold text-text">Clinical Insight: </span>
                  Automated stage calculation is derived from region-level voxel variance compared against multi-site standard benchmarks. Final diagnostic sign-off remains under the clinician&rsquo;s direct oversight.
                </div>
              </div>
            ) : (
              <div className="flex min-h-[280px] flex-col items-center justify-center text-center">
                <Sparkles className="h-8 w-8 text-indigo/60 mb-2" />
                <p className="font-display text-sm font-medium text-text">
                  Ready to Run Simulation
                </p>
                <p className="mt-1 text-xs text-text-muted max-w-xs">
                  Click the button on the left to trigger the neural segmentation pipeline.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
