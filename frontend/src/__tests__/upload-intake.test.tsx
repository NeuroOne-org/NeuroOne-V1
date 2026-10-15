import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

const calls: string[] = [];
const push = vi.fn();
const createPatient = vi.fn();
const createVisit = vi.fn();
const uploadScan = vi.fn();
const runAnalysis = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push }),
}));

vi.mock("@/lib/endpoints", () => ({
  patients: {
    create: (...args: unknown[]) => {
      calls.push("createPatient");
      return createPatient(...args);
    },
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

const { default: UploadPage } = await import("@/app/dashboard/upload/page");

function fillForm(container: HTMLElement) {
  fireEvent.change(container.querySelector("#first_name")!, {
    target: { value: "Jane" },
  });
  fireEvent.change(container.querySelector("#dob")!, {
    target: { value: "1990-01-01" },
  });
  // Pick by the visible label, so the test sends whatever value the option
  // actually carries rather than one the test assumes.
  const gender = container.querySelector("#gender") as HTMLSelectElement;
  const female = Array.from(gender.options).find((o) => o.text === "Female")!;
  fireEvent.change(gender, { target: { value: female.value } });
  fireEvent.change(container.querySelector("#email")!, {
    target: { value: "jane@example.com" },
  });
  fireEvent.change(container.querySelector("#phone")!, {
    target: { value: "+1 555 0100" },
  });
  fireEvent.change(container.querySelector("#address")!, {
    target: { value: "1 Main St" },
  });
  fireEvent.change(container.querySelector("#blood_group")!, {
    target: { value: "O+" },
  });
  fireEvent.change(container.querySelector("#emergency_contact")!, {
    target: { value: "John, +1 555 0101" },
  });
  fireEvent.change(container.querySelector("#chief_complaint")!, {
    target: { value: "Progressive memory loss" },
  });
}

function submit() {
  fireEvent.click(
    screen.getByRole("button", { name: /create and analyse|retry/i })
  );
}

describe("Upload intake", () => {
  beforeEach(() => {
    calls.length = 0;
    push.mockReset();
    createPatient.mockReset().mockResolvedValue({ id: "p9" });
    createVisit.mockReset().mockResolvedValue({ id: "v9" });
    uploadScan.mockReset().mockResolvedValue({ id: "s9" });
    runAnalysis.mockReset().mockResolvedValue({ id: "a9" });
  });

  it("creates the patient and visit, then analyses without a scan", async () => {
    const { container } = render(<UploadPage />);
    fillForm(container);
    submit();

    await waitFor(() =>
      expect(push).toHaveBeenCalledWith("/dashboard/patients/p9")
    );
    expect(calls).toEqual(["createPatient", "createVisit", "runAnalysis"]);
  });

  it("records structured symptoms with the first visit (FR-03)", async () => {
    const { container } = render(<UploadPage />);
    fillForm(container);
    fireEvent.click(screen.getByRole("button", { name: /add symptom/i }));
    fireEvent.change(screen.getByLabelText("Symptom"), {
      target: { value: "memory loss" },
    });
    fireEvent.change(screen.getByLabelText("Severity"), {
      target: { value: "6" },
    });
    fireEvent.change(screen.getByLabelText("Duration (days)"), {
      target: { value: "90" },
    });
    submit();

    await waitFor(() => expect(createVisit).toHaveBeenCalled());
    expect(createVisit.mock.calls[0][1].symptoms).toEqual([
      {
        symptom_name: "memory loss",
        severity: 6,
        onset: null,
        duration_days: 90,
        observation: null,
      },
    ]);
  });

  it("sends gender as the single-letter code the backend stores", async () => {
    const { container } = render(<UploadPage />);
    fillForm(container);
    submit();

    await waitFor(() => expect(createPatient).toHaveBeenCalled());
    expect(createPatient).toHaveBeenCalledWith(
      expect.objectContaining({ gender: "F" })
    );
  });

  it("uploads an attached scan between creating the visit and analysing", async () => {
    const { container } = render(<UploadPage />);
    fillForm(container);
    const input = container.querySelector(
      'input[type="file"]'
    ) as HTMLInputElement;
    fireEvent.change(input, {
      target: { files: [new File(["scan"], "brain.nii")] },
    });
    submit();

    await waitFor(() => expect(push).toHaveBeenCalled());
    expect(calls).toEqual([
      "createPatient",
      "createVisit",
      "uploadScan",
      "runAnalysis",
    ]);
  });

  it("retries a failed analysis without creating a second patient or visit", async () => {
    runAnalysis.mockRejectedValueOnce(new Error("Pipeline unavailable"));
    const { container } = render(<UploadPage />);
    fillForm(container);
    submit();

    expect(await screen.findByText(/earlier steps were already saved/i)).toBeInTheDocument();
    expect(calls).toEqual(["createPatient", "createVisit", "runAnalysis"]);

    submit();

    await waitFor(() => expect(push).toHaveBeenCalledWith("/dashboard/patients/p9"));
    expect(calls).toEqual([
      "createPatient",
      "createVisit",
      "runAnalysis",
      "runAnalysis",
    ]);
    expect(createPatient).toHaveBeenCalledTimes(1);
    expect(createVisit).toHaveBeenCalledTimes(1);
  });

  it("retries a failed scan upload without re-attaching the scan a second time", async () => {
    uploadScan.mockRejectedValueOnce(new Error("Storage unavailable"));
    const { container } = render(<UploadPage />);
    fillForm(container);
    const input = container.querySelector(
      'input[type="file"]'
    ) as HTMLInputElement;
    fireEvent.change(input, {
      target: { files: [new File(["scan"], "brain.nii")] },
    });
    submit();

    expect(await screen.findByText(/earlier steps were already saved/i)).toBeInTheDocument();
    expect(calls).toEqual(["createPatient", "createVisit", "uploadScan"]);

    submit();

    await waitFor(() => expect(push).toHaveBeenCalledWith("/dashboard/patients/p9"));
    expect(calls).toEqual([
      "createPatient",
      "createVisit",
      "uploadScan",
      "uploadScan",
      "runAnalysis",
    ]);
    expect(createPatient).toHaveBeenCalledTimes(1);
    expect(createVisit).toHaveBeenCalledTimes(1);
  });

  it("does not create a visit when patient creation fails", async () => {
    createPatient.mockRejectedValue(new Error("Patient rejected"));
    const { container } = render(<UploadPage />);
    fillForm(container);
    submit();

    await waitFor(() => expect(calls).toEqual(["createPatient"]));
    expect(push).not.toHaveBeenCalled();
  });
});
