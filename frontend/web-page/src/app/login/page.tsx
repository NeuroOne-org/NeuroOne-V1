import { Suspense } from "react";
import { LoginForm } from "../../components/login-form";
import { AuthShell } from "../../components/auth-shell";

export default function LoginPage() {
  return (
    <AuthShell heading="Welcome back!" headingId="login-heading" subtitle="Access your patient queue and analyses.">
      <Suspense fallback={<p role="status">Loading sign-in form…</p>}>
        <LoginForm />
      </Suspense>
    </AuthShell>
  );
}
