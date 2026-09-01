"use client";

import { useEffect, useRef, useState, useMemo } from "react";
import * as THREE from "three";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import {
  Users,
  Activity,
  AlertTriangle,
  TrendingUp,
  Search,
  ChevronLeft,
  ChevronRight,
  ChevronUp,
  ChevronDown,
  Plus,
  X,
  CalendarClock,
  FileDown,
  Flag,
  ArrowUpDown,
} from "lucide-react";
import { useAuth } from "@/components/auth-provider";

const ACCENTS = {
  violet: "#8b5cf6",
  cyan: "#22d3ee",
  coral: "#fb7185",
  amber: "#fbbf24",
  emerald: "#34d399",
};

const STATUS_STYLE: Record<
  string,
  { color: string; bg: string; ring: string }
> = {
  Stable: {
    color: ACCENTS.emerald,
    bg: "rgba(52,211,153,0.12)",
    ring: "rgba(52,211,153,0.35)",
  },
  Monitoring: {
    color: ACCENTS.amber,
    bg: "rgba(251,191,36,0.12)",
    ring: "rgba(251,191,36,0.35)",
  },
  Critical: {
    color: ACCENTS.coral,
    bg: "rgba(251,113,133,0.12)",
    ring: "rgba(251,113,133,0.35)",
  },
  Reviewing: {
    color: ACCENTS.violet,
    bg: "rgba(139,92,246,0.12)",
    ring: "rgba(139,92,246,0.35)",
  },
};

const AVATAR_PALETTES: [string, string][] = [
  ["#8b5cf6", "#6366f1"],
  ["#22d3ee", "#0ea5e9"],
  ["#fb7185", "#f472b6"],
  ["#fbbf24", "#f59e0b"],
  ["#34d399", "#10b981"],
];

interface PatientRow {
  id: string;
  name: string;
  age: number;
  region: string;
  confidence: number;
  status: string;
  lastScan: string;
  history: number[];
}

const PATIENTS: PatientRow[] = [
  { id: "NP-1042", name: "Elena Vasquez", age: 54, region: "Temporal Lobe", confidence: 96, status: "Stable", lastScan: "Aug 1, 2026", history: [88, 90, 93, 96] },
  { id: "NP-1043", name: "Marcus Chen", age: 61, region: "Hippocampus", confidence: 78, status: "Monitoring", lastScan: "Aug 1, 2026", history: [70, 74, 75, 78] },
  { id: "NP-1044", name: "Amara Okafor", age: 47, region: "Frontal Cortex", confidence: 91, status: "Stable", lastScan: "Jul 31, 2026", history: [85, 87, 89, 91] },
  { id: "NP-1045", name: "David Park", age: 69, region: "Brainstem", confidence: 58, status: "Critical", lastScan: "Jul 31, 2026", history: [71, 66, 61, 58] },
  { id: "NP-1046", name: "Sofia Moretti", age: 39, region: "Cerebellum", confidence: 88, status: "Stable", lastScan: "Jul 30, 2026", history: [80, 83, 86, 88] },
  { id: "NP-1047", name: "Ravi Patel", age: 57, region: "Parietal Lobe", confidence: 82, status: "Reviewing", lastScan: "Jul 30, 2026", history: [79, 80, 81, 82] },
  { id: "NP-1048", name: "Grace Lindqvist", age: 44, region: "Occipital Lobe", confidence: 94, status: "Stable", lastScan: "Jul 29, 2026", history: [90, 91, 93, 94] },
  { id: "NP-1049", name: "Tomas Novak", age: 72, region: "Temporal Lobe", confidence: 63, status: "Monitoring", lastScan: "Jul 29, 2026", history: [72, 69, 65, 63] },
  { id: "NP-1050", name: "Yuki Tanaka", age: 50, region: "Hippocampus", confidence: 97, status: "Stable", lastScan: "Jul 28, 2026", history: [92, 94, 96, 97] },
  { id: "NP-1051", name: "Layla Haddad", age: 63, region: "Frontal Cortex", confidence: 71, status: "Reviewing", lastScan: "Jul 28, 2026", history: [76, 74, 73, 71] },
];

