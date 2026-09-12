import { describe, expect, it } from "vitest";
import {
  MAX_CONFIDENCE,
  confidencePercent,
  formatConfidence,
  triageReasons,
} from "@/lib/utils";
import type { TriageEntry } from "@/lib/types";

function entry(flags: Partial<TriageEntry>): TriageEntry {
  return {
    patient_id: "p",
    patient_first_name: "Test",
    awaiting_sign_off: false,
    has_open_early_watch: false,
    has_worsening_trend: false,
    ...flags,
  };
}

describe("confidence display", () => {
  it("never exceeds the 0.92 ceiling", () => {
    expect(MAX_CONFIDENCE).toBe(0.92);
    expect(confidencePercent(0.97)).toBe(92);
    expect(confidencePercent(1)).toBe(92);
    expect(formatConfidence(0.999)).toBe("92%");
  });

  it("passes values under the ceiling through and floors at zero", () => {
    expect(confidencePercent(0.5)).toBe(50);
    expect(confidencePercent(0.92)).toBe(92);
    expect(confidencePercent(-0.2)).toBe(0);
  });
});

describe("triageReasons", () => {
  it("names reasons in ADR-006 ranking order", () => {
    const reasons = triageReasons(
      entry({
        awaiting_sign_off: true,
        has_open_early_watch: true,
        has_worsening_trend: true,
      })
    );
    expect(reasons.map((r) => r.key)).toEqual([
      "early_watch",
      "worsening",
      "sign_off",
    ]);
  });

  it("returns nothing for a row with no open signals", () => {
    expect(triageReasons(entry({}))).toEqual([]);
  });
});
