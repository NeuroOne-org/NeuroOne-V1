"use client";

import { useEffect, useId, useState } from "react";
import { cn } from "@/lib/utils";

interface ConfidenceDialProps {
  /** 0–1 */
  value: number;
  tone?: "teal" | "amber";
  label?: string;
  size?: number;
}

/**
 * Instrument-style radial gauge, deliberately modeled on the sweep
 * indicators found on radiology/monitoring equipment rather than a
 * generic donut chart. Ticks mark 0/25/50/75/100; the arc sweeps in
 * on mount to draw attention to the number that matters most on the
 * results page.
 */
export function ConfidenceDial({
  value,
  tone = "teal",
  label,
  size = 168,
}: ConfidenceDialProps) {
  const id = useId();
  const [mounted, setMounted] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setMounted(true), 30);
    return () => clearTimeout(t);
  }, []);

  const stroke = 10;
  const r = (size - stroke) / 2;
  const cx = size / 2;
  const cy = size / 2;

  // 270 degree sweep, starting at 135deg (bottom-left) going clockwise
  const startAngle = 135;
  const sweepAngle = 270;
  const circumference = 2 * Math.PI * r;
  const arcLength = (sweepAngle / 360) * circumference;

  const target = arcLength * (1 - value);
  const full = arcLength;

  const colorVar = tone === "amber" ? "#FF6A3D" : "#35D6C8";

  const ticks = [0, 0.25, 0.5, 0.75, 1];

  function polar(angleDeg: number, radius: number) {
    const rad = (angleDeg * Math.PI) / 180;
    return { x: cx + radius * Math.cos(rad), y: cy + radius * Math.sin(rad) };
  }

  return (
    <div className="flex flex-col items-center">
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className="-rotate-[0deg]"
      >
        <defs>
          <filter id={`glow-${id}`}>
            <feGaussianBlur stdDeviation="2.5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* track */}
        <circle
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke="#1D2126"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={`${arcLength} ${circumference}`}
          strokeDashoffset={0}
          transform={`rotate(${startAngle} ${cx} ${cy})`}
        />

        {/* ticks */}
        {ticks.map((t) => {
          const angle = startAngle + t * sweepAngle;
          const outer = polar(angle, r + stroke / 2 + 4);
          const inner = polar(angle, r - stroke / 2 - 2);
          return (
            <line
              key={t}
              x1={inner.x}
              y1={inner.y}
              x2={outer.x}
              y2={outer.y}
              stroke="#565C66"
              strokeWidth={1.5}
            />
          );
        })}

        {/* value arc */}
        <circle
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke={colorVar}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={`${arcLength} ${circumference}`}
          strokeDashoffset={mounted ? target : full}
          style={{
            transition: "stroke-dashoffset 1.1s cubic-bezier(0.16,1,0.3,1)",
            filter: `url(#glow-${id})`,
          }}
          transform={`rotate(${startAngle} ${cx} ${cy})`}
        />

        <text
          x={cx}
          y={cy - 4}
          textAnchor="middle"
          className="font-mono"
          fontSize={size * 0.19}
          fill="#E7E9EC"
          fontWeight={500}
        >
          {Math.round(value * 100)}
          <tspan fontSize={size * 0.09} fill="#8A9099">
            %
          </tspan>
        </text>
        <text
          x={cx}
          y={cy + size * 0.14}
          textAnchor="middle"
          fontSize={size * 0.065}
          fill="#565C66"
          className="font-mono uppercase"
          style={{ letterSpacing: "0.1em" }}
        >
          confidence
        </text>
      </svg>
      {label && (
        <p
          className={cn(
            "mt-1 font-mono text-[11px] uppercase tracking-[0.12em]",
            tone === "amber" ? "text-amber" : "text-teal"
          )}
        >
          {label}
        </p>
      )}
    </div>
  );
}
