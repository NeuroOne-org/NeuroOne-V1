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
import { useHydrated } from "@/hooks/use-hydrated";
import type { User } from "@/lib/types";
import type { LoginInput } from "@/lib/validation";

interface AuthContextValue {
  user: User | null;
  isLoading: boolean;
  /**
   * Verifies the password. If the backend requires a second factor
   * (AUTH_REQUIRE_OTP), it has already emailed a code and this resolves
   * with `{ otpRequired: true }` instead of signing in -- the caller should
   * send the user to /verify-otp. Otherwise it signs in directly.
   */
  login: (input: LoginInput) => Promise<{ otpRequired: boolean }>;
  /** Manually opt into a code instead of a password-only sign-in: emails a
   * code and remembers the credentials, regardless of AUTH_REQUIRE_OTP. */
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
  const [pendingOtpEmail, setPendingOtpEmail] = useState<string | null>(null);

  // The session is loading until hydration, and after it only while a token
  // found at startup is being checked. With no token there is nothing to
  // wait for, which is derived here rather than set from the mount effect.
  const hydrated = useHydrated();
  const [startedWithToken] = useState(
    () => typeof document !== "undefined" && Boolean(Cookies.get(TOKEN_COOKIE))
  );
  const [sessionChecked, setSessionChecked] = useState(false);
  const isLoading = !hydrated || (startedWithToken && !sessionChecked);

  // Kept in memory only. /auth/verify-otp checks password and code together,
  // so the OTP step needs the password a second time -- and a password must
  // never travel in a URL or sit in storage to get there. A refresh clears
  // this, which the verify screen reports as an expired attempt.
  const pendingLogin = useRef<{ email: string; password: string } | null>(null);

  // Assumes a token is stored; callers check for one first.
  const loadUser = useCallback(
    () =>
      authApi.me().then(
        (me) => setUser(me),
        () => {
          Cookies.remove(TOKEN_COOKIE);
          setUser(null);
        }
      ),
    []
  );

  const fetchCurrentUser = useCallback(async () => {
    if (!Cookies.get(TOKEN_COOKIE)) {
      setUser(null);
      return;
    }
    await loadUser();
  }, [loadUser]);

  useEffect(() => {
    if (!startedWithToken) return;
    loadUser().finally(() => setSessionChecked(true));
  }, [startedWithToken, loadUser]);

  const login = useCallback(
    async (input: LoginInput) => {
      try {
        const result = await authApi.login(input.email, input.password);
        if (result.otp_required) {
          // The backend already sent the code. Hold the password in memory
          // the same way beginOtpLogin does, and let the caller route to
          // /verify-otp -- no separate request-otp call needed here.
          pendingLogin.current = { email: input.email, password: input.password };
          setPendingOtpEmail(input.email);
          return { otpRequired: true };
        }
        persistToken(result.access_token as string);
        await fetchCurrentUser();
        return { otpRequired: false };
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