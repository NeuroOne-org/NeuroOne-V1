"use client";

import React, { useRef, useState } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Html } from "@react-three/drei";
import { useScroll, useTransform, useSpring, motion, MotionValue } from "framer-motion";
import * as THREE from "three";
import Link from "next/link";
import { Activity, ArrowRight, ShieldCheck, Zap, Microscope, Brain } from "lucide-react";
import { cn } from "@/lib/utils";

// --- 3D NEURAL MESH BACKGROUND (WebGL R3F Geometry) ---

// Random node positions and the line segments connecting nearby nodes.
// Impure, so it runs once per mount from a useState initializer, never
// during a render.
function createNeuralMesh() {
  const nodes: THREE.Vector3[] = [];
  const count = 38;
  const radius = 4.2;

  for (let i = 0; i < count; i++) {
    const u = Math.random();
    const v = Math.random();
    const theta = u * 2.0 * Math.PI;
    const phi = Math.acos(2.0 * v - 1.0);
    const r = radius * (0.65 + Math.random() * 0.45);
    const x = r * Math.sin(phi) * Math.cos(theta);
    const y = r * Math.sin(phi) * Math.sin(theta);
    const z = r * Math.cos(phi);
    nodes.push(new THREE.Vector3(x, y, z));
  }

  const linePoints: THREE.Vector3[] = [];
  for (let i = 0; i < count; i++) {
    for (let j = i + 1; j < count; j++) {
      const dist = nodes[i].distanceTo(nodes[j]);
      if (dist < 2.6) {
        linePoints.push(nodes[i]);
        linePoints.push(nodes[j]);
      }
    }
  }

  const geom = new THREE.BufferGeometry().setFromPoints(linePoints);
  return { nodePositions: nodes, lineGeometry: geom };
}

function NeuralMesh3D({ smoothProgress }: { smoothProgress: MotionValue<number> }) {
  const meshGroupRef = useRef<THREE.Group>(null);
  const ringRef = useRef<THREE.Group>(null);

  const [{ nodePositions, lineGeometry }] = useState(createNeuralMesh);

  useFrame((state, delta) => {
    if (!meshGroupRef.current) return;
    const progress = smoothProgress.get();

    // Scroll drives camera angle, mesh rotation, and scale smoothly
    meshGroupRef.current.rotation.y = state.clock.elapsedTime * 0.15 + progress * Math.PI * 2.5;
    meshGroupRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.2) * 0.2 + (progress - 0.5) * 1.2;
    meshGroupRef.current.position.z = -1.5 + Math.sin(progress * Math.PI) * 1.8;

    if (ringRef.current) {
      ringRef.current.rotation.z = -state.clock.elapsedTime * 0.25;
      ringRef.current.rotation.x = progress * Math.PI;
    }
  });

  return (
    <group ref={meshGroupRef}>
      {/* Connecting Synaptic Lines */}
      <lineSegments geometry={lineGeometry}>
        <lineBasicMaterial color="#35D6C8" transparent opacity={0.35} />
      </lineSegments>

      {/* Instanced Glowing Nodes */}
      {nodePositions.map((pos, idx) => (
        <mesh key={idx} position={pos}>
          <sphereGeometry args={[0.075, 12, 12]} />
          <meshBasicMaterial
            color={idx % 3 === 0 ? "#FF6A3D" : idx % 2 === 0 ? "#6E7BFF" : "#35D6C8"}
          />
        </mesh>
      ))}

      {/* Outer 3D Orbital Rings */}
      <group ref={ringRef}>
        <mesh>
          <torusGeometry args={[5.2, 0.015, 16, 100]} />
          <meshBasicMaterial color="#6E7BFF" transparent opacity={0.25} />
        </mesh>
        <mesh rotation={[Math.PI / 3, 0, 0]}>
          <torusGeometry args={[4.6, 0.012, 16, 100]} />
          <meshBasicMaterial color="#35D6C8" transparent opacity={0.2} />
        </mesh>
      </group>
    </group>
  );
}

