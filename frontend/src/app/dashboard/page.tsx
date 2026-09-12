"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import {
  ArrowRight,
  CircleCheck,
  Clock,
  Eye,
  ListCheck,
  Plus,
  Sparkles,
  TrendingDown,
} from "@/components/icons";
import { Button } from "@/components/ui/button";
import { Card, CardHeader } from "@/components/ui/card";
import { EmptyState, ErrorState, Pager, TableSkeleton } from "@/components/ui/state";
import {
  QueueFilterCards,
  type FilterCard,
  type QueueFilter,
} from "@/components/queue-filter-cards";
import { useAuth } from "@/components/auth-provider";
import { QUEUE_FETCH_LIMIT, useTriageQueue } from "@/hooks/use-patients";
import {
  cn,
  formatRelative,
  initials,
  triageName,
  triageUrgency,
} from "@/lib/utils";
import type { TriageEntry } from "@/lib/types";

const PAGE_SIZE = 8;

function matchesFilter(entry: TriageEntry, filter: QueueFilter): boolean {
  switch (filter) {
    case "sign_off":
      return entry.awaiting_sign_off;
    case "worsening":
      return entry.has_worsening_trend;
    case "early_watch":
      return entry.has_open_early_watch;
    default:
      return true;
  }
}

export default function DashboardPage() {
  const { user } = useAuth();
  const [filter, setFilter] = useState<QueueFilter>("all");
  const [page, setPage] = useState(1);

  const queue = useTriageQueue();
  const entries = useMemo(() => queue.data?.items ?? [], [queue.data]);
  const totalRecords = queue.data?.pagination.total_records;

  const counts = useMemo(
    () => ({
      all: entries.length,
      sign_off: entries.filter((e) => e.awaiting_sign_off).length,
      worsening: entries.filter((e) => e.has_worsening_trend).length,
      early_watch: entries.filter((e) => e.has_open_early_watch).length,
    }),
    [entries]
  );

  // Worst first. The backend sends no score, so `triageUrgency` is the whole
  // ordering rule; ties fall back to the most recently analysed.
  const ranked = useMemo(
    () =>
      [...entries].sort((a, b) => {
        const byUrgency = triageUrgency(b) - triageUrgency(a);
        if (byUrgency !== 0) return byUrgency;
        return (
          new Date(b.latest_analysis_generated_at ?? 0).getTime() -
          new Date(a.latest_analysis_generated_at ?? 0).getTime()
        );
      }),
    [entries]
  );

  const filtered = useMemo(
    () => ranked.filter((entry) => matchesFilter(entry, filter)),
    [ranked, filter]
  );

  // Changing the filter while on page 3 of the old result set looks broken.
  useEffect(() => setPage(1), [filter]);

  const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const safePage = Math.min(page, pageCount);
  const visible = filtered.slice(
    (safePage - 1) * PAGE_SIZE,
    safePage * PAGE_SIZE
  );

  const isReady = Boolean(queue.data) && !queue.error;

  const cards: FilterCard[] = [
    {
      key: "all",
      icon: ListCheck,
      title: "Open cases",
      count: isReady ? counts.all : undefined,
      description: "Everything in your queue",
      accentVar: "--indigo",
    },
    {
      key: "worsening",
      icon: TrendingDown,
      title: "Worsening",
      count: isReady ? counts.worsening : undefined,
      description: "Trending the wrong way",
      accentVar: "--amber",
    },
    {
      key: "sign_off",
      icon: Clock,
      title: "Awaiting sign-off",
      count: isReady ? counts.sign_off : undefined,
      description: "Analysed, needs you",
      accentVar: "--indigo",
    },
    {
      key: "early_watch",
      icon: Sparkles,
      title: "Early watch",
      count: isReady ? counts.early_watch : undefined,
      description: "Worth keeping an eye on",
      accentVar: "--teal",
    },
  ];

  return (
    <div className="mx-auto max-w-6xl">
      <header className="mb-7 flex flex-wrap items-end justify-between gap-4">
        <div>
          <TodayLine />
          <h1 className="font-display text-2xl font-medium text-text">
            Welcome back{user ? `, ${user.first_name}` : ""}
          </h1>
          <p className="mt-1.5 max-w-xl text-sm leading-relaxed text-text-muted">
            {summarise({
              isLoading: queue.isLoading && queue.isInitialLoad,
              hasError: Boolean(queue.error),
              counts,
              topName: ranked[0] ? triageName(ranked[0]) : null,
            })}
          </p>
        </div>
        <Link href="/dashboard/upload">
          <Button size="md">
            <Plus className="h-4 w-4" />
            New intake
          </Button>
        </Link>
      </header>

      <div className="mb-6">
        <QueueFilterCards cards={cards} active={filter} onChange={setFilter} />
        {totalRecords !== undefined && totalRecords > QUEUE_FETCH_LIMIT && (
          <p className="mt-2.5 text-[12px] text-text-faint">
            Counts cover the {QUEUE_FETCH_LIMIT} most urgent of {totalRecords}{" "}
            open cases.
          </p>
        )}
      </div>

      <Card>
        <CardHeader
          eyebrow={filterEyebrow(filter)}
          title="Cases to review"
          action={
            filter !== "all" && (
              <button
                onClick={() => setFilter("all")}
                className={cn(
                  "rounded border border-line px-2.5 py-1 text-[12px] text-text-muted",
                  "transition-[background-color,border-color,color,transform] duration-150 ease-out",
                  "hover:border-text-faint hover:bg-raised hover:text-text active:scale-[0.96]"
                )}
              >
                Show all
              </button>
            )
          }
        />

        {queue.isInitialLoad && queue.isLoading ? (
          <TableSkeleton rows={6} cols={4} />
        ) : queue.error ? (
          <ErrorState message={queue.error} onRetry={queue.refetch} />
        ) : visible.length === 0 ? (
          <EmptyState
            icon={CircleCheck}
            title={
              entries.length === 0
                ? "Your queue is clear"
                : "Nothing under this filter"
            }
            hint={
              entries.length === 0
                ? "I'll put new analyses here the moment the pipeline finishes one."
                : "Every case is filed under something else right now."
            }
            action={
              entries.length > 0 && (
                <Button size="sm" variant="secondary" onClick={() => setFilter("all")}>
                  Show all cases
                </Button>
              )
            }
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="label-eyebrow text-left">
                  <th className="px-5 py-3 font-normal">Patient</th>
                  <th className="px-5 py-3 font-normal">Signals</th>
                  <th className="hidden px-5 py-3 font-normal md:table-cell">
                    Last analysis
                  </th>
                  <th className="px-5 py-3 text-right font-normal">Open</th>
                </tr>
              </thead>
              <tbody>
                {visible.map((entry, index) => (
                  <QueueRow
                    key={entry.patient_id}
                    entry={entry}
                    index={index}
                  />
                ))}
              </tbody>
            </table>
          </div>
        )}

        <Pager
          page={safePage}
          pageCount={pageCount}
          total={filtered.length}
          pageSize={PAGE_SIZE}
          onPrev={() => setPage((p) => Math.max(1, p - 1))}
          onNext={() => setPage((p) => Math.min(pageCount, p + 1))}
        />
      </Card>
    </div>
  );
}

