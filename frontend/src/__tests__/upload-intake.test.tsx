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
  fireEvent.change(container.querySelector("#gender")!, {
    target: { value: "female" },
  });
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
