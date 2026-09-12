"use client";

import { useMemo, useState } from "react";
import { patients as patientsApi, triage as triageApi } from "@/lib/endpoints";
import { useAsync, useDebounced } from "@/hooks/use-api";

/**
 * The whole ranked queue in one request.
 *
 * `/triage` pages but does not filter, so counting "awaiting sign-off" from a
 * single 8-row page would describe that page rather than the queue — and the
 * filter cards sit next to each other, inviting exactly that comparison.
 * Fetching the max page and filtering on the client makes every count true of
 * the same set. `QUEUE_FETCH_LIMIT` is the API ceiling; past it the UI says so
 * rather than quietly under-reporting.
 */
export const QUEUE_FETCH_LIMIT = 100;

export function useTriageQueue() {
  return useAsync(
    () => triageApi.list({ page: 1, page_size: QUEUE_FETCH_LIMIT }),
    []
  );
}

/**
 * The patient directory, with server-side search.
 *
 * `/patients/search` and `/patients` return the same shape, so the query
 * decides which endpoint answers rather than the caller branching.
 */
export function usePatientDirectory(page: number, query: string, pageSize = 8) {
  const debouncedQuery = useDebounced(query.trim(), 300);

  const state = useAsync(
    () =>
      debouncedQuery
        ? patientsApi.search(debouncedQuery, { page, page_size: pageSize })
        : patientsApi.list({ page, page_size: pageSize }),
    [page, pageSize, debouncedQuery]
  );

  // The visible query outrunning the fetched one is what "searching…" means.
  const isSearchPending = query.trim() !== debouncedQuery;

  return { ...state, isSearchPending };
}

export function usePatient(patientId: string) {
  return useAsync(() => patientsApi.get(patientId), [patientId], {
    enabled: Boolean(patientId),
  });
}

export function usePatientVisits(patientId: string, page = 1, pageSize = 20) {
  return useAsync(
    () => patientsApi.visits(patientId, { page, page_size: pageSize }),
    [patientId, page, pageSize],
    { enabled: Boolean(patientId) }
  );
}

/** Local page state paired with a total, so pagers stay in range when filters change. */
export function usePager(totalPages: number | undefined) {
  const [page, setPage] = useState(1);
  const pageCount = Math.max(1, totalPages ?? 1);
  const safePage = Math.min(page, pageCount);

  return useMemo(
    () => ({
      page: safePage,
      pageCount,
      setPage,
      reset: () => setPage(1),
      next: () => setPage((p) => Math.min(pageCount, p + 1)),
      prev: () => setPage((p) => Math.max(1, p - 1)),
    }),
    [safePage, pageCount]
  );
}
