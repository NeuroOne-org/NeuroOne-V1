"use client";

import { useState } from "react";
import { Eye, Layers, Zap, Info, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface RegionInfo {
  id: string;
  name: string;
  plane: "coronal" | "axial";
  x: number; // percentage
  y: number; // percentage
  disease: "Alzheimer's Indicator" | "Parkinson's Indicator";
  metricLabel: string;
  metricValue: string;
  status: "Significant Atrophy" | "Signal Attenuation" | "Moderate Expansion" | "Cortical Thinning";
  statusTone: "amber" | "teal";
  description: string;
}

const REGIONS: RegionInfo[] = [
  {
    id: "hippocampus",
    name: "Hippocampal Formation",
    plane: "coronal",
    x: 36,
    y: 54,
    disease: "Alzheimer's Indicator",
    metricLabel: "Volume Deficit",
    metricValue: "-34.2%",
    status: "Significant Atrophy",
    statusTone: "amber",
    description:
      "Bilateral volume loss in the CA1 and subiculum subfields, strongly correlated with Braak Stage III/IV progression.",
  },
  {
    id: "entorhinal",
    name: "Entorhinal Cortex",
    plane: "coronal",
    x: 64,
    y: 58,
    disease: "Alzheimer's Indicator",
    metricLabel: "Cortical Thickness",
    metricValue: "1.74 mm",
    status: "Cortical Thinning",
    statusTone: "amber",
    description:
      "Early neurofibrillary tangle accumulation causing localized cortical mantle thinning compared to age-matched norms.",
  },
  {
    id: "ventricles",
    name: "Lateral Ventricles",
    plane: "coronal",
    x: 50,
    y: 38,
    disease: "Alzheimer's Indicator",
    metricLabel: "VBR Ratio",
    metricValue: "0.21 (+45%)",
    status: "Moderate Expansion",
    statusTone: "teal",
    description:
      "Compensatory ventricular expansion (ex vacuo expansion) resulting from surrounding periventricular white matter loss.",
  },
  {
    id: "substantia_nigra",
    name: "Substantia Nigra",
    plane: "axial",
    x: 48,
    y: 48,
    disease: "Parkinson's Indicator",
    metricLabel: "Pars Compacta Intensity",
    metricValue: "-41.8%",
    status: "Signal Attenuation",
    statusTone: "amber",
    description:
      "Loss of neuromelanin hyperintensity in N1 subregion, indicating dopaminergic neuron degeneration.",
  },
  {
    id: "caudate",
    name: "Striatum / Caudate",
    plane: "axial",
    x: 35,
    y: 35,
    disease: "Parkinson's Indicator",
    metricLabel: "Binding Index",
    metricValue: "-28.5%",
    status: "Moderate Expansion",
    statusTone: "teal",
    description:
      "Asymmetric putaminal and caudate nucleus uptake imbalance characteristic of early Hoehn & Yahr Stage 2.",
  },
];

export function InteractiveMriViewer() {
  const [showHeatmap, setShowHeatmap] = useState(true);
  const [plane, setPlane] = useState<"coronal" | "axial">("coronal");
  const [selectedRegionId, setSelectedRegionId] = useState<string>("hippocampus");

  const visibleRegions = REGIONS.filter((r) => r.plane === plane);
  const selectedRegion =
    REGIONS.find((r) => r.id === selectedRegionId) || visibleRegions[0] || REGIONS[0];

  return (
    <div className="rounded-lg border border-line bg-panel p-4 md:p-6 shadow-2xl backdrop-blur-sm">
      {/* Top Controls Bar */}
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3 border-b border-line pb-4">
        <div className="flex items-center gap-2">
          <span className="inline-flex h-2 w-2 rounded-full bg-teal animate-pulse" />
          <span className="font-mono text-xs uppercase tracking-wider text-text-muted">
            Interactive MRI Volumetric Scanner
          </span>
        </div>

        <div className="flex items-center gap-3">
          {/* Plane Selector */}
          <div className="flex rounded-md border border-line bg-ink p-1">
            <button
              onClick={() => {
                setPlane("coronal");
                setSelectedRegionId("hippocampus");
              }}
              className={cn(
                "rounded px-3 py-1 font-mono text-xs transition-colors",
                plane === "coronal"
                  ? "bg-raised text-teal font-medium shadow-sm"
                  : "text-text-muted hover:text-text"
              )}
            >
              Coronal Plane
            </button>
            <button
              onClick={() => {
                setPlane("axial");
                setSelectedRegionId("substantia_nigra");
              }}
              className={cn(
                "rounded px-3 py-1 font-mono text-xs transition-colors",
                plane === "axial"
                  ? "bg-raised text-teal font-medium shadow-sm"
                  : "text-text-muted hover:text-text"
              )}
            >
              Axial Plane
            </button>
          </div>

          {/* Heatmap Toggle */}
          <button
            onClick={() => setShowHeatmap(!showHeatmap)}
            className={cn(
              "flex items-center gap-1.5 rounded-md border px-3 py-1.5 font-mono text-xs transition-all",
              showHeatmap
                ? "border-teal/40 bg-teal/10 text-teal"
                : "border-line bg-ink text-text-muted hover:text-text"
            )}
          >
            {showHeatmap ? <Zap className="h-3.5 w-3.5 text-teal" /> : <Eye className="h-3.5 w-3.5" />}
            <span>{showHeatmap ? "AI Overlay Active" : "Raw T1w MRI"}</span>
          </button>
        </div>
      </div>

      {/* Main Scanner Container */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12 lg:items-center">
        {/* MRI Canvas Viewport (7 cols) */}
        <div className="relative aspect-square w-full max-w-md mx-auto lg:max-w-none lg:col-span-7 overflow-hidden rounded-md border border-line bg-ink/90 p-2">
          {/* Subtle grid pattern background */}
          <div
            className="absolute inset-0 opacity-15 pointer-events-none"
            style={{
              backgroundImage: `radial-gradient(#6E7BFF 1px, transparent 1px)`,
              backgroundSize: "20px 20px",
            }}
          />

          {/* Animated Scanning Beam */}
          <div className="pointer-events-none absolute inset-x-0 h-px w-full animate-scan bg-gradient-to-r from-transparent via-teal/50 to-transparent z-20" />

          {/* Stylized Anatomical Brain Slice SVG */}
          <div className="relative h-full w-full flex items-center justify-center">
            <svg
              viewBox="0 0 400 400"
              className="h-full w-full transition-transform duration-500 hover:scale-[1.02]"
            >
              <defs>
                {/* Radial gradient for Heatmap overlay */}
                <radialGradient id="heat-hippocampus" cx="36%" cy="54%" r="20%">
                  <stop offset="0%" stopColor="#FF6A3D" stopOpacity="0.8" />
                  <stop offset="50%" stopColor="#6E7BFF" stopOpacity="0.4" />
                  <stop offset="100%" stopColor="#35D6C8" stopOpacity="0" />
                </radialGradient>

                <radialGradient id="heat-entorhinal" cx="64%" cy="58%" r="18%">
                  <stop offset="0%" stopColor="#FF6A3D" stopOpacity="0.75" />
                  <stop offset="60%" stopColor="#6E7BFF" stopOpacity="0.3" />
                  <stop offset="100%" stopColor="#35D6C8" stopOpacity="0" />
                </radialGradient>

                <radialGradient id="heat-substantia" cx="48%" cy="48%" r="22%">
                  <stop offset="0%" stopColor="#FF6A3D" stopOpacity="0.85" />
                  <stop offset="70%" stopColor="#35D6C8" stopOpacity="0.35" />
                  <stop offset="100%" stopColor="#6E7BFF" stopOpacity="0" />
                </radialGradient>

                <filter id="mri-glow" x="-20%" y="-20%" width="140%" height="140%">
                  <feGaussianBlur stdDeviation="4" result="blur" />
                  <feMerge>
                    <feMergeNode in="blur" />
                    <feMergeNode in="SourceGraphic" />
                  </feMerge>
                </filter>
              </defs>

              {/* Skull & Outer Contour */}
              <ellipse
                cx="200"
                cy="200"
                rx={plane === "coronal" ? "145" : "155"}
                ry={plane === "coronal" ? "165" : "140"}
                fill="#14171B"
                stroke="#262B31"
                strokeWidth="4"
              />
              <ellipse
                cx="200"
                cy="200"
                rx={plane === "coronal" ? "138" : "148"}
                ry={plane === "coronal" ? "158" : "133"}
                fill="#0B0D10"
                stroke="#34393F"
                strokeWidth="1.5"
                strokeDasharray="4 4"
              />

              {/* Brain Hemisphere Structure Lines */}
              {plane === "coronal" ? (
                <g stroke="#34393F" fill="none" strokeWidth="1.5" opacity="0.85">
                  {/* Left & Right Cortex Sulci */}
                  <path d="M 200 65 Q 195 190 200 340" stroke="#6E7BFF" strokeWidth="1" strokeDasharray="3 3" opacity="0.5" />
                  <path d="M 80 160 C 120 140, 150 180, 180 150 C 190 200, 160 250, 120 270 C 80 230, 90 190, 80 160 Z" fill="#181C22" stroke="#262B31" />
                  <path d="M 320 160 C 280 140, 250 180, 220 150 C 210 200, 240 250, 280 270 C 320 230, 310 190, 320 160 Z" fill="#181C22" stroke="#262B31" />
                  
                  {/* Ventricles (Center) */}
                  <path d="M 180 150 Q 200 130 220 150 Q 210 190 200 200 Q 190 190 180 150 Z" fill={showHeatmap ? "#35D6C822" : "#1B1F24"} stroke="#35D6C8" strokeWidth="1.5" />
                  
                  {/* Temporal Lobe / Hippocampus boundaries */}
                  <path d="M 130 210 C 145 200, 160 220, 150 245 C 135 250, 120 230, 130 210 Z" fill={showHeatmap ? "#FF6A3D33" : "#1D2126"} stroke={showHeatmap ? "#FF6A3D" : "#565C66"} strokeWidth="1.5" />
                  <path d="M 270 210 C 255 200, 240 220, 250 245 C 265 250, 280 230, 270 210 Z" fill={showHeatmap ? "#FF6A3D33" : "#1D2126"} stroke={showHeatmap ? "#FF6A3D" : "#565C66"} strokeWidth="1.5" />
                </g>
              ) : (
                <g stroke="#34393F" fill="none" strokeWidth="1.5" opacity="0.85">
                  {/* Midbrain / Axial Anatomy */}
                  <path d="M 200 70 Q 200 200 200 330" stroke="#6E7BFF" strokeWidth="1" strokeDasharray="3 3" opacity="0.5" />
                  <ellipse cx="200" cy="190" rx="90" ry="70" fill="#181C22" stroke="#262B31" />
                  
                  {/* Substantia Nigra butterfly structure */}
                  <path d="M 170 185 C 180 175, 195 185, 190 205 C 175 210, 165 195, 170 185 Z" fill={showHeatmap ? "#FF6A3D44" : "#1B1F24"} stroke={showHeatmap ? "#FF6A3D" : "#565C66"} strokeWidth="1.5" />
                  <path d="M 230 185 C 220 175, 205 185, 210 205 C 225 210, 235 195, 230 185 Z" fill={showHeatmap ? "#FF6A3D44" : "#1B1F24"} stroke={showHeatmap ? "#FF6A3D" : "#565C66"} strokeWidth="1.5" />

                  {/* Caudate / Putamen */}
                  <path d="M 140 140 Q 160 120 180 150 Q 150 170 140 140 Z" fill={showHeatmap ? "#35D6C822" : "#1D2126"} stroke="#35D6C8" strokeWidth="1" />
                  <path d="M 260 140 Q 240 120 220 150 Q 250 170 260 140 Z" fill={showHeatmap ? "#35D6C822" : "#1D2126"} stroke="#35D6C8" strokeWidth="1" />
                </g>
              )}

              {/* Heatmap Overlay Layer */}
              {showHeatmap && (
                <g filter="url(#mri-glow)">
                  {plane === "coronal" ? (
                    <>
                      <circle cx="144" cy="216" r="45" fill="url(#heat-hippocampus)" />
                      <circle cx="256" cy="232" r="38" fill="url(#heat-entorhinal)" />
                    </>
                  ) : (
                    <circle cx="192" cy="192" r="50" fill="url(#heat-substantia)" />
                  )}
                </g>
              )}

              {/* Interactive Target Pins */}
              {visibleRegions.map((region) => {
                const isSelected = region.id === selectedRegion.id;
                const px = (region.x / 100) * 400;
                const py = (region.y / 100) * 400;
                return (
                  <g
                    key={region.id}
                    className="cursor-pointer transition-transform hover:scale-125"
                    onClick={() => setSelectedRegionId(region.id)}
                  >
                    {/* Outer Pulsing Aura */}
                    <circle
                      cx={px}
                      cy={py}
                      r={isSelected ? "18" : "12"}
                      fill={region.statusTone === "amber" ? "#FF6A3D22" : "#35D6C822"}
                      className="animate-ping"
                      style={{ animationDuration: "3s" }}
                    />
                    {/* Ring */}
                    <circle
                      cx={px}
                      cy={py}
                      r={isSelected ? "10" : "6"}
                      fill="#0B0D10"
                      stroke={region.statusTone === "amber" ? "#FF6A3D" : "#35D6C8"}
                      strokeWidth={isSelected ? "2.5" : "1.5"}
                    />
                    {/* Center Dot */}
                    <circle
                      cx={px}
                      cy={py}
                      r="3"
                      fill={region.statusTone === "amber" ? "#FF6A3D" : "#35D6C8"}
                    />
                  </g>
                );
              })}
            </svg>
          </div>

          {/* Bottom Scanner Status Overlay */}
          <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between rounded bg-ink/80 px-3 py-1.5 backdrop-blur border border-line text-[11px] font-mono text-text-muted">
            <span>Slice Index: {plane === "coronal" ? "C-148 / 256" : "A-092 / 256"}</span>
            <span className="text-teal">Voxel Res: 1.0mm³</span>
          </div>
        </div>

        {/* Selected Region Detail Inspector Panel (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="rounded-md border border-line bg-ink p-4 space-y-3">
            <div className="flex items-center justify-between">
              <span className="label-eyebrow text-teal">{selectedRegion.disease}</span>
              <span
                className={cn(
                  "inline-flex items-center gap-1 rounded px-2 py-0.5 font-mono text-[10px] font-medium uppercase tracking-wider",
                  selectedRegion.statusTone === "amber"
                    ? "bg-amber/10 text-amber border border-amber/30"
                    : "bg-teal/10 text-teal border border-teal/30"
                )}
              >
                {selectedRegion.status}
              </span>
            </div>

            <div>
              <h3 className="font-display text-lg font-medium text-text">
                {selectedRegion.name}
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-text-muted">
                {selectedRegion.description}
              </p>
            </div>

            {/* Metric Box */}
            <div className="grid grid-cols-2 gap-2 pt-2 border-t border-line">
              <div className="rounded bg-raised p-2.5">
                <span className="block font-mono text-[10px] text-text-faint uppercase">
                  {selectedRegion.metricLabel}
                </span>
                <span className="data-num text-sm font-semibold text-text mt-0.5 block">
                  {selectedRegion.metricValue}
                </span>
              </div>
              <div className="rounded bg-raised p-2.5">
                <span className="block font-mono text-[10px] text-text-faint uppercase">
                  Attribution Influence
                </span>
                <span className="data-num text-sm font-semibold text-teal mt-0.5 block">
                  High Impact
                </span>
              </div>
            </div>
          </div>

          {/* Quick Hotspot Selector Buttons */}
          <div>
            <p className="label-eyebrow mb-2">Anatomical Region Hotspots:</p>
            <div className="flex flex-wrap gap-2">
              {visibleRegions.map((r) => (
                <button
                  key={r.id}
                  onClick={() => setSelectedRegionId(r.id)}
                  className={cn(
                    "flex items-center gap-1.5 rounded border px-2.5 py-1 font-mono text-xs transition-all",
                    r.id === selectedRegion.id
                      ? "border-teal/50 bg-teal/10 text-teal font-medium"
                      : "border-line bg-raised/50 text-text-muted hover:border-line-soft hover:text-text"
                  )}
                >
                  <span
                    className={cn(
                      "h-1.5 w-1.5 rounded-full",
                      r.statusTone === "amber" ? "bg-amber" : "bg-teal"
                    )}
                  />
                  {r.name}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
