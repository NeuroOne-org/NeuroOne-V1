import type { PredictionRegion } from "@/lib/types";

export function RegionBars({ regions }: { regions: PredictionRegion[] }) {
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
