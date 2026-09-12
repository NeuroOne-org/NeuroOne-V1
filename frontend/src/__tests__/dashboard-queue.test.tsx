import { render, screen, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import type { TriageEntry } from "@/lib/types";

// Deliberately NOT the order a "worst first" client sort would produce: the
// early-watch-only row leads, ahead of a worsening-only row. The page must
// keep it that way.
const SERVER_ORDER: TriageEntry[] = [
  {
    patient_id: "p-early",
    patient_first_name: "Ada",
    patient_last_name: "Early",
    has_open_early_watch: true,
    has_worsening_trend: false,
    awaiting_sign_off: false,
  },
  {
    patient_id: "p-worse",
    patient_first_name: "Ben",
    patient_last_name: "Worse",
    has_open_early_watch: false,
    has_worsening_trend: true,
    awaiting_sign_off: true,
  },
  {
    patient_id: "p-sign",
    patient_first_name: "Cy",
    patient_last_name: "Sign",
    has_open_early_watch: false,
    has_worsening_trend: false,
    awaiting_sign_off: true,
  },
  {
    patient_id: "p-quiet",
    patient_first_name: "Di",
    patient_last_name: "Quiet",
    has_open_early_watch: false,
    has_worsening_trend: false,
    awaiting_sign_off: false,
  },
];

vi.mock("next/link", () => ({
  default: ({
    href,
    children,
    ...rest
  }: {
    href: string;
    children: React.ReactNode;
  }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

vi.mock("@/components/auth-provider", () => ({
  useAuth: () => ({ user: { first_name: "Test" } }),
}));

vi.mock("@/hooks/use-patients", () => ({
  QUEUE_FETCH_LIMIT: 100,
  useTriageQueue: () => ({
    data: {
      items: SERVER_ORDER,
      pagination: {
        page: 1,
        page_size: 100,
        total_pages: 1,
        total_records: SERVER_ORDER.length,
      },
    },
    isLoading: false,
    isInitialLoad: false,
    error: null,
    refetch: () => {},
  }),
}));

const { default: DashboardPage } = await import("@/app/dashboard/page");

describe("triage queue", () => {
  it("renders rows in server order, without re-sorting", () => {
    render(<DashboardPage />);

    const rows = within(screen.getByRole("table")).getAllByRole("row").slice(1);
    const names = rows.map(
      (row) => within(row).getAllByRole("paragraph")[0]?.textContent
    );

    expect(names).toEqual(["Ada Early", "Ben Worse", "Cy Sign", "Di Quiet"]);
  });

  it("labels each row's reasons in ranking order", () => {
    render(<DashboardPage />);

    const rows = within(screen.getByRole("table")).getAllByRole("row").slice(1);
    const benSignals = within(rows[1]).getAllByText(/Worsening|Awaiting sign-off/);

    expect(benSignals.map((el) => el.textContent)).toEqual([
      "Worsening",
      "Awaiting sign-off",
    ]);
    expect(within(rows[3]).getByText("No open signals")).toBeInTheDocument();
  });
});
