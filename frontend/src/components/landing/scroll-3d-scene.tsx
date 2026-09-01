"use client";

import { useState } from "react";
import { useScroll, useTransform, useSpring, useMotionValueEvent, motion } from "framer-motion";
import { NeuralNetwork } from "@/components/neural-network";
import { FloatingParticles } from "@/components/floating-particles";

export function Scroll3dScene() {
  const [poseName, setPoseName] = useState<string>("POSE 01: HERO CORTICAL OVERVIEW");
  const [poseDegree, setPoseDegree] = useState<string>("0° CAM ROTATION");

  // Bind to window scroll progress (0 at top, 1 at bottom)
  const { scrollYProgress } = useScroll();

  // Add smooth physical inertia spring to scroll progress
  const smoothProgress = useSpring(scrollYProgress, {
    stiffness: 80,
    damping: 25,
    restDelta: 0.0005,
  });

  // Listen to scroll updates for HUD text display
  useMotionValueEvent(smoothProgress, "change", (latest) => {
    setPoseDegree(`${Math.round(latest * 360)}° CAM ROTATION`);
    if (latest < 0.2) {
      setPoseName("POSE 01: HERO CORTICAL OVERVIEW");
    } else if (latest < 0.45) {
      setPoseName("POSE 02: STRUCTURAL SLICE DEEP-SCAN");
    } else if (latest < 0.75) {
      setPoseName("POSE 03: VOLUMETRIC SYNAPSE EXECUTION");
    } else if (latest < 0.9) {
      setPoseName("POSE 04: GOVERNANCE & XAI AUDIT");
    } else {
      setPoseName("POSE 05: DECISION SUPPORT FOCAL CLIMAX");
    }
  });

  // 1. 3D Camera / Mesh Rotation & Transform mappings across scroll positions
  // Scroll 0.0 (Hero) -> 0.25 (Problem) -> 0.55 (Pipeline) -> 0.8 (Trust) -> 1.0 (CTA)
  const meshRotateX = useTransform(
    smoothProgress,
    [0, 0.25, 0.55, 0.8, 1.0],
    [16, -22, 38, 10, -14]
  );

  const meshRotateY = useTransform(
    smoothProgress,
    [0, 0.25, 0.55, 0.8, 1.0],
    [-18, 52, -65, 15, 190]
  );

  const meshRotateZ = useTransform(
    smoothProgress,
    [0, 0.25, 0.55, 0.8, 1.0],
    [0, 12, -15, 45, 0]
  );

  const meshX = useTransform(
    smoothProgress,
    [0, 0.25, 0.55, 0.8, 1.0],
    ["0%", "28%", "-30%", "0%", "0%"]
  );

  const meshY = useTransform(
    smoothProgress,
    [0, 0.25, 0.55, 0.8, 1.0],
    ["0%", "-10%", "5%", "-15%", "0%"]
  );

  const meshScale = useTransform(
    smoothProgress,
    [0, 0.25, 0.55, 0.8, 1.0],
    [1.1, 0.85, 1.25, 0.95, 1.4]
  );

  const meshOpacity = useTransform(
    smoothProgress,
    [0, 0.15, 0.85, 1.0],
    [0.75, 0.55, 0.65, 0.85]
  );

  // 2. Parallax Layers
  // Background particles move slower (depth parallax)
  const bgParticleY = useTransform(smoothProgress, [0, 1], ["0px", "-180px"]);
  const bgParticleRotate = useTransform(smoothProgress, [0, 1], [0, 90]);

  // Glow blob 3D shifts
  const glowTealX = useTransform(smoothProgress, [0, 0.5, 1], ["-10%", "30%", "-20%"]);
  const glowTealY = useTransform(smoothProgress, [0, 0.5, 1], ["-10%", "40%", "10%"]);
  const glowIndigoX = useTransform(smoothProgress, [0, 0.5, 1], ["20%", "-30%", "20%"]);
  const glowIndigoY = useTransform(smoothProgress, [0, 0.5, 1], ["10%", "-20%", "30%"]);

  return (
    <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden select-none">
      {/* Dynamic Scroll-Linked Ambient Glow Blobs */}
      <motion.div
        className="absolute h-[600px] w-[600px] rounded-full bg-teal/10 blur-[130px]"
        style={{ left: glowTealX, top: glowTealY }}
      />
      <motion.div
        className="absolute h-[650px] w-[650px] rounded-full bg-indigo/10 blur-[140px]"
        style={{ right: glowIndigoX, top: glowIndigoY }}
      />

      {/* Parallax Background Particle Field */}
      <motion.div
        className="absolute inset-0 opacity-50"
        style={{ y: bgParticleY, rotate: bgParticleRotate }}
      >
        <FloatingParticles className="h-full w-full" />
      </motion.div>

      {/* Global 3D Perspective Stage Container */}
      <div
        className="relative h-full w-full flex items-center justify-center"
        style={{ perspective: "1200px" }}
      >
        {/* Main Scroll-Transformed 3D Neural Cortex Mesh */}
        <motion.div
          className="relative h-[650px] w-[650px] max-w-[90vw] max-h-[90vh]"
          style={{
            x: meshX,
            y: meshY,
            rotateX: meshRotateX,
            rotateY: meshRotateY,
            rotateZ: meshRotateZ,
            scale: meshScale,
            opacity: meshOpacity,
            transformStyle: "preserve-3d",
          }}
        >
          {/* Outer 3D Orbital HUD Ring */}
          <div
            className="absolute inset-0 rounded-full border border-teal/20 animate-rotate-slow"
            style={{ transform: "translateZ(-60px)" }}
          />
          <div
            className="absolute inset-6 rounded-full border border-dashed border-indigo/20 animate-[rotate-slow_90s_linear_infinite_reverse]"
            style={{ transform: "translateZ(40px)" }}
          />

          {/* Central Neural Network Model */}
          <div className="h-full w-full drop-shadow-[0_0_35px_rgba(53,214,200,0.15)]">
            <NeuralNetwork className="h-full w-full" />
          </div>

          {/* Floating 3D Spatial HUD Indicator (linked to real camera pose) */}
          <div
            className="absolute -bottom-6 left-1/2 -translate-x-1/2 rounded-full border border-line bg-ink/90 px-3.5 py-1 font-mono text-[10px] text-teal backdrop-blur shadow-xl flex items-center gap-2"
            style={{ transform: "translateZ(80px)" }}
          >
            <span className="h-1.5 w-1.5 rounded-full bg-teal animate-ping" />
            <span>{poseName}</span>
            <span className="text-text-faint font-mono">|</span>
            <span className="text-indigo">{poseDegree}</span>
          </div>
        </motion.div>
      </div>

      {/* Subtle Scan Beam moving vertically */}
      <div className="absolute inset-x-0 top-0 h-px w-full animate-scan bg-gradient-to-r from-transparent via-teal/30 to-transparent" />
    </div>
  );
}