// --- SINGLE 3D FLOATING STORY CARD ---
interface StoryCardProps {
  index: number;
  totalCards: number;
  smoothProgress: MotionValue<number>;
  scrollRange: [number, number, number, number]; // [enterStart, restStart, restEnd, exitEnd]
  badge: string;
  badgeTone: "teal" | "indigo" | "amber";
  title: string;
  copy: string;
  isCta?: boolean;
}

function StoryCard3D({
  smoothProgress,
  scrollRange,
  badge,
  badgeTone,
  title,
  copy,
  isCta = false,
}: StoryCardProps) {
  const cardRef = useRef<THREE.Group>(null);
  const [enterStart, restStart, restEnd, exitEnd] = scrollRange;

  // Map scroll progress to 3D rotation, scale, position, and opacity
  // 1. Entrance Rotation & Scale (off-axis enter)
  const rotY = useTransform(
    smoothProgress,
    [enterStart, restStart, restEnd, exitEnd],
    [-115, 0, 0, 85]
  );

  const rotX = useTransform(
    smoothProgress,
    [enterStart, restStart, restEnd, exitEnd],
    [35, 0, 0, -65]
  );

  const rotZ = useTransform(
    smoothProgress,
    [enterStart, restStart, restEnd, exitEnd],
    [-20, 0, 0, 30]
  );

  const posZ = useTransform(
    smoothProgress,
    [enterStart, restStart, restEnd, exitEnd],
    [-12, 0, 0, -10]
  );

  const posX = useTransform(
    smoothProgress,
    [enterStart, restStart, restEnd, exitEnd],
    [-4, 0, 0, 4]
  );

  const opacity = useTransform(
    smoothProgress,
    [enterStart, restStart, restEnd, exitEnd],
    [0, 1, 1, 0]
  );

  const scale = useTransform(
    smoothProgress,
    [enterStart, restStart, restEnd, exitEnd],
    [0.45, 1.0, 1.0, 0.4]
  );

  useFrame((state) => {
    if (!cardRef.current) return;
    const progress = smoothProgress.get();

    // Check if card is currently active/resting in viewport
    const isActive = progress >= restStart && progress <= restEnd;

    // Gentle sinusoidal bobbing float when resting in view
    if (isActive) {
      const bob = Math.sin(state.clock.elapsedTime * 1.8) * 0.12;
      cardRef.current.position.y = bob;
    } else {
      cardRef.current.position.y = 0;
    }

    // Apply scroll-linked transforms to 3D Three.js group
    const rY = (rotY.get() * Math.PI) / 180;
    const rX = (rotX.get() * Math.PI) / 180;
    const rZ = (rotZ.get() * Math.PI) / 180;

    cardRef.current.rotation.set(rX, rY, rZ);
    cardRef.current.position.z = posZ.get();
    cardRef.current.position.x = posX.get();
    const s = scale.get();
    cardRef.current.scale.set(s, s, s);
  });

  return (
    <group ref={cardRef}>
      <Html
        transform
        occlude={false}
        distanceFactor={6}
        className="pointer-events-auto select-none"
      >
        <motion.div
          style={{ opacity }}
          className={cn(
            "w-[340px] sm:w-[420px] rounded-xl border border-line/90 bg-panel/90 p-6 md:p-8 shadow-2xl backdrop-blur-xl transition-shadow hover:shadow-teal/10",
            isCta && "text-center border-teal/40 bg-panel/95"
          )}
        >
          {/* Card Header Badge */}
          <div className={cn("mb-3 flex items-center gap-2", isCta && "justify-center")}>
            <span
              className={cn(
                "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-wider",
                badgeTone === "amber"
                  ? "border-amber/40 bg-amber/10 text-amber"
                  : badgeTone === "indigo"
                  ? "border-indigo/40 bg-indigo/10 text-indigo"
                  : "border-teal/40 bg-teal/10 text-teal"
              )}
            >
              <span
                className={cn(
                  "h-1.5 w-1.5 rounded-full animate-ping",
                  badgeTone === "amber" ? "bg-amber" : badgeTone === "indigo" ? "bg-indigo" : "bg-teal"
                )}
              />
              {badge}
            </span>
          </div>

          {/* Card Title & Punchy Copy */}
          <h3 className="font-display text-xl sm:text-2xl font-semibold text-text tracking-tight leading-snug">
            {title}
          </h3>
          <p className="mt-2.5 text-xs sm:text-sm leading-relaxed text-text-muted">
            {copy}
          </p>

          {/* If final CTA card, show small understated Start Button */}
          {isCta && (
            <div className="mt-6 flex items-center justify-center">
              <Link
                href="/login"
                className="group relative inline-flex items-center gap-2 rounded-md bg-teal px-5 py-2 font-display text-xs font-semibold text-ink transition-all hover:bg-teal/90 hover:scale-105 shadow-md shadow-teal/20"
              >
                <span>Start Platform</span>
                <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
              </Link>
            </div>
          )}
        </motion.div>
      </Html>
    </group>
  );
}

