import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import type { Analysis, Patient, Visit } from "@/lib/types";

const VISIT: Visit = {
  id: "v1",
  patient_id: "p1",
  chief_complaint: "intermittent hand tremor",
  visit_date: "2026-09-01T10:00:00Z",
  status: "analyzed",
  created_at: "2026-09-01T10:00:00Z",
  updated_at: "2026-09-01T10:00:00Z",
};

const PATIENT = {
  id: "p1",
  first_name: "Demo",
  last_name: "Patient",
  dob: "1962-04-09",
  gender: "F",
  email: "demo@example.com",
  phone: [{ phone_number: "5551110000" }],
  address: "1 Example Street",
  blood_group: "O+",
  allergies: [],
  emergency_contact: "5550000000",
  doctor_id: "u1",
  doctor: { first_name: "Demo", last_name: "Clinician" },
  created_at: "2026-01-01T00:00:00Z",
  updated_at: "2026-01-01T00:00:00Z",
} as unknown as Patient;

function analysis(overrides: Partial<Analysis> = {}): Analysis {
  return {
    id: "a1",
    visit_id: "v1",
    model_name: "mock-reasoner",
    provider_mode: "simulated",
    pipeline_note: "pipeline complete, evidence retrieval simulated",
    disclaimer: "Decision support only.",
    findings: [],
    generated_at: "2026-09-01T10:05:00Z",
    reviewed_at: null,
    created_at: "2026-09-01T10:05:00Z",
    updated_at: "2026-09-01T10:05:00Z",
    ...overrides,
  };
}

const latestAnalysis = vi.fn<(visitId: string) => Promise<Analysis>>();

vi.mock("next/navigation", () => ({
  useParams: () => ({ id: "p1" }),
  useSearchParams: () => new URLSearchParams(),
}));

vi.mock("next/link", () => ({
  default: ({ href, children }: { href: string; children: React.ReactNode }) => (
    <a href={href}>{children}</a>
  ),
}));

vi.mock("@/hooks/use-patients", () => {
  const settled = <T,>(data: T) => ({
    data,
    isLoading: false,
    isInitialLoad: false,
    error: null,
    refetch: () => {},
  });
  return {
    usePatient: () => settled(PATIENT),
    usePatientVisits: () =>
      settled({
        items: [VISIT],
        pagination: { page: 1, page_size: 20, total_pages: 1, total_records: 1 },
      }),
  };
});

vi.mock("@/lib/endpoints", () => ({
  visits: {
    latestAnalysis: (visitId: string) => latestAnalysis(visitId),
    runAnalysis: vi.fn(),
    getScan: vi.fn(() => Promise.reject(new Error("Not found"))),
  },
  analyses: { signOff: vi.fn() },
  reports: { list: vi.fn(), generate: vi.fn(), download: vi.fn() },
}));

const { default: PatientDetailPage } = await import(
  "@/app/dashboard/patients/[id]/page"
);

describe("analysis view", () => {
  beforeEach(() => latestAnalysis.mockReset());

  it("shows provider mode, pipeline note and disclaimer on the analysis", async () => {
    latestAnalysis.mockResolvedValue(analysis());
    render(<PatientDetailPage />);

    expect(
      await screen.findByText("pipeline complete, evidence retrieval simulated")
    ).toBeVisible();
    expect(screen.getByText("simulated")).toBeVisible();
    expect(screen.getByText("Decision support only.")).toBeVisible();
  });

  it("keeps the report unreachable until the analysis is signed off", async () => {
    latestAnalysis.mockResolvedValue(analysis({ reviewed_at: null }));
    render(<PatientDetailPage />);

    const download = await screen.findByRole("button", { name: /download report/i });
    expect(download).toBeDisabled();
    expect(screen.getByRole("button", { name: /sign off/i })).toBeEnabled();
  });

  it("enables the report once signed off", async () => {
    latestAnalysis.mockResolvedValue(
      analysis({ reviewed_at: "2026-09-02T09:00:00Z", reviewed_by_id: "u1" })
    );
    render(<PatientDetailPage />);

    const download = await screen.findByRole("button", { name: /download report/i });
    expect(download).toBeEnabled();
    expect(screen.queryByRole("button", { name: /^sign off$/i })).not.toBeInTheDocument();
  });
});
