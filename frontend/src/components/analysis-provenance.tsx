import { Info } from "@/components/icons";
import { Badge } from "@/components/ui/badge";
import type { Analysis } from "@/lib/types";

/**
 * What produced this analysis, and what it is not.
 *
 * ADR-006 decision 9: provenance is stated per analysis, not per
 * environment. A staged MRI region with a percentage looks like measurement,
 * so the line saying which parts were simulated sits above the findings and
 * is never tucked into a tooltip -- it is the thing a clinician (or a demo
 * audience) needs in order to read the rest of the card correctly.
 */
export function AnalysisProvenance({
  analysis,
}: {
  analysis: Pick<Analysis, "provider_mode" | "pipeline_note" | "disclaimer">;
}) {
  const isSimulated = analysis.provider_mode === "simulated";

  return (
    <section
      aria-label="Analysis provenance"
      className="mb-5 rounded-md border border-line bg-raised/40 px-4 py-3"
    >
      <div className="flex flex-wrap items-center gap-2">
        <p className="label-eyebrow">Provenance</p>
        <Badge tone={isSimulated ? "amber" : "indigo"}>
          {analysis.provider_mode}
        </Badge>
      </div>
      <p className="mt-1.5 text-[13px] leading-relaxed text-text-muted">
        {analysis.pipeline_note}
      </p>
      <p className="mt-2.5 flex gap-1.5 border-t border-line pt-2.5 text-[12px] leading-relaxed text-text-muted">
        <Info className="mt-0.5 h-3.5 w-3.5 shrink-0" />
        <span>{analysis.disclaimer}</span>
      </p>
    </section>
  );
}
