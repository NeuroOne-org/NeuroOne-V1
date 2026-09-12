"use client";

import { useSyncExternalStore } from "react";

const subscribeNever = () => () => {};

/**
 * False on the server and during hydration, true on every client render
 * after. For UI that depends on browser-only state (a stored theme, a
 * cookie) and would otherwise mismatch the server HTML.
 */
export function useHydrated(): boolean {
  return useSyncExternalStore(
    subscribeNever,
    () => true,
    () => false
  );
}
