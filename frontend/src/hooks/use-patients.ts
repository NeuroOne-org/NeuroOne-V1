"use client";

import { useCallback, useEffect, useState } from "react";
import { api, extractApiError } from "@/lib/api";
import type { Patient } from "@/lib/types";

export function usePatients() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refetch = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const { data } = await api.get<Patient[]>("/patients");
      setPatients(data);
    } catch (err) {
      setError(extractApiError(err));
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    refetch();
  }, [refetch]);

  return { patients, isLoading, error, refetch };
}