/* -- copy ------------------------------------------------------------- */

/**
 * The line under the greeting.
 *
 * It reports what is actually in the queue rather than describing the
 * feature. Every branch is derived from a real count — nothing here says
 * anything the data does not support.
 */
function summarise({
  isLoading,
  hasError,
  counts,
  topName,
}: {
  isLoading: boolean;
  hasError: boolean;
  counts: Record<QueueFilter, number>;
  topName: string | null;
}): string {
  if (isLoading) return "Just pulling your queue together…";
  if (hasError) return "I can't reach the queue at the moment — the retry below should do it.";
  if (counts.all === 0) {
    return "Nothing needs you right now. I'll put new analyses here as soon as they land.";
  }

  const cases = `${counts.all} ${counts.all === 1 ? "case" : "cases"}`;

  if (counts.worsening > 0) {
    return topName
      ? `${cases} waiting, and ${topName}'s is trending the wrong way — I've moved it to the top.`
      : `${cases} waiting. I've put the worsening ones at the top.`;
  }
  if (counts.sign_off > 0) {
    const n = counts.sign_off;
    return `${cases} waiting — ${n} ${n === 1 ? "is" : "are"} analysed and just needs your sign-off.`;
  }
  return `${cases} in your queue, none of them urgent. Take them in the order you like.`;
}

