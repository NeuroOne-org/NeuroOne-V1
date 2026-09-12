"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { extractApiError } from "@/lib/api";

export interface AsyncState<T> {
  data: T | null;
  isLoading: boolean;
  /** True only on the first load, so refetches don't blank the screen. */
  isInitialLoad: boolean;
  error: string | null;
  refetch: () => void;
}

/**
 * Runs `fetcher` whenever `deps` change and keeps the previous data visible
 * while the next request is in flight.
 *
 * Keeping stale data on screen during a refetch is the difference between a
 * table that updates and a table that flashes empty every keystroke; the
 * spinner lives in the toolbar instead of replacing the content.
 */
export function useAsync<T>(
  fetcher: () => Promise<T>,
  deps: unknown[],
  options: { enabled?: boolean } = {}
): AsyncState<T> {
  const enabled = options.enabled ?? true;

  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(enabled);
  const [isInitialLoad, setIsInitialLoad] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [nonce, setNonce] = useState(0);

  // A new request starts whenever these change. The loading flag and the
  // stale error are reset during render rather than in the effect, so the
  // render that starts a request already shows it as in flight.
  const requestKey = [enabled, nonce, ...deps];
  const [prevRequestKey, setPrevRequestKey] = useState(requestKey);
  if (!sameKey(prevRequestKey, requestKey)) {
    setPrevRequestKey(requestKey);
    setIsLoading(enabled);
    if (enabled) setError(null);
  }

  // Guards against a slow earlier request resolving after a newer one and
  // overwriting fresher data.
  const requestId = useRef(0);
  // Always calls the latest `fetcher` without making it a dependency, so an
  // inline arrow doesn't refetch on every render. Written in an effect, not
  // during render; declared first, so it runs before the fetch below.
  const fetcherRef = useRef(fetcher);
  useEffect(() => {
    fetcherRef.current = fetcher;
  });

  useEffect(() => {
    if (!enabled) return;

    const id = ++requestId.current;
    let cancelled = false;

    fetcherRef
      .current()
      .then((result) => {
        if (cancelled || id !== requestId.current) return;
        setData(result);
      })
      .catch((err) => {
        if (cancelled || id !== requestId.current) return;
        setError(extractApiError(err));
      })
      .finally(() => {
        if (cancelled || id !== requestId.current) return;
        setIsLoading(false);
        setIsInitialLoad(false);
      });

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [enabled, nonce, ...deps]);

  const refetch = useCallback(() => setNonce((n) => n + 1), []);

  return { data, isLoading, isInitialLoad, error, refetch };
}

/** Compares two dependency lists the way `useEffect` does. */
function sameKey(a: unknown[], b: unknown[]): boolean {
  return a.length === b.length && a.every((value, i) => Object.is(value, b[i]));
}

/**
 * Debounces a value. Search boxes hit `/patients/search` on every keystroke
 * otherwise, and the server is the wrong place to absorb typing speed.
 */
export function useDebounced<T>(value: T, delayMs = 300): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delayMs);
    return () => clearTimeout(timer);
  }, [value, delayMs]);
  return debounced;
}
