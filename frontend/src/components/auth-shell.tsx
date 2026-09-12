import { Activity } from "@/components/icons";
import { NeuralNetwork } from "@/components/neural-network";
import { FloatingParticles } from "@/components/floating-particles";

/**
 * Premium auth split.
 *
 * The signature panel takes two thirds and the form takes one. That ratio is
 * the whole point: the credential fields are a short, familiar task that wants
 * a narrow, quiet column, while the brand statement is what the page is
 * actually for on a first visit. Everything on the left is sized to be read
 * from across a desk; everything on the right is sized to be typed into.
 */
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
    <main className="dark grid min-h-screen grid-cols-1 bg-ink lg:grid-cols-[2fr_minmax(400px,1fr)]">
      {/* Signature panel — two thirds */}
      <section className="relative hidden overflow-hidden border-r border-line bg-panel lg:flex lg:flex-col lg:justify-between lg:p-14 xl:p-16">
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute -left-32 -top-32 h-[440px] w-[440px] animate-drift rounded-full bg-teal/10 blur-3xl" />
          <div
            className="absolute -bottom-36 right-0 h-[420px] w-[420px] animate-drift rounded-full bg-indigo/10 blur-3xl"
            style={{ animationDelay: "3s" }}
          />
          <div
            className="absolute left-1/2 top-1/2 h-[690px] w-[690px] -translate-x-1/2 -translate-y-1/2 opacity-70"
            style={{ perspective: "1350px" }}
          >
            <div className="h-full w-full animate-tilt-3d" style={{ transformStyle: "preserve-3d" }}>
              <NeuralNetwork className="h-full w-full" />
            </div>
          </div>
          <div className="absolute inset-x-0 top-1/2 h-px w-full animate-scan bg-gradient-to-r from-transparent via-teal/40 to-transparent" />
        </div>

        <div
          className="relative flex animate-fade-up items-center gap-3 font-display text-2xl font-semibold tracking-tight"
          style={{ animationDelay: "40ms" }}
        >
          <Activity className="h-7 w-7 text-teal" />
          NeuroOne
        </div>

        <div className="relative max-w-[580px] xl:max-w-[660px]">
          <p
            className="label-eyebrow mb-4 animate-fade-up text-[12px]"
            style={{ animationDelay: "100ms" }}
          >
            Clinical Intelligence Platform
          </p>
          <h1
            className="animate-fade-up font-display text-[42px] font-medium leading-[1.15] tracking-[-0.02em] text-text xl:text-[48px]"
            style={{ animationDelay: "150ms" }}
          >
            MRI-driven staging for Alzheimer&rsquo;s and Parkinson&rsquo;s,
            explained.
          </h1>
          <p
            className="mt-6 animate-fade-up text-[19px] leading-relaxed text-text-muted"
            style={{ animationDelay: "210ms" }}
          >
            Upload a scan, add patient context, and get a stage estimate with
            the regions that drove it &mdash; built to support a clinician&rsquo;s
            judgment, not replace it.
          </p>
        </div>

        <p
          className="relative animate-fade-up font-mono text-[13px] uppercase tracking-[0.14em] text-text-faint"
          style={{ animationDelay: "270ms" }}
        >
          Decision support &middot; Not a diagnostic device
        </p>
      </section>

      {/* Form panel — one third. Deliberately calmer than the left: the
          ambient depth is scaled to the narrower column so it reads as
          atmosphere behind the fields rather than as competing artwork. */}
      <section className="relative flex flex-col justify-center overflow-hidden bg-ink px-8 py-12 sm:px-12">
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute -right-32 -top-32 h-[380px] w-[380px] animate-drift rounded-full bg-indigo/10 blur-3xl" />
          <div
            className="absolute -bottom-40 -left-24 h-[340px] w-[340px] animate-drift rounded-full bg-teal/10 blur-3xl"
            style={{ animationDelay: "4s" }}
          />

          {/* True CSS 3D: perspective + a continuously tilting network,
              rather than a flat animated SVG. */}
          <div
            className="absolute -right-24 -top-28 h-[260px] w-[260px] opacity-[0.28]"
            style={{ perspective: "700px" }}
          >
            <div className="h-full w-full animate-tilt-3d" style={{ transformStyle: "preserve-3d" }}>
              <NeuralNetwork className="h-full w-full" />
            </div>
          </div>

          <FloatingParticles className="absolute inset-0" />

          <div
            className="absolute inset-x-0 top-1/3 h-px w-full animate-scan bg-gradient-to-r from-transparent via-indigo/30 to-transparent"
            style={{ animationDelay: "1.2s" }}
          />
        </div>

        <div className="relative mx-auto w-full max-w-[360px]">
          <div className="mb-8 flex items-center gap-2 font-display text-lg font-semibold lg:hidden">
            <Activity className="h-5 w-5 text-teal" />
            NeuroOne
          </div>
          <h2 className="animate-fade-up font-display text-xl font-medium text-text">
            {title}
          </h2>
          <p
            className="mt-1.5 animate-fade-up text-sm text-text-muted"
            style={{ animationDelay: "50ms" }}
          >
            {subtitle}
          </p>
          <div className="mt-8 animate-fade-up" style={{ animationDelay: "100ms" }}>
            {children}
          </div>
        </div>
      </section>
    </main>
  );
}