// --- MAIN R3F CANVAS SCENE CONTAINER ---
export function R3fCanvasScene() {
  const { scrollYProgress } = useScroll();

  // Physical spring inertia applied on top of raw scroll progress
  const smoothProgress = useSpring(scrollYProgress, {
    stiffness: 85,
    damping: 26,
    restDelta: 0.0005,
  });

  // Story Cards Configuration & Scroll Trigger Windows
  const CARDS: Omit<StoryCardProps, "smoothProgress">[] = [
    {
      index: 0,
      totalCards: 5,
      scrollRange: [0.0, 0.02, 0.18, 0.24],
      badge: "NeuroOne Platform",
      badgeTone: "teal",
      title: "MRI-Driven Staging for Alzheimer's & Parkinson's",
      copy: "Transforming raw structural neuroimaging into quantitative, explainable stage estimates designed to support clinical judgment.",
    },
    {
      index: 1,
      totalCards: 5,
      scrollRange: [0.22, 0.28, 0.42, 0.48],
      badge: "The Problem",
      badgeTone: "amber",
      title: "Manual MRI Staging Is Slow & Visually Subtle",
      copy: "Early hippocampal subfield atrophy and substantia nigra voxel signal loss are nearly impossible to quantify by eye across hundreds of 3D slices.",
    },
    {
      index: 2,
      totalCards: 5,
      scrollRange: [0.46, 0.52, 0.64, 0.70],
      badge: "AI Pipeline",
      badgeTone: "indigo",
      title: "Automated 3D Volumetric Segmentation",
      copy: "Direct DICOM and NIfTI ingestion segmenting 14 cortical and subcortical brain regions in seconds against normative benchmarks.",
    },
    {
      index: 3,
      totalCards: 5,
      scrollRange: [0.68, 0.74, 0.84, 0.88],
      badge: "Clinician Trust",
      badgeTone: "teal",
      title: "Explainable AI (XAI) Attributed Evidence",
      copy: "NeuroOne highlights exact anatomical region drivers with quantitative confidence ratings, placing final diagnostic sign-off firmly in doctor hands.",
    },
    {
      index: 4,
      totalCards: 5,
      scrollRange: [0.87, 0.92, 0.99, 1.0],
      badge: "Get Started",
      badgeTone: "teal",
      title: "Ready to Evaluate NeuroOne in Your Workflow?",
      copy: "Access decision-support clinical intelligence for neurologists and researchers.",
      isCta: true,
    },
  ];

  return (
    <div className="fixed inset-0 z-0 h-full w-full pointer-events-none">
      <Canvas
        camera={{ position: [0, 0, 9], fov: 50 }}
        gl={{ antialias: true, alpha: true, powerPreference: "high-performance" }}
        dpr={[1, 1.5]}
      >
        <ambientLight intensity={0.8} />
        <pointLight position={[10, 10, 10]} intensity={1.2} />

        {/* 3D WebGL Neural Background Mesh */}
        <NeuralMesh3D smoothProgress={smoothProgress} />

        {/* 3D Story Cards Floating in WebGL Scene */}
        {CARDS.map((cardProps) => (
          <StoryCard3D
            key={cardProps.index}
            {...cardProps}
            smoothProgress={smoothProgress}
          />
        ))}
      </Canvas>
    </div>
  );
}
