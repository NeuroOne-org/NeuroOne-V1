import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AnalysisFindings } from "@/components/analysis-findings";
import { AnalysisProvenance } from "@/components/analysis-provenance";
import type { Finding } from "@/lib/types";

function finding(overrides: Partial<Finding>): Finding {
  return {
    id: "f1",
    rank: 0,
    name: "Candidate",
    category: "differential_diagnosis",
    confidence: 0.5,
    likelihood_band: "moderate",
    explanation: "",
    supporting_findings: [],
    contradicting_findings: [],
    ...overrides,
  };
}

describe("AnalysisProvenance", () => {
  it("shows provider mode, pipeline note and disclaimer together", () => {
    render(
      <AnalysisProvenance
        analysis={{
          provider_mode: "simulated",
          pipeline_note:
            "pipeline complete, reasoning simulated, evidence retrieval simulated",
          disclaimer: "Decision support only. Not a diagnosis.",
        }}
      />
    );

    expect(screen.getByText("simulated")).toBeVisible();
    expect(
      screen.getByText(
        "pipeline complete, reasoning simulated, evidence retrieval simulated"
      )
    ).toBeVisible();
    expect(
      screen.getByText("Decision support only. Not a diagnosis.")
    ).toBeVisible();
  });
});

describe("AnalysisFindings", () => {
  it("never displays a confidence above 92%", () => {
    render(
      <AnalysisFindings
        findings={[
          finding({ id: "a", rank: 0, name: "Over ceiling", confidence: 0.97 }),
          finding({ id: "b", rank: 1, name: "Under ceiling", confidence: 0.41 }),
        ]}
      />
    );

    expect(screen.getByText("92%")).toBeInTheDocument();
    expect(screen.getByText("41%")).toBeInTheDocument();
    expect(screen.queryByText(/\b(9[3-9]|100)%/)).not.toBeInTheDocument();
  });

  it("keeps early-watch signals apart from the differential", () => {
    render(
      <AnalysisFindings
        findings={[
          finding({ id: "a", name: "Differential one" }),
          finding({ id: "b", name: "Quiet signal", category: "early_watch" }),
        ]}
      />
    );

    expect(screen.getByText("Differential diagnoses")).toBeInTheDocument();
    expect(screen.getByText("Early watch")).toBeInTheDocument();
  });
});
