"use client";

import { useState } from "react";
import { ChevronDown, Info, Sparkles } from "@/components/icons";
import { cn, confidencePercent } from "@/lib/utils";
import type { Finding, LikelihoodBand } from "@/lib/types";

const BAND_TONE: Record<LikelihoodBand, string> = {
  high: "border-amber/30 bg-amber-soft text-amber",
  moderate: "border-indigo/30 bg-indigo-soft text-indigo",
  low: "border-line bg-raised text-text-muted",
};

const BAR_TONE: Record<LikelihoodBand, string> = {
  high: "bg-amber",
  moderate: "bg-indigo",
  low: "bg-text-faint",
};

/**
 * Ranked findings from one analysis.
 *
 * The likelihood band, not the raw confidence, is what the clinician is
 * meant to read first — the number is shown next to it because hiding it
 * would be worse, but the band carries the colour.
 */
export function AnalysisFindings({ findings }: { findings: Finding[] }) {
  const ranked = [...findings].sort((a, b) => a.rank - b.rank);
  const differentials = ranked.filter(
    (f) => f.category === "differential_diagnosis"
  );
  const earlyWatch = ranked.filter((f) => f.category === "early_watch");

  return (
    <div className="space-y-6">
      {differentials.length > 0 && (
        <FindingGroup title="Differential diagnoses" findings={differentials} />
      )}
      {earlyWatch.length > 0 && (
        <FindingGroup
          title="Early watch"
          hint="Signals worth tracking that do not yet meet a diagnostic threshold."
          findings={earlyWatch}
        />
      )}
    </div>
  );
}

function FindingGroup({
  title,
  hint,
  findings,
}: {
  title: string;
  hint?: string;
  findings: Finding[];
}) {
  return (
    <section>
      <p className="label-eyebrow mb-1">{title}</p>
      {hint && <p className="mb-3 text-[12px] text-text-faint">{hint}</p>}
      <div className="space-y-2">
        {findings.map((finding, index) => (
          <FindingRow key={finding.id} finding={finding} index={index} />
        ))}
      </div>
    </section>
  );
}

function FindingRow({ finding, index }: { finding: Finding; index: number }) {
  const [open, setOpen] = useState(false);
  const evidence = finding.evidence ?? [];
  const pct = confidencePercent(finding.confidence);

  return (
    <div
      className="animate-fade-up rounded-md border border-line bg-raised/40"
      style={{ animationDelay: `${Math.min(index, 6) * 40}ms` }}
    >
      <button
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        className={cn(
          "flex w-full items-start gap-3 rounded-md px-4 py-3 text-left",
          "transition-[background-color,transform] duration-150 ease-out",
          "hover:bg-raised/70 active:scale-[0.995]"
        )}
      >
        {/* Position in the ranked list, not `finding.rank` -- the backend
            ranks from zero and "0." reads as a bug in a numbered list. */}
        <span className="data-num mt-0.5 w-5 shrink-0 text-[12px] text-text-faint">
          {index + 1}
        </span>

        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <p className="text-sm text-text">{finding.name}</p>
            <span
              className={cn(
                "rounded-sm border px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wide",
                BAND_TONE[finding.likelihood_band]
              )}
            >
              {finding.likelihood_band}
            </span>
          </div>

          <div className="mt-2 flex items-center gap-2.5">
            <div className="h-1 w-full max-w-[200px] overflow-hidden rounded-full bg-line">
              <div
                className={cn(
                  "h-full rounded-full transition-[width] duration-500 ease-out",
                  BAR_TONE[finding.likelihood_band]
                )}
                style={{ width: `${pct}%` }}
              />
            </div>
            <span className="data-num text-[11px] text-text-faint">{pct}%</span>
          </div>
        </div>

        <ChevronDown
          className={cn(
            "mt-0.5 h-4 w-4 shrink-0 text-text-faint",
            "transition-transform duration-200 ease-out",
            open && "rotate-180"
          )}
        />
      </button>

      {open && (
        <div className="border-t border-line px-4 py-3.5 text-[13px]">
          <p className="leading-relaxed text-text-muted">{finding.explanation}</p>

          {finding.supporting_findings.length > 0 && (
            <PointList
              label="Supporting"
              tone="teal"
              items={finding.supporting_findings}
            />
          )}
          {finding.contradicting_findings.length > 0 && (
            <PointList
              label="Contradicting"
              tone="amber"
              items={finding.contradicting_findings}
            />
          )}

          {evidence.length > 0 && (
            <div className="mt-4">
              <p className="label-eyebrow mb-2 flex items-center gap-1.5">
                <Sparkles className="h-3 w-3" />
                Evidence
              </p>
              <ul className="space-y-2">
                {evidence.map((item, i) => (
                  <li
                    key={`${item.citation}-${i}`}
                    className="rounded border border-line bg-ink/40 px-3 py-2"
                  >
                    <p className="leading-relaxed text-text-muted">
                      &ldquo;{item.relevant_passage}&rdquo;
                    </p>
                    <p className="mt-1.5 text-[11px] text-text-faint">
                      {item.source_url ? (
                        <a
                          href={item.source_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-indigo hover:underline"
                        >
                          {item.citation}
                        </a>
                      ) : (
                        item.citation
                      )}
                      {item.published_year ? ` · ${item.published_year}` : ""}
                      {item.source ? ` · ${item.source}` : ""}
                    </p>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {evidence.length === 0 && (
            <p className="mt-3 flex items-center gap-1.5 text-[12px] text-text-faint">
              <Info className="h-3.5 w-3.5" />
              No citations were attached to this finding.
            </p>
          )}
        </div>
      )}
    </div>
  );
}

function PointList({
  label,
  tone,
  items,
}: {
  label: string;
  tone: "teal" | "amber";
  items: string[];
}) {
  return (
    <div className="mt-3">
      <p
        className={cn(
          "label-eyebrow mb-1.5",
          tone === "teal" ? "text-teal" : "text-amber"
        )}
      >
        {label}
      </p>
      <ul className="space-y-1">
        {items.map((item, i) => (
          <li key={i} className="flex gap-2 text-text-muted">
            <span
              className={cn(
                "mt-[7px] h-1 w-1 shrink-0 rounded-full",
                tone === "teal" ? "bg-teal" : "bg-amber"
              )}
            />
            <span className="leading-relaxed">{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
