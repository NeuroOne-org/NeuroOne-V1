import { cn } from "@/lib/utils";

type Tone = "neutral" | "teal" | "amber" | "indigo";

const toneClasses: Record<Tone, string> = {
  neutral: "bg-raised text-text-muted border-line",
  teal: "bg-teal-soft text-teal border-teal/30",
  amber: "bg-amber-soft text-amber border-amber/30",
  indigo: "bg-indigo-soft text-indigo border-indigo/30",
};

export function Badge({
  tone = "neutral",
  children,
}: {
  tone?: Tone;
  children: React.ReactNode;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-sm border px-2 py-0.5 text-[11px] font-mono uppercase tracking-wide",
        toneClasses[tone]
      )}
    >
      {children}
    </span>
  );
}