function filterEyebrow(filter: QueueFilter): string {
  switch (filter) {
    case "sign_off":
      return "Awaiting your sign-off";
    case "worsening":
      return "Worsening trend";
    case "early_watch":
      return "Early watch";
    default:
      return "Most urgent first";
  }
}

/** Today's date, rendered after mount so the server and client agree. */
function TodayLine() {
  const [today, setToday] = useState<string | null>(null);

  useEffect(() => {
    setToday(
      new Date().toLocaleDateString(undefined, {
        weekday: "long",
        day: "numeric",
        month: "long",
      })
    );
  }, []);

  return (
    <p className="label-eyebrow mb-1.5 h-4">
      {today ?? ""}
    </p>
  );
}

/* -- pieces ----------------------------------------------------------- */

function QueueRow({ entry, index }: { entry: TriageEntry; index: number }) {
  const name = triageName(entry) || "Unnamed patient";
  const urgency = triageUrgency(entry);

  return (
    <tr
      className="animate-fade-up border-t border-line transition-colors duration-150 hover:bg-raised/60"
      // Short stagger, capped: past a handful of rows the delay stops
      // reading as cascade and starts reading as lag.
      style={{ animationDelay: `${Math.min(index, 7) * 35}ms` }}
    >
      <td className="px-5 py-3.5">
        <div className="flex items-center gap-3">
          <span
            className={cn(
              "flex h-8 w-8 shrink-0 items-center justify-center rounded-full border font-mono text-[11px]",
              urgency === 2
                ? "border-amber/40 bg-amber-soft text-amber"
                : "border-line bg-raised text-text-muted"
            )}
          >
            {initials(name)}
          </span>
          <div className="min-w-0">
            <p className="truncate text-text">{name}</p>
            <p className="data-num truncate text-[11px] text-text-faint">
              {entry.patient_id.slice(0, 8)}
            </p>
          </div>
        </div>
      </td>

      <td className="px-5 py-3.5">
        <div className="flex flex-wrap gap-1.5">
          {entry.has_worsening_trend && (
            <Signal tone="amber" icon={TrendingDown} label="Worsening" />
          )}
          {entry.awaiting_sign_off && (
            <Signal tone="indigo" icon={Clock} label="Awaiting sign-off" />
          )}
          {entry.has_open_early_watch && (
            <Signal tone="teal" icon={Sparkles} label="Early watch" />
          )}
          {urgency === 0 && (
            <span className="text-[12px] text-text-faint">No open signals</span>
          )}
        </div>
      </td>

      <td className="hidden px-5 py-3.5 text-text-muted md:table-cell">
        {entry.latest_analysis_generated_at ? (
          <span className="data-num text-[12px]">
            {formatRelative(entry.latest_analysis_generated_at)}
          </span>
        ) : (
          <span className="text-[12px] text-text-faint">Not yet analysed</span>
        )}
      </td>

      <td className="px-5 py-3.5 text-right">
        <Link
          href={`/dashboard/patients/${entry.patient_id}`}
          className={cn(
            "inline-flex items-center gap-1.5 rounded border border-line px-2.5 py-1.5 text-[12px] text-text-muted",
            "transition-[background-color,border-color,color,transform] duration-150 ease-out",
            "hover:border-text-faint hover:bg-raised hover:text-text active:scale-[0.96]"
          )}
        >
          <Eye className="h-3.5 w-3.5" />
          Review
          <ArrowRight className="h-3.5 w-3.5" />
        </Link>
      </td>
    </tr>
  );
}

function Signal({
  tone,
  icon: Icon,
  label,
}: {
  tone: "amber" | "indigo" | "teal";
  icon: React.ComponentType<{ className?: string }>;
  label: string;
}) {
  const toneClass = {
    amber: "border-amber/30 bg-amber-soft text-amber",
    indigo: "border-indigo/30 bg-indigo-soft text-indigo",
    teal: "border-teal/30 bg-teal-soft text-teal",
  }[tone];

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-sm border px-2 py-0.5 text-[11px]",
        toneClass
      )}
    >
      <Icon className="h-3 w-3" />
      {label}
    </span>
  );
}