const SCAN_VOLUME = [
  { day: "Jul 20", scans: 14 }, { day: "Jul 21", scans: 18 }, { day: "Jul 22", scans: 12 },
  { day: "Jul 23", scans: 21 }, { day: "Jul 24", scans: 19 }, { day: "Jul 25", scans: 24 },
  { day: "Jul 26", scans: 17 }, { day: "Jul 27", scans: 22 }, { day: "Jul 28", scans: 26 },
  { day: "Jul 29", scans: 23 }, { day: "Jul 30", scans: 28 }, { day: "Jul 31", scans: 25 },
  { day: "Aug 1", scans: 30 },
];

const PAGE_SIZE = 6;

function hexToRgb01(hex: string): [number, number, number] {
  const v = parseInt(hex.slice(1), 16);
  return [((v >> 16) & 255) / 255, ((v >> 8) & 255) / 255, (v & 255) / 255];
}

function useCountUp(target: number, duration = 900) {
  const [value, setValue] = useState(0);
  useEffect(() => {
    let raf: number;
    const start = performance.now();
    function tick(now: number) {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      setValue(target * eased);
      if (t < 1) raf = requestAnimationFrame(tick);
    }
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target, duration]);
  return value;
}

function Sparkline({
  data,
  color,
  width = 90,
  height = 28,
}: {
  data: number[];
  color: string;
  width?: number;
  height?: number;
}) {
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;
  const points = data
    .map((d, i) => {
      const x = (i / (data.length - 1)) * width;
      const y = height - ((d - min) / range) * height;
      return `${x},${y}`;
    })
    .join(" ");
  const areaPoints = `0,${height} ${points} ${width},${height}`;
  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} className="overflow-visible">
      <polyline points={areaPoints} fill={color} opacity="0.12" />
      <polyline points={points} fill="none" stroke={color} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function RadialGauge({ value, color, size = 108 }: { value: number; color: string; size?: number }) {
  const animated = useCountUp(value, 1000);
  const stroke = 8;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const offset = c - (animated / 100) * c;
  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} stroke="rgba(255,255,255,0.08)" strokeWidth={stroke} fill="none" />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          stroke={color}
          strokeWidth={stroke}
          fill="none"
          strokeDasharray={c}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{ filter: `drop-shadow(0 0 6px ${color}aa)` }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span style={{ fontFamily: "'JetBrains Mono', monospace", color: "#eef1fb" }} className="text-xl font-semibold tabular-nums">
          {Math.round(animated)}%
        </span>
        <span className="text-[10px] uppercase tracking-wider" style={{ color: "#6b7291" }}>
          confidence
        </span>
      </div>
    </div>
  );
}

function Avatar({ name, index, size = 38 }: { name: string; index: number; size?: number }) {
  const initials = name.split(" ").map((n) => n[0]).slice(0, 2).join("");
  const [c1, c2] = AVATAR_PALETTES[index % AVATAR_PALETTES.length];
  return (
    <div
      className="flex items-center justify-center rounded-full shrink-0 font-semibold"
      style={{
        width: size,
        height: size,
        background: `linear-gradient(135deg, ${c1}, ${c2})`,
        color: "#070a16",
        fontSize: size * 0.36,
      }}
    >
      {initials}
    </div>
  );
}

