import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

const calls: string[] = [];
const push = vi.fn();
const createVisit = vi.fn();
const uploadScan = vi.fn();
const runAnalysis = vi.fn();

vi.mock("next/navigation", () => ({
  useParams: () => ({ id: "p1" }),
  useRouter: () => ({ push }),
}));

vi.mock("next/link", () => ({
  default: ({ href, children }: { href: string; children: React.ReactNode }) => (
    <a href={href}>{children}</a>
  ),
}));

vi.mock("@/hooks/use-patients", () => ({
  usePatient: () => ({
    data: { first_name: "Grace", last_name: "Adeyemi" },
    isLoading: false,
    isInitialLoad: false,
    error: null,
    refetch: () => {},
  }),
}));

vi.mock("@/lib/endpoints", () => ({
  patients: {
    createVisit: (...args: unknown[]) => {
      calls.push("createVisit");
      return createVisit(...args);
    },
  },
  visits: {
    uploadScan: (...args: unknown[]) => {
      calls.push("uploadScan");
      return uploadScan(...args);
    },
    runAnalysis: (...args: unknown[]) => {
      calls.push("runAnalysis");
      return runAnalysis(...args);
    },
  },
}));

const { default: NewVisitPage } = await import(
  "@/app/dashboard/patients/[id]/visits/new/page"
);

function fillForm() {
  fireEvent.change(screen.getByLabelText("Chief complaint"), {
    target: { value: "forgetfulness getting worse" },
  });
  fireEvent.change(screen.getByLabelText("Symptom"), {
    target: { value: "memory loss" },
  });
  fireEvent.change(screen.getByLabelText("Severity"), {
    target: { value: "4" },
  });
}

function submit() {
  fireEvent.click(screen.getByRole("button", { name: /save and analyse|retry/i }));
}

describe("New visit", () => {
  beforeEach(() => {
    calls.length = 0;
    push.mockReset();
    createVisit.mockReset().mockResolvedValue({ id: "v9" });
    uploadScan.mockReset().mockResolvedValue({ id: "s9" });
    runAnalysis.mockReset().mockResolvedValue({ id: "a9" });
  });

  it("creates the visit with its symptoms inline, then analyses it", async () => {
    render(<NewVisitPage />);
    fillForm();
    submit();

    await waitFor(() =>
      expect(push).toHaveBeenCalledWith("/dashboard/patients/p1?visit=v9")
    );
    expect(calls).toEqual(["createVisit", "runAnalysis"]);
    expect(createVisit).toHaveBeenCalledWith("p1", {
      chief_complaint: "forgetfulness getting worse",
      history: null,
      notes: null,
      status: "submitted",
      symptoms: [{ symptom_name: "memory loss", severity: 4, onset: null }],
    });
    expect(runAnalysis).toHaveBeenCalledWith("v9");
  });

  it("uploads an attached scan between creating and analysing", async () => {
    const { container } = render(<NewVisitPage />);
    fillForm();
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    fireEvent.change(input, {
      target: { files: [new File(["scan"], "follow-up.nii")] },
    });
    submit();

    await waitFor(() => expect(push).toHaveBeenCalled());
    expect(calls).toEqual(["createVisit", "uploadScan", "runAnalysis"]);
  });

  it("does not analyse when the visit could not be created", async () => {
    createVisit.mockRejectedValue(new Error("Visit rejected"));
    render(<NewVisitPage />);
    fillForm();
    submit();

    expect(await screen.findByRole("alert")).toBeInTheDocument();
    expect(calls).toEqual(["createVisit"]);
    expect(push).not.toHaveBeenCalled();
  });

  it("retries a failed analysis without creating a second visit", async () => {
    runAnalysis.mockRejectedValueOnce(new Error("Pipeline unavailable"));
    render(<NewVisitPage />);
    fillForm();
    submit();

    expect(await screen.findByRole("alert")).toHaveTextContent(/visit itself was saved/i);
    submit();

    await waitFor(() => expect(push).toHaveBeenCalled());
    expect(calls).toEqual(["createVisit", "runAnalysis", "runAnalysis"]);
  });

  it("rejects a severity outside 1-10 before calling the API", async () => {
    render(<NewVisitPage />);
    fillForm();
    fireEvent.change(screen.getByLabelText("Severity"), { target: { value: "11" } });
    submit();

    await waitFor(() => expect(screen.getByText(/1 to 10/i)).toBeInTheDocument());
    expect(calls).toEqual([]);
  });
});
