import { SynapseArtwork } from "./synapse-artwork";

export function AuthShell({
  heading,
  headingId = "auth-heading",
  subtitle,
  children,
}: {
  heading: string;
  headingId?: string;
  subtitle: string;
  children: React.ReactNode;
}) {
  return (
    <main className="flex min-h-svh items-center justify-center bg-product-bg p-4 sm:p-8 lg:p-12">
      <div className="grid w-full max-w-[1120px] grid-cols-1 overflow-hidden rounded-md bg-product-surface shadow-[0_24px_64px_rgba(15,42,67,0.12)] md:grid-cols-2">
        <section aria-labelledby={headingId} className="flex flex-col justify-center px-6 py-10 sm:px-12 sm:py-14 lg:px-20 lg:py-16">
          <div className="mx-auto w-full max-w-[360px]">
            <div className="logo-wordmark mb-10 text-product-ink">NeuroOne</div>
            <h1 id={headingId} className="text-2xl font-semibold leading-8">{heading}</h1>
            <p className="mb-8 mt-2 text-[15px] leading-6 text-product-ink-soft">
              {subtitle}
            </p>
            {children}
          </div>
        </section>
        <div aria-hidden="true" className="relative hidden min-h-[680px] overflow-hidden bg-brand-navy md:block">
          <SynapseArtwork />
        </div>
      </div>
    </main>
  );
}
