/**
 * Contribution bars for the landing page's sample cases.
 *
 * Landing-scoped on purpose: these regions are illustrative copy, not an API
 * shape. The live analysis view renders ranked findings from the backend
 * instead — see `@/components/analysis-findings`.
 */

export type DemoDiseaseLabel = "healthy" | "alzheimers" | "parkinsons";

export type DemoDiseaseStage = "CN" | "MCI" | "MILD" | "MODERATE" | "SEVERE";

export interface DemoRegion {
  label: string;
  contribution: number;
}

export function RegionBars({ regions }: { regions: DemoRegion[] }) {
  const sorted = [...regions].sort((a, b) => b.contribution - a.contribution);
  return (
    <div className="space-y-3">
      {sorted.map((region) => (
        <div key={region.label}>
          <div className="mb-1 flex items-center justify-between text-[13px]">
            <span className="text-text-muted">{region.label}</span>
            <span className="data-num text-text-faint">
              {Math.round(region.contribution * 100)}%
            </span>
          </div>
          <div className="h-1.5 w-full overflow-hidden rounded-full bg-raised">
            <div
              className="h-full rounded-full bg-gradient-to-r from-indigo to-amber"
              style={{ width: `${region.contribution * 100}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