function NeuralBackground() {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return;

    const reduceMotion =
      typeof window !== "undefined" &&
      window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    let width = mount.clientWidth;
    let height = mount.clientHeight;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 100);
    camera.position.z = 17;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    mount.appendChild(renderer.domElement);

    const group = new THREE.Group();
    scene.add(group);

    const palette = [ACCENTS.violet, ACCENTS.cyan, ACCENTS.coral, ACCENTS.amber, ACCENTS.emerald];

    const NODE_COUNT = 68;
    const nodePositions: number[] = [];
    const nodeColors: number[] = [];
    for (let i = 0; i < NODE_COUNT; i++) {
      const r = 9 + Math.random() * 3.5;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 2 - 1);
      const x = r * Math.sin(phi) * Math.cos(theta);
      const y = r * Math.sin(phi) * Math.sin(theta) * 0.55;
      const z = r * Math.cos(phi);
      nodePositions.push(x, y, z);
      const c = hexToRgb01(palette[i % palette.length]);
      nodeColors.push(...c);
    }

    const nodeGeo = new THREE.BufferGeometry();
    nodeGeo.setAttribute("position", new THREE.Float32BufferAttribute(nodePositions, 3));
    nodeGeo.setAttribute("color", new THREE.Float32BufferAttribute(nodeColors, 3));
    const nodeMat = new THREE.PointsMaterial({
      size: 0.22,
      vertexColors: true,
      transparent: true,
      opacity: 0.8,
      sizeAttenuation: true,
    });
    const points = new THREE.Points(nodeGeo, nodeMat);
    group.add(points);

    const linePositions: number[] = [];
    const lineColors: number[] = [];
    const edges: [number, number][] = [];
    const threshold = 4.4;
    for (let i = 0; i < NODE_COUNT; i++) {
      for (let j = i + 1; j < NODE_COUNT; j++) {
        const dx = nodePositions[i * 3] - nodePositions[j * 3];
        const dy = nodePositions[i * 3 + 1] - nodePositions[j * 3 + 1];
        const dz = nodePositions[i * 3 + 2] - nodePositions[j * 3 + 2];
        const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
        if (dist < threshold && Math.random() > 0.58) {
          linePositions.push(
            nodePositions[i * 3], nodePositions[i * 3 + 1], nodePositions[i * 3 + 2],
            nodePositions[j * 3], nodePositions[j * 3 + 1], nodePositions[j * 3 + 2]
          );
          const c1 = [nodeColors[i * 3], nodeColors[i * 3 + 1], nodeColors[i * 3 + 2]];
          lineColors.push(...c1, ...c1);
          edges.push([i, j]);
        }
      }
    }

    const lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute("position", new THREE.Float32BufferAttribute(linePositions, 3));
    lineGeo.setAttribute("color", new THREE.Float32BufferAttribute(lineColors, 3));
    const lineMat = new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.14 });
    const lines = new THREE.LineSegments(lineGeo, lineMat);
    group.add(lines);

    const pulses: { mesh: THREE.Mesh; edge: [number, number]; t: number; speed: number }[] = [];
    const pulseGeo = new THREE.SphereGeometry(0.09, 8, 8);
    if (edges.length > 0) {
      const PULSE_COUNT = 18;
      for (let i = 0; i < PULSE_COUNT; i++) {
        const edge = edges[Math.floor(Math.random() * edges.length)];
        const color = new THREE.Color(palette[i % palette.length]);
        const mat = new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.95 });
        const mesh = new THREE.Mesh(pulseGeo, mat);
        group.add(mesh);
        pulses.push({ mesh, edge, t: Math.random(), speed: 0.12 + Math.random() * 0.22 });
      }
    }

    let frameId: number;
    const clock = new THREE.Clock();

    function renderFrame(delta: number) {
      group.rotation.y += delta * 0.045;
      group.rotation.x = Math.sin(clock.elapsedTime * 0.08) * 0.07;

      pulses.forEach((p) => {
        p.t += delta * p.speed;
        if (p.t > 1) {
          p.t = 0;
          p.edge = edges[Math.floor(Math.random() * edges.length)];
        }
        const [i, j] = p.edge;
        const ax = nodePositions[i * 3], ay = nodePositions[i * 3 + 1], az = nodePositions[i * 3 + 2];
        const bx = nodePositions[j * 3], by = nodePositions[j * 3 + 1], bz = nodePositions[j * 3 + 2];
        p.mesh.position.set(ax + (bx - ax) * p.t, ay + (by - ay) * p.t, az + (bz - az) * p.t);
      });

      renderer.render(scene, camera);
    }

    if (reduceMotion) {
      renderFrame(0.016);
    } else {
      const animate = () => {
        const delta = clock.getDelta();
        renderFrame(delta);
        frameId = requestAnimationFrame(animate);
      };
      animate();
    }

    function handleResize() {
      if (!mount) return;
      width = mount.clientWidth;
      height = mount.clientHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    }
    window.addEventListener("resize", handleResize);

    return () => {
      if (frameId) cancelAnimationFrame(frameId);
      window.removeEventListener("resize", handleResize);
      if (mount.contains(renderer.domElement)) mount.removeChild(renderer.domElement);
      nodeGeo.dispose();
      nodeMat.dispose();
      lineGeo.dispose();
      lineMat.dispose();
      pulseGeo.dispose();
      pulses.forEach((p) => (p.mesh.material as THREE.Material).dispose());
      renderer.dispose();
    };
  }, []);

  return <div ref={mountRef} className="absolute inset-0" />;
}

function StatCard({
  icon: Icon,
  label,
  value,
  suffix = "",
  sublabel,
  accent,
  sparkData,
}: {
  icon: any;
  label: string;
  value: number;
  suffix?: string;
  sublabel: string;
  accent: string;
  sparkData: number[];
}) {
  const animated = useCountUp(value);
  return (
    <div
      className="relative rounded-2xl p-5 overflow-hidden backdrop-blur-xl border transition-transform hover:-translate-y-1"
      style={{
        background: "rgba(16,21,42,0.55)",
        borderColor: "rgba(255,255,255,0.08)",
        boxShadow: `0 0 0 1px rgba(255,255,255,0.02), 0 8px 30px -12px ${accent}55`,
      }}
    >
      <div className="absolute -top-10 -right-10 w-32 h-32 rounded-full blur-3xl opacity-40" style={{ background: accent }} />
      <div className="relative flex items-start justify-between">
        <div>
          <p className="text-[11px] uppercase tracking-[0.14em] font-medium" style={{ color: "#8a91ad" }}>
            {label}
          </p>
          <p className="mt-2 text-3xl font-semibold tabular-nums" style={{ fontFamily: "'JetBrains Mono', monospace", color: "#eef1fb" }}>
            {Math.round(animated)}
            {suffix}
          </p>
          <p className="mt-1 text-xs" style={{ color: "#6b7291" }}>
            {sublabel}
          </p>
        </div>
        <div className="flex items-center justify-center w-10 h-10 rounded-xl shrink-0" style={{ background: `${accent}22`, border: `1px solid ${accent}45` }}>
          <Icon size={18} style={{ color: accent }} strokeWidth={2} />
        </div>
      </div>
      <div className="relative mt-3">
        <Sparkline data={sparkData} color={accent} />
      </div>
    </div>
  );
}

function FilterChip({
  label,
  count,
  active,
  accent,
  onClick,
}: {
  label: string;
  count: number;
  active: boolean;
  accent: string;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all"
      style={{
        background: active ? `${accent}22` : "rgba(255,255,255,0.03)",
        border: `1px solid ${active ? accent + "66" : "rgba(255,255,255,0.08)"}`,
        color: active ? accent : "#8a91ad",
      }}
    >
      {label}
      <span
        className="px-1.5 py-0.5 rounded-full text-[10px]"
        style={{ background: active ? `${accent}33` : "rgba(255,255,255,0.06)", color: active ? accent : "#6b7291" }}
      >
        {count}
      </span>
    </button>
  );
}

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload || !payload.length) return null;
  return (
    <div
      className="rounded-lg px-3 py-2 text-xs backdrop-blur-xl border"
      style={{ background: "rgba(10,13,26,0.9)", borderColor: "rgba(255,255,255,0.1)", fontFamily: "'JetBrains Mono', monospace" }}
    >
      <div style={{ color: "#8a91ad" }}>{label}</div>
      <div style={{ color: ACCENTS.cyan }}>{payload[0].value} scans</div>
    </div>
  );
}

function DetailDrawer({
  patient,
  index,
  onClose,
}: {
  patient: PatientRow;
  index: number;
  onClose: () => void;
}) {
  const s = STATUS_STYLE[patient.status];
  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div
        className="relative w-full max-w-sm h-full overflow-y-auto p-6 border-l"
        style={{ background: "#0b0f21", borderColor: "rgba(255,255,255,0.08)" }}
      >
        <button onClick={onClose} className="absolute top-5 right-5 p-1.5 rounded-lg hover:bg-white/5" style={{ color: "#8a91ad" }} aria-label="Close">
          <X size={18} />
        </button>

        <div className="flex items-center gap-3 mb-6">
          <Avatar name={patient.name} index={index} size={48} />
          <div>
            <h3 style={{ color: "#eef1fb" }} className="text-base font-semibold">
              {patient.name}
            </h3>
            <p style={{ color: "#6b7291", fontFamily: "'JetBrains Mono', monospace" }} className="text-xs">
              {patient.id} · Age {patient.age}
            </p>
          </div>
        </div>

        <div className="flex justify-center mb-6">
          <RadialGauge value={patient.confidence} color={s.color} />
        </div>

        <div className="flex items-center justify-between mb-6">
          <span
            className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
            style={{ color: s.color, background: s.bg, border: `1px solid ${s.ring}` }}
          >
            {patient.status}
          </span>
          <span className="text-xs" style={{ color: "#6b7291" }}>
            {patient.region}
          </span>
        </div>

        <div className="mb-6">
          <p className="text-[11px] uppercase tracking-wider mb-2" style={{ color: "#6b7291" }}>
            Confidence trend
          </p>
          <div className="rounded-xl p-3 border" style={{ background: "rgba(255,255,255,0.02)", borderColor: "rgba(255,255,255,0.06)" }}>
            <Sparkline data={patient.history} color={s.color} width={280} height={50} />
            <div className="flex justify-between mt-1 text-[10px]" style={{ color: "#6b7291", fontFamily: "'JetBrains Mono', monospace" }}>
              <span>4 scans ago</span>
              <span>latest</span>
            </div>
          </div>
        </div>

        <div className="space-y-2">
          <button
            className="w-full flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-transform hover:-translate-y-0.5"
            style={{ background: "linear-gradient(135deg, #8b5cf6, #6366f1)", color: "#f5f3ff" }}
          >
            <CalendarClock size={16} />
            Schedule follow-up
          </button>
          <button
            className="w-full flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium border"
            style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)", color: "#b7bdd6" }}
          >
            <FileDown size={16} />
            Download report
          </button>
          <button
            className="w-full flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium border"
            style={{ background: "rgba(251,113,133,0.08)", borderColor: "rgba(251,113,133,0.25)", color: ACCENTS.coral }}
          >
            <Flag size={16} />
            Flag as critical
          </button>
        </div>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const { user } = useAuth();
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(0);
  const [statusFilter, setStatusFilter] = useState("All");
  const [sortKey, setSortKey] = useState<keyof PatientRow>("lastScan");
  const [sortDir, setSortDir] = useState<"asc" | "desc">("desc");
  const [selectedPatient, setSelectedPatient] = useState<PatientRow | null>(null);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    let list = PATIENTS;
    if (statusFilter !== "All") list = list.filter((p) => p.status === statusFilter);
    if (q) {
      list = list.filter(
        (p) => p.name.toLowerCase().includes(q) || p.id.toLowerCase().includes(q) || p.region.toLowerCase().includes(q)
      );
    }
    const sorted = [...list].sort((a, b) => {
      const av = a[sortKey];
      const bv = b[sortKey];
      if (typeof av === "string" && typeof bv === "string") {
        return sortDir === "asc" ? av.localeCompare(bv) : bv.localeCompare(av);
      }
      if (typeof av === "number" && typeof bv === "number") {
        return sortDir === "asc" ? av - bv : bv - av;
      }
      return 0;
    });
    return sorted;
  }, [query, statusFilter, sortKey, sortDir]);

  const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const pageSafe = Math.min(page, pageCount - 1);
  const pageItems = filtered.slice(pageSafe * PAGE_SIZE, pageSafe * PAGE_SIZE + PAGE_SIZE);

  const stats = useMemo(() => {
    const total = PATIENTS.length;
    const active = PATIENTS.filter((p) => p.status === "Monitoring" || p.status === "Reviewing").length;
    const critical = PATIENTS.filter((p) => p.status === "Critical").length;
    const avgConf = Math.round(PATIENTS.reduce((s, p) => s + p.confidence, 0) / total);
    return { total, active, critical, avgConf };
  }, []);

  const statusCounts = useMemo(() => {
    const counts: Record<string, number> = { All: PATIENTS.length, Stable: 0, Monitoring: 0, Critical: 0, Reviewing: 0 };
    PATIENTS.forEach((p) => (counts[p.status] += 1));
    return counts;
  }, []);

  function toggleSort(key: keyof PatientRow) {
    if (sortKey === key) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir("asc");
    }
    setPage(0);
  }

  function SortHeader({ label, sortField, className = "" }: { label: string; sortField: keyof PatientRow; className?: string }) {
    const activeSort = sortKey === sortField;
    return (
      <th className={`px-5 py-3 font-medium ${className}`}>
        <button onClick={() => toggleSort(sortField)} className="flex items-center gap-1 hover:text-[#b7bdd6] transition-colors">
          {label}
          {activeSort ? sortDir === "asc" ? <ChevronUp size={12} /> : <ChevronDown size={12} /> : <ArrowUpDown size={11} className="opacity-40" />}
        </button>
      </th>
    );
  }

  return (
    <div className="relative -mx-8 -my-8 min-h-[calc(100vh-0px)] overflow-hidden" style={{ background: "#070a16" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');
      `}</style>

      <NeuralBackground />
      <div
        className="absolute inset-0 pointer-events-none"
        style={{ background: "radial-gradient(ellipse at 50% -10%, rgba(7,10,22,0.2) 0%, #070a16 78%)" }}
      />

      <div className="relative z-10 max-w-6xl mx-auto px-5 sm:px-8 py-8">
        <div className="flex items-center justify-between mb-8 gap-4">
          <div>
            <h1 style={{ fontFamily: "'Space Grotesk', sans-serif", fontWeight: 600, color: "#eef1fb" }} className="text-xl">
              Welcome back{user ? `, ${user.first_name}` : ""}
            </h1>
            <p className="text-sm mt-0.5" style={{ color: "#6b7291" }}>
              Here's what's happening with your patients today.
            </p>
          </div>
          <button
            className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-transform hover:-translate-y-0.5"
            style={{ background: "linear-gradient(135deg, #8b5cf6, #6366f1)", color: "#f5f3ff", boxShadow: "0 8px 24px -8px rgba(139,92,246,0.6)" }}
          >
            <Plus size={16} />
            <span className="hidden sm:inline">New patient</span>
          </button>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <StatCard icon={Users} label="Total patients" value={stats.total} sublabel="Across all wards" accent={ACCENTS.violet} sparkData={[6, 7, 8, 9, 9, 10]} />
          <StatCard icon={Activity} label="Active scans" value={stats.active} sublabel="Monitoring + reviewing" accent={ACCENTS.cyan} sparkData={[3, 4, 3, 5, 4, 4]} />
          <StatCard icon={AlertTriangle} label="Critical cases" value={stats.critical} sublabel="Needs attention" accent={ACCENTS.coral} sparkData={[2, 1, 2, 1, 1, 1]} />
          <StatCard icon={TrendingUp} label="Avg. confidence" value={stats.avgConf} suffix="%" sublabel="Model certainty" accent={ACCENTS.emerald} sparkData={[81, 83, 85, 84, 87, 89]} />
        </div>

        <div className="rounded-2xl p-5 mb-6 backdrop-blur-xl border" style={{ background: "rgba(16,21,42,0.55)", borderColor: "rgba(255,255,255,0.08)" }}>
          <div className="flex items-center justify-between mb-3">
            <h2 style={{ fontFamily: "'Space Grotesk', sans-serif", fontWeight: 600, color: "#eef1fb" }} className="text-base">
              Scan volume · last 14 days
            </h2>
            <span style={{ color: "#6b7291", fontFamily: "'JetBrains Mono', monospace" }} className="text-xs">
              +23% vs prior period
            </span>
          </div>
          <div style={{ width: "100%", height: 180 }}>
            <ResponsiveContainer>
              <AreaChart data={SCAN_VOLUME} margin={{ top: 5, right: 5, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="scanGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={ACCENTS.cyan} stopOpacity={0.45} />
                    <stop offset="100%" stopColor={ACCENTS.cyan} stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="day" tick={{ fill: "#6b7291", fontSize: 10 }} axisLine={false} tickLine={false} interval={1} />
                <YAxis tick={{ fill: "#6b7291", fontSize: 10 }} axisLine={false} tickLine={false} width={28} />
                <Tooltip content={<CustomTooltip />} />
                <Area type="monotone" dataKey="scans" stroke={ACCENTS.cyan} strokeWidth={2} fill="url(#scanGradient)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-2xl overflow-hidden backdrop-blur-xl border" style={{ background: "rgba(16,21,42,0.55)", borderColor: "rgba(255,255,255,0.08)" }}>
          <div className="flex flex-col gap-4 px-5 py-4 border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
            <div className="flex items-center justify-between gap-4">
              <h2 style={{ fontFamily: "'Space Grotesk', sans-serif", fontWeight: 600, color: "#eef1fb" }} className="text-base">
                Patients
              </h2>
              <div className="relative w-full max-w-[260px]">
                <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2" style={{ color: "#6b7291" }} />
                <input
                  value={query}
                  onChange={(e) => {
                    setQuery(e.target.value);
                    setPage(0);
                  }}
                  placeholder="Search patients..."
                  className="w-full pl-9 pr-3 py-2 rounded-lg text-sm outline-none"
                  style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", color: "#eef1fb" }}
                />
              </div>
            </div>
            <div className="flex flex-wrap gap-2">
              {["All", "Stable", "Monitoring", "Critical", "Reviewing"].map((s) => (
                <FilterChip
                  key={s}
                  label={s}
                  count={statusCounts[s]}
                  active={statusFilter === s}
                  accent={s === "All" ? ACCENTS.violet : STATUS_STYLE[s].color}
                  onClick={() => {
                    setStatusFilter(s);
                    setPage(0);
                  }}
                />
              ))}
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr style={{ color: "#6b7291" }} className="text-left text-[11px] uppercase tracking-wider">
                  <SortHeader label="Patient" sortField="name" />
                  <th className="px-5 py-3 font-medium hidden sm:table-cell">MRI region</th>
                  <SortHeader label="Confidence" sortField="confidence" />
                  <th className="px-5 py-3 font-medium">Status</th>
                  <SortHeader label="Last scan" sortField="lastScan" className="hidden md:table-cell" />
                </tr>
              </thead>
              <tbody>
                {pageItems.map((p) => {
                  const s = STATUS_STYLE[p.status];
                  const globalIndex = PATIENTS.findIndex((x) => x.id === p.id);
                  return (
                    <tr
                      key={p.id}
                      onClick={() => setSelectedPatient(p)}
                      className="border-t cursor-pointer transition-colors hover:bg-white/[0.03]"
                      style={{ borderColor: "rgba(255,255,255,0.05)" }}
                    >
                      <td className="px-5 py-3.5">
                        <div className="flex items-center gap-3">
                          <Avatar name={p.name} index={globalIndex} />
                          <div>
                            <div style={{ color: "#eef1fb" }} className="font-medium">
                              {p.name}
                            </div>
                            <div style={{ color: "#6b7291", fontFamily: "'JetBrains Mono', monospace" }} className="text-xs">
                              {p.id} · Age {p.age}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="px-5 py-3.5 hidden sm:table-cell" style={{ color: "#b7bdd6" }}>
                        {p.region}
                      </td>
                      <td className="px-5 py-3.5">
                        <div className="flex items-center gap-2">
                          <div className="w-16 h-1.5 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.08)" }}>
                            <div
                              className="h-full rounded-full"
                              style={{
                                width: `${p.confidence}%`,
                                background: p.confidence >= 85 ? ACCENTS.emerald : p.confidence >= 65 ? ACCENTS.amber : ACCENTS.coral,
                              }}
                            />
                          </div>
                          <span style={{ fontFamily: "'JetBrains Mono', monospace", color: "#b7bdd6" }} className="text-xs tabular-nums">
                            {p.confidence}%
                          </span>
                        </div>
                      </td>
                      <td className="px-5 py-3.5">
                        <span
                          className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                          style={{ color: s.color, background: s.bg, border: `1px solid ${s.ring}` }}
                        >
                          {p.status}
                        </span>
                      </td>
                      <td className="px-5 py-3.5 hidden md:table-cell" style={{ color: "#6b7291", fontFamily: "'JetBrains Mono', monospace" }}>
                        {p.lastScan}
                      </td>
                    </tr>
                  );
                })}
                {pageItems.length === 0 && (
                  <tr>
                    <td colSpan={5} className="px-5 py-10 text-center text-sm" style={{ color: "#6b7291" }}>
                      No patients match your filters.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          <div className="flex items-center justify-between px-5 py-4 border-t" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
            <span className="text-xs" style={{ color: "#6b7291" }}>
              {filtered.length === 0 ? "0" : `${pageSafe * PAGE_SIZE + 1}–${Math.min(filtered.length, pageSafe * PAGE_SIZE + PAGE_SIZE)}`} of {filtered.length}
            </span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setPage((p) => Math.max(0, p - 1))}
                disabled={pageSafe === 0}
                className="p-1.5 rounded-lg disabled:opacity-30 hover:bg-white/5 transition-colors"
                style={{ color: "#b7bdd6" }}
                aria-label="Previous page"
              >
                <ChevronLeft size={16} />
              </button>
              <span style={{ fontFamily: "'JetBrains Mono', monospace", color: "#6b7291" }} className="text-xs">
                {pageSafe + 1} / {pageCount}
              </span>
              <button
                onClick={() => setPage((p) => Math.min(pageCount - 1, p + 1))}
                disabled={pageSafe >= pageCount - 1}
                className="p-1.5 rounded-lg disabled:opacity-30 hover:bg-white/5 transition-colors"
                style={{ color: "#b7bdd6" }}
                aria-label="Next page"
              >
                <ChevronRight size={16} />
              </button>
            </div>
          </div>
        </div>
      </div>

      {selectedPatient && (
        <DetailDrawer
          patient={selectedPatient}
          index={PATIENTS.findIndex((x) => x.id === selectedPatient.id)}
          onClose={() => setSelectedPatient(null)}
        />
      )}
    </div>
  );
}