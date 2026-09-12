"use client";

import dynamic from "next/dynamic";
import Link from "next/link";
import { Activity, ArrowRight, ChevronDown } from "lucide-react";
import { useScroll, useSpring, useMotionValueEvent } from "framer-motion";
import { useState } from "react";
import { FloatingParticles } from "@/components/floating-particles";

const R3fCanvasScene = dynamic(
  () =>
    import("@/components/landing/r3f-canvas-scene").then(
      (mod) => mod.R3fCanvasScene
    ),
  { ssr: false }
);

export default function LandingPage() {
  const [scrollPercent, setScrollPercent] = useState<number>(0);
  const { scrollYProgress } = useScroll();
  const smoothProgress = useSpring(scrollYProgress, { stiffness: 90, damping: 28 });

  useMotionValueEvent(smoothProgress, "change", (latest) => {
    setScrollPercent(Math.round(latest * 100));
  });

  return (
    <div className="dark relative min-h-[500vh] bg-ink text-text selection:bg-indigo/30 selection:text-text overflow-x-hidden">
      {/* Fixed 3D canvas — carries ALL the story copy as rotating/floating cards.
          Nothing else on this page duplicates that content. */}
      <R3fCanvasScene />

      {/* Ambient particles, purely decorative, spans the whole scroll */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden opacity-30 z-[1]">
        <FloatingParticles className="h-full w-full" />
      </div>

      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 border-b border-line/70 bg-ink/75 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <Link
            href="/"
            className="flex items-center gap-2.5 font-display text-lg font-semibold tracking-tight transition-opacity hover:opacity-90"
          >
            <Activity className="h-5 w-5 text-teal animate-pulse" />
            <span>NeuroOne</span>
          </Link>

          <div className="flex items-center gap-4">
            <span className="hidden sm:inline-flex items-center gap-1.5 rounded-full border border-teal/30 bg-teal/10 px-2.5 py-0.5 font-mono text-[11px] text-teal">
              <span className="h-1.5 w-1.5 rounded-full bg-teal animate-ping" />
              CLINICAL INTEL V1.4 &middot; {scrollPercent}%
            </span>

            <Link
              href="/login"
              className="inline-flex items-center gap-1.5 rounded-md border border-teal/40 bg-teal/10 px-3.5 py-1.5 font-mono text-xs font-medium text-teal transition-all hover:bg-teal hover:text-ink shadow-sm"
            >
              <span>Start</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>
        </div>
      </header>

      {/* Pure scroll-height spacer — no widgets, no duplicate text.
          Its only job is to give the 3D canvas enough scroll distance
          to play through all 5 cards' enter/rest/exit animations. */}
      <main className="relative z-10 pointer-events-none">
        <div className="h-[500vh]" aria-hidden="true" />

        {/* Scroll cue, fades out once the user starts scrolling */}
        <div
          className="fixed bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 font-mono text-[11px] text-text-faint animate-bounce z-10 transition-opacity duration-500"
          style={{ opacity: scrollPercent < 3 ? 1 : 0 }}
        >
          <span>SCROLL TO EXPLORE</span>
          <ChevronDown className="h-4 w-4 text-teal" />
        </div>
      </main>
    </div>
  );
}