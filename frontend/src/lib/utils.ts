import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatConfidence(value: number): string {
  return `${Math.round(value * 100)}%`;
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export function stageLabel(stage: string): string {
  const map: Record<string, string> = {
    CN: "Cognitively Normal",
    MCI: "Mild Cognitive Impairment",
    MILD: "Mild",
    MODERATE: "Moderate",
    SEVERE: "Severe",
  };
  return map[stage] ?? stage;
}
