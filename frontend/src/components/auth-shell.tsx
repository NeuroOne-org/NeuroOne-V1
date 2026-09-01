import { Activity } from "lucide-react";
import { NeuralNetwork } from "@/components/neural-network";
import { FloatingParticles } from "@/components/floating-particles";

export function AuthShell({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle: string;
  children: React.ReactNode;
}) {
  return (
    <main className="grid min-h-screen grid-cols-1 md:grid-cols-[1fr_440px]">
      {/* Branding / signature panel */}
      <section className="relative hidden overflow-hidden border-r border-line bg-panel md:flex md:flex-col md:justify-between md:p-10 lg:p-12">
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute -left-20 -top-20 h-[300px] w-[300px] animate-drift rounded-full bg-teal/10 blur-3xl" />
          <div
            className="absolute -bottom-24 right-0 h-[280px] w-[280px] animate-drift rounded-full bg-indigo/10 blur-3xl"
            style={{ animationDelay: "3s" }}
          />
          <div
            className="absolute left-1/2 top-1/2 h-[460px] w-[460px] -translate-x-1/2 -translate-y-1/2 opacity-70"
            style={{ perspective: "900px" }}
          >
            <div className="h-full w-full animate-tilt-3d" style={{ transformStyle: "preserve-3d" }}>
              <NeuralNetwork className="h-full w-full" />
            </div>
          </div>
          <div className="absolute inset-x-0 top-1/2 h-px w-full animate-scan bg-gradient-to-r from-transparent via-teal/40 to-transparent" />
        </div>

        <div className="relative flex items-center gap-2 font-display text-lg font-semibold tracking-tight">
          <Activity className="h-5 w-5 text-teal" />
          NeuroOne
        </div>

        <div className="relative max-w-sm">
          <p className="label-eyebrow mb-3">Clinical Intelligence Platform</p>
          <h1 className="font-display text-3xl font-medium leading-snug text-text">
            MRI-driven staging for Alzheimer&rsquo;s and Parkinson&rsquo;s,
            explained.
          </h1>
          <p className="mt-4 text-sm leading-relaxed text-text-muted">
            Upload a scan, add patient context, and get a stage estimate with
            the regions that drove it &mdash; built to support a clinician&rsquo;s
            judgment, not replace it.
          </p>
        </div>

        <p className="relative font-mono text-[11px] uppercase tracking-[0.14em] text-text-faint">
          Decision support &middot; Not a diagnostic device
        </p>
      </section>

      {/* Form panel */}
      <section className="relative flex flex-col justify-center overflow-hidden bg-ink px-8 py-12 sm:px-14">
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute -right-32 -top-32 h-[420px] w-[420px] animate-drift rounded-full bg-indigo/10 blur-3xl" />
          <div
            className="absolute -bottom-40 -left-24 h-[380px] w-[380px] animate-drift rounded-full bg-teal/10 blur-3xl"
            style={{ animationDelay: "4s" }}
          />

          {/* True CSS 3D: perspective + a continuously tilting network,
              rather than a flat animated SVG. */}
          <div
            className="absolute -right-20 -top-24 h-[300px] w-[300px] opacity-[0.35]"
            style={{ perspective: "700px" }}
          >
            <div className="h-full w-full animate-tilt-3d" style={{ transformStyle: "preserve-3d" }}>
              <NeuralNetwork className="h-full w-full" />
            </div>
          </div>
          <div
            className="absolute -bottom-24 -left-16 h-[280px] w-[280px] opacity-[0.28]"
            style={{ perspective: "700px" }}
          >
            <div
              className="h-full w-full rotate-180 animate-tilt-3d"
              style={{ transformStyle: "preserve-3d", animationDelay: "-7s" }}
            >
              <NeuralNetwork className="h-full w-full" />
            </div>
          </div>

          <FloatingParticles className="absolute inset-0" />

          <div
            className="absolute inset-x-0 top-1/3 h-px w-full animate-scan bg-gradient-to-r from-transparent via-indigo/30 to-transparent"
            style={{ animationDelay: "1.2s" }}
          />
        </div>

        <div className="relative mx-auto w-full max-w-[340px]">
          <div className="mb-8 flex items-center gap-2 font-display text-lg font-semibold md:hidden">
            <Activity className="h-5 w-5 text-teal" />
            NeuroOne
          </div>
          <h2 className="font-display text-xl font-medium text-text">
            {title}
          </h2>
          <p className="mt-1.5 text-sm text-text-muted">{subtitle}</p>
          <div className="mt-8">{children}</div>
        </div>
      </section>
    </main>
  );
}
