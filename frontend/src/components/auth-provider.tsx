"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import Cookies from "js-cookie";
import { api, TOKEN_COOKIE, extractApiError } from "@/lib/api";
import type { User } from "@/lib/types";
import type { LoginInput } from "@/lib/validation";

interface AuthTokens {
  access_token: string;
  token_type: string;
}

interface AuthContextValue {
  user: User | null;
  isLoading: boolean;
  login: (input: LoginInput) => Promise<void>;
  verifyLoginOtp: (username: string, otp: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchCurrentUser = useCallback(async () => {
    const token = Cookies.get(TOKEN_COOKIE);
    if (!token) {
      setUser(null);
      setIsLoading(false);
      return;
    }
    try {
      const { data } = await api.get<User>("/auth/me");
      setUser(data);
    } catch {
      Cookies.remove(TOKEN_COOKIE);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCurrentUser();
  }, [fetchCurrentUser]);

  const login = useCallback(async (input: LoginInput) => {
    try {
      await api.post("/auth/login", {
        username: input.email,
        password: input.password,
      });
    } catch (error) {
      throw new Error(extractApiError(error));
    }
  }, []);

  const verifyLoginOtp = useCallback(
    async (username: string, otp: string) => {
      try {
        const { data } = await api.post<AuthTokens>("/auth/verify-otp", {
          username,
          otp,
        });
        Cookies.set(TOKEN_COOKIE, data.access_token, {
          expires: 1,
          sameSite: "strict",
        });
        await fetchCurrentUser();
      } catch (error) {
        throw new Error(extractApiError(error));
      }
    },
    [fetchCurrentUser]
  );

  const logout = useCallback(() => {
    Cookies.remove(TOKEN_COOKIE);
    setUser(null);
    window.location.href = "/login";
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        login,
        verifyLoginOtp,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}