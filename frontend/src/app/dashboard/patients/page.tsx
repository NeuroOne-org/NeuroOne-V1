"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  ArrowRight,
  Loader,
  Plus,
  Search,
  Users,
  X,
} from "@/components/icons";
import { Button } from "@/components/ui/button";
import { Card, CardHeader } from "@/components/ui/card";
import { EmptyState, ErrorState, Pager, TableSkeleton } from "@/components/ui/state";
import { usePager, usePatientDirectory } from "@/hooks/use-patients";
import { ageFromDob, cn, formatDate, fullName, initials } from "@/lib/utils";

const PAGE_SIZE = 8;

export default function PatientsPage() {
  const [query, setQuery] = useState("");
  const pager = usePager(undefined);
  const directory = usePatientDirectory(pager.page, query, PAGE_SIZE);

  // A new search starts at page one; staying on page 4 of the old result set
  // is the fastest way to make a search look broken.
  const { reset } = pager;
  useEffect(() => {
    reset();
  }, [query, reset]);

  const items = directory.data?.items ?? [];
  const pagination = directory.data?.pagination;
  const isBusy = directory.isSearchPending || directory.isLoading;

  return (
    <div className="mx-auto max-w-6xl">
      <header className="mb-7 flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="label-eyebrow mb-1.5">Directory</p>
          <h1 className="font-display text-2xl font-medium text-text">Patients</h1>
          <p className="mt-1 text-sm text-text-muted">
            Every patient on your list, searchable by name.
          </p>
        </div>
        <Link href="/dashboard/upload">
          <Button size="md">
            <Plus className="h-4 w-4" />
            New intake
          </Button>
        </Link>
      </header>

      <Card>
        <CardHeader
          eyebrow={
            pagination ? `${pagination.total_records} on file` : "Loading"
          }
          title="All patients"
          action={
            <div className="relative w-full max-w-[280px]">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-faint" />
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search by name…"
                aria-label="Search patients"
                className={cn(
                  "h-9 w-full rounded border border-line bg-raised pl-9 pr-9 text-[13px] text-text",
                  "placeholder:text-text-faint transition-colors duration-150",
                  "focus:border-indigo focus:outline-none focus:ring-1 focus:ring-indigo"
                )}
              />
              {/* One slot, two meanings: a spinner while the query is in
                  flight, a clear button once it has settled. */}
              <span className="absolute right-2.5 top-1/2 -translate-y-1/2">
                {isBusy && query ? (
                  <Loader className="h-4 w-4 animate-spin text-text-faint" />
                ) : query ? (
                  <button
                    onClick={() => setQuery("")}
                    aria-label="Clear search"
                    className="rounded p-0.5 text-text-faint transition-colors duration-150 hover:text-text"
                  >
                    <X className="h-4 w-4" />
                  </button>
                ) : null}
              </span>
            </div>
          }
        />

        {directory.isInitialLoad && directory.isLoading ? (
          <TableSkeleton rows={6} cols={4} />
        ) : directory.error ? (
          <ErrorState message={directory.error} onRetry={directory.refetch} />
        ) : items.length === 0 ? (
          <EmptyState
            icon={Users}
            title={query ? "No patients match that search" : "No patients yet"}
            hint={
              query
                ? "Try part of a first or last name."
                : "Add your first patient from the intake form."
            }
            action={
              !query && (
                <Link href="/dashboard/upload">
                  <Button size="sm" variant="secondary">
                    <Plus className="h-4 w-4" />
                    New intake
                  </Button>
                </Link>
              )
            }
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="label-eyebrow text-left">
                  <th className="px-5 py-3 font-normal">Patient</th>
                  <th className="hidden px-5 py-3 font-normal sm:table-cell">
                    Age
                  </th>
                  <th className="hidden px-5 py-3 font-normal md:table-cell">
                    Contact
                  </th>
                  <th className="hidden px-5 py-3 font-normal lg:table-cell">
                    Added
                  </th>
                  <th className="px-5 py-3 text-right font-normal">Open</th>
                </tr>
              </thead>
              <tbody>
                {items.map((patient, index) => {
                  const name = fullName(patient) || "Unnamed patient";
                  const age = ageFromDob(patient.dob);
                  return (
                    <tr
                      key={patient.id}
                      className="animate-fade-up border-t border-line transition-colors duration-150 hover:bg-raised/60"
                      style={{ animationDelay: `${Math.min(index, 7) * 35}ms` }}
                    >
                      <td className="px-5 py-3.5">
                        <div className="flex items-center gap-3">
                          <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border border-line bg-raised font-mono text-[11px] text-text-muted">
                            {initials(name)}
                          </span>
                          <div className="min-w-0">
                            <p className="truncate text-text">{name}</p>
                            <p className="truncate text-[11px] capitalize text-text-faint">
                              {patient.gender}
                              {patient.blood_group
                                ? ` · ${patient.blood_group}`
                                : ""}
                            </p>
                          </div>
                        </div>
                      </td>
                      <td className="hidden px-5 py-3.5 sm:table-cell">
                        <span className="data-num text-text-muted">
                          {age ?? "—"}
                        </span>
                      </td>
                      <td className="hidden max-w-[220px] truncate px-5 py-3.5 text-[13px] text-text-muted md:table-cell">
                        {patient.email ||
                          patient.phone?.[0]?.phone_number ||
                          "—"}
                      </td>
                      <td className="hidden px-5 py-3.5 lg:table-cell">
                        <span className="data-num text-[12px] text-text-faint">
                          {formatDate(patient.created_at)}
                        </span>
                      </td>
                      <td className="px-5 py-3.5 text-right">
                        <Link
                          href={`/dashboard/patients/${patient.id}`}
                          className={cn(
                            "inline-flex items-center gap-1.5 rounded border border-line px-2.5 py-1.5 text-[12px] text-text-muted",
                            "transition-[background-color,border-color,color,transform] duration-150 ease-out",
                            "hover:border-text-faint hover:bg-raised hover:text-text active:scale-[0.96]"
                          )}
                        >
                          Open
                          <ArrowRight className="h-3.5 w-3.5" />
                        </Link>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        <Pager
          page={pager.page}
          pageCount={Math.max(1, pagination?.total_pages ?? 1)}
          total={pagination?.total_records ?? 0}
          pageSize={PAGE_SIZE}
          onPrev={pager.prev}
          onNext={pager.next}
        />
      </Card>
    </div>
  );
}
