import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import type { Patient, TriageEntry } from "@/lib/types";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * No displayed confidence may exceed this (ADR-006 constraints). It mirrors
 * the backend's `MAX_CONFIDENCE`, which already enforces it -- holding the
 * display to it too means a contract regression can never render as
 * certainty on a clinician's screen.
 */
export const MAX_CONFIDENCE = 0.92;

/** A confidence as a whole percentage, held inside [0, MAX_CONFIDENCE]. */
export function confidencePercent(value: number): number {
  const bounded = Math.min(Math.max(value, 0), MAX_CONFIDENCE);
  return Math.round(bounded * 100);
}

export function formatConfidence(value: number): string {
  return `${confidencePercent(value)}%`;
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export function formatDateTime(iso: string): string {
  return new Date(iso).toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

/**
 * "3d ago" rather than a date, for the one column where recency is the
 * point. Falls back to an absolute date past a week, where "23d ago" stops
 * being easier to read than the date itself.
 */
export function formatRelative(iso: string): string {
  const then = new Date(iso).getTime();
  const minutes = Math.floor((Date.now() - then) / 60000);

  if (minutes < 1) return "just now";
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days <= 7) return `${days}d ago`;
  return formatDate(iso);
}

/** The backend stores names in two nullable halves; the UI needs one string. */
export function fullName(
  person: Pick<Patient, "first_name" | "last_name">
): string {
  return [person.first_name, person.last_name].filter(Boolean).join(" ").trim();
}

export function triageName(entry: TriageEntry): string {
  return [entry.patient_first_name, entry.patient_last_name]
    .filter(Boolean)
    .join(" ")
    .trim();
}

export function initials(name: string): string {
  return (
    name
      .split(/\s+/)
      .filter(Boolean)
      .map((part) => part[0])
      .slice(0, 2)
      .join("")
      .toUpperCase() || "?"
  );
}

export function ageFromDob(dob: string): number | null {
  const born = new Date(dob);
  if (Number.isNaN(born.getTime())) return null;
  const now = new Date();
  let age = now.getFullYear() - born.getFullYear();
  const monthDelta = now.getMonth() - born.getMonth();
  if (monthDelta < 0 || (monthDelta === 0 && now.getDate() < born.getDate())) {
    age -= 1;
  }
  return age >= 0 ? age : null;
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

export function visitStatusLabel(status: string): string {
  const map: Record<string, string> = {
    draft: "Draft",
    submitted: "Submitted",
    analyzed: "Analyzed",
    closed: "Closed",
  };
  return map[status] ?? status;
}

export type TriageReasonKey = "early_watch" | "worsening" | "sign_off";

export interface TriageReason {
  key: TriageReasonKey;
  label: string;
}

/**
 * Why a queue row is where it is, most urgent first.
 *
 * The backend sends three flags and no score, and has already ranked the
 * queue on them in exactly this order (ADR-006 decision 7). This only names
 * the reasons; it never orders rows, because a client-side sort would be a
 * second, different opinion on the server's clinical ranking.
 */
export function triageReasons(entry: TriageEntry): TriageReason[] {
  const reasons: TriageReason[] = [];
  if (entry.has_open_early_watch) {
    reasons.push({ key: "early_watch", label: "Early watch" });
  }
  if (entry.has_worsening_trend) {
    reasons.push({ key: "worsening", label: "Worsening" });
  }
  if (entry.awaiting_sign_off) {
    reasons.push({ key: "sign_off", label: "Awaiting sign-off" });
  }
  return reasons;
}
