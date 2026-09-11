import { Suspense } from "react";
import { LoginForm } from "../../components/login-form";
import { LoginShell } from "../../components/login-shell";

export default function LoginPage() {
  return (
    <LoginShell>
      <Suspense fallback={<p role="status">Loading sign-in form…</p>}>
        <LoginForm />
      </Suspense>
    </LoginShell>
  );
}
