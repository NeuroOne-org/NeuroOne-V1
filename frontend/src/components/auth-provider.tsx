"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import Cookies from "js-cookie";
import { TOKEN_COOKIE, extractApiError } from "@/lib/api";
import { auth as authApi } from "@/lib/endpoints";
import type { User } from "@/lib/types";
import type { LoginInput } from "@/lib/validation";

interface AuthContextValue {
  user: User | null;
  isLoading: boolean;
  /** Password only. Signs in and returns; no second factor. */
  login: (input: LoginInput) => Promise<void>;
  /** Opt-in second factor: emails a code and remembers the credentials. */
  beginOtpLogin: (input: LoginInput) => Promise<void>;
  completeOtpLogin: (otp: string) => Promise<void>;
  cancelOtpLogin: () => void;
  /** The address a code was sent to, or null if no OTP sign-in is in flight. */
  pendingOtpEmail: string | null;
  requestPasswordReset: (email: string) => Promise<void>;
  resetPassword: (
    email: string,
    otp: string,
    newPassword: string
  ) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

function persistToken(token: string) {
  Cookies.set(TOKEN_COOKIE, token, { expires: 1, sameSite: "strict" });
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [pendingOtpEmail, setPendingOtpEmail] = useState<string | null>(null);

  // Kept in memory only. /auth/verify-otp checks password and code together,
  // so the OTP step needs the password a second time -- and a password must
  // never travel in a URL or sit in storage to get there. A refresh clears
  // this, which the verify screen reports as an expired attempt.
  const pendingLogin = useRef<{ email: string; password: string } | null>(null);

  const fetchCurrentUser = useCallback(async () => {
    const token = Cookies.get(TOKEN_COOKIE);
    if (!token) {
      setUser(null);
      setIsLoading(false);
      return;
    }
    try {
      setUser(await authApi.me());
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

  const login = useCallback(
    async (input: LoginInput) => {
      try {
        const token = await authApi.login(input.email, input.password);
        persistToken(token.access_token);
        await fetchCurrentUser();
      } catch (error) {
        throw new Error(extractApiError(error));
      }
    },
    [fetchCurrentUser]
  );

  const beginOtpLogin = useCallback(async (input: LoginInput) => {
    try {
      await authApi.requestOtp(input.email);
      pendingLogin.current = { email: input.email, password: input.password };
      setPendingOtpEmail(input.email);
    } catch (error) {
      throw new Error(extractApiError(error));
    }
  }, []);

  const completeOtpLogin = useCallback(
    async (otp: string) => {
      const pending = pendingLogin.current;
      if (!pending) {
        throw new Error(
          "This sign-in attempt expired. Start again from the sign-in page."
        );
      }
      try {
        const token = await authApi.verifyOtp(pending.email, otp, pending.password);
        persistToken(token.access_token);
        pendingLogin.current = null;
        setPendingOtpEmail(null);
        await fetchCurrentUser();
      } catch (error) {
        throw new Error(extractApiError(error));
      }
    },
    [fetchCurrentUser]
  );

  const cancelOtpLogin = useCallback(() => {
    pendingLogin.current = null;
    setPendingOtpEmail(null);
  }, []);

  const requestPasswordReset = useCallback(async (email: string) => {
    try {
      await authApi.forgotPassword(email);
    } catch (error) {
      throw new Error(extractApiError(error));
    }
  }, []);

  const resetPassword = useCallback(
    async (email: string, otp: string, newPassword: string) => {
      try {
        // Returns a confirmation message, not a token: resetting a password
        // does not sign you in, so the caller sends the user to sign in with
        // the password they just chose.
        await authApi.resetPassword(email, otp, newPassword);
      } catch (error) {
        throw new Error(extractApiError(error));
      }
    },
    []
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
        beginOtpLogin,
        completeOtpLogin,
        cancelOtpLogin,
        pendingOtpEmail,
        requestPasswordReset,
        resetPassword,
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