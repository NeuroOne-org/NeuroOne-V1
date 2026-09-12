"use client";

/**
 * Queue filter cards.
 *
 * Spotlight Cards by kokonutui (MIT, @dorianbaffier,
 * https://kokonutui.com/docs/cards/spotlight-cards), reworked from a static
 * feature grid into the queue's filter control: aurora tint, magnetic 3D
 * tilt, and siblings dimming on hover are kept; the cards are now buttons
 * that carry a pressed state and a live count.
 *
 * The accent colour is not decorative here. It is the same amber/indigo/teal
 * meaning the rest of the app uses, read from the palette at runtime so the
 * cards re-tint with the theme.
 */

import { useRef, useState } from "react";
import {
  motion,
  useMotionValue,
  useReducedMotion,
  useSpring,
  useTransform,
} from "framer-motion";
import { cn } from "@/lib/utils";

/** `--amber` + 0.2 -> `rgb(var(--amber) / 0.2)`; omit alpha for the solid colour. */
function tint(cssVar: string, alpha?: number): string {
  return alpha === undefined
    ? `rgb(var(${cssVar}))`
    : `rgb(var(${cssVar}) / ${alpha})`;
}

const TILT_MAX = 9;
const TILT_SPRING = { stiffness: 300, damping: 28 } as const;
const GLOW_SPRING = { stiffness: 180, damping: 22 } as const;

export type QueueFilter = "all" | "sign_off" | "worsening" | "early_watch";

export interface FilterCard {
  key: QueueFilter;
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  /** Undefined until the count is known — renders an em dash, never a zero. */
  count: number | undefined;
  description: string;
  /** A palette variable name, e.g. `--amber`. */
  accentVar: string;
}

interface CardProps {
  card: FilterCard;
  active: boolean;
  dimmed: boolean;
  onSelect: () => void;
  onHoverStart: () => void;
  onHoverEnd: () => void;
}

function Card({
  card,
  active,
  dimmed,
  onSelect,
  onHoverStart,
  onHoverEnd,
}: CardProps) {
  const Icon = card.icon;
  const cardRef = useRef<HTMLButtonElement>(null);
  const reduceMotion = useReducedMotion();

  const normX = useMotionValue(0.5);
  const normY = useMotionValue(0.5);

  const rawRotateX = useTransform(normY, [0, 1], [TILT_MAX, -TILT_MAX]);
  const rawRotateY = useTransform(normX, [0, 1], [-TILT_MAX, TILT_MAX]);

  const rotateX = useSpring(rawRotateX, TILT_SPRING);
  const rotateY = useSpring(rawRotateY, TILT_SPRING);
  const glowOpacity = useSpring(0, GLOW_SPRING);

  const accent = (alpha?: number) => tint(card.accentVar, alpha);

  function handleMouseMove(e: React.MouseEvent<HTMLButtonElement>) {
    // Springs run on their own loop, so the global prefers-reduced-motion
    // CSS rule cannot reach them — the tilt is switched off here instead.
    if (reduceMotion) return;
    const el = cardRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    normX.set((e.clientX - rect.left) / rect.width);
    normY.set((e.clientY - rect.top) / rect.height);
  }

  function handleMouseEnter() {
    glowOpacity.set(1);
    onHoverStart();
  }

  function handleMouseLeave() {
    normX.set(0.5);
    normY.set(0.5);
    glowOpacity.set(0);
    onHoverEnd();
  }

  return (
    <motion.button
      ref={cardRef}
      type="button"
      onClick={onSelect}
      aria-pressed={active}
      // The visible card is an icon, a title, a number and a hint spread over
      // several spans. Spelling the name out gives a screen reader the one
      // sentence a sighted user assembles at a glance.
      aria-label={
        card.count === undefined
          ? `Filter: ${card.title}`
          : `Filter: ${card.title}, ${card.count} ${
              card.count === 1 ? "case" : "cases"
            }`
      }
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onMouseMove={handleMouseMove}
      animate={{
        scale: dimmed ? 0.97 : 1,
        // 0.55 reads as "disabled" against a white card, where there is no
        // dark ground for the fade to sink into. The scale carries most of
        // the focus shift; the opacity only has to support it.
        opacity: dimmed ? 0.68 : 1,
      }}
      transition={{ duration: 0.18, ease: [0.23, 1, 0.32, 1] }}
      style={{
        rotateX: reduceMotion ? 0 : rotateX,
        rotateY: reduceMotion ? 0 : rotateY,
        transformPerspective: 900,
      }}
      className={cn(
        "group relative flex flex-col gap-3 overflow-hidden rounded-md border p-4 text-left",
        "transition-[border-color,background-color] duration-300",
        active
          ? "border-text-faint/50 bg-panel"
          : "border-line bg-panel hover:border-text-faint/40"
      )}
    >
      {/* Resting accent tint */}
      <span
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 rounded-md"
        style={{
          background: `radial-gradient(ellipse at 20% 20%, ${accent(
            active ? 0.14 : 0.07
          )}, transparent 65%)`,
        }}
      />

      {/* Hover aurora */}
      <motion.span
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 rounded-md"
        style={{
          opacity: glowOpacity,
          background: `radial-gradient(ellipse at 20% 20%, ${accent(0.2)}, transparent 65%)`,
        }}
      />

      <span className="relative z-10 flex items-center gap-2">
        <span
          className="flex h-7 w-7 items-center justify-center rounded"
          // The icon draws with `currentColor`, so the accent is set once
          // here rather than threaded through the icon's props.
          style={{
            background: accent(0.12),
            boxShadow: `inset 0 0 0 1px ${accent(0.28)}`,
            color: accent(),
          }}
        >
          <Icon className="h-3.5 w-3.5" />
        </span>
        <span className="label-eyebrow">{card.title}</span>
      </span>

      <span className="relative z-10 flex flex-col">
        <span className="data-num text-2xl text-text">
          {card.count === undefined ? "—" : card.count}
        </span>
        <span className="mt-0.5 text-[12px] text-text-faint">
          {card.description}
        </span>
      </span>

      {/* Accent underline: sweeps in on hover, stays put while selected. */}
      <span
        aria-hidden="true"
        className={cn(
          "absolute bottom-0 left-0 h-[2px] rounded-full transition-all duration-500 ease-out",
          active ? "w-full" : "w-0 group-hover:w-full"
        )}
        style={{
          background: `linear-gradient(to right, ${accent(0.75)}, transparent)`,
        }}
      />
    </motion.button>
  );
}

export function QueueFilterCards({
  cards,
  active,
  onChange,
}: {
  cards: FilterCard[];
  active: QueueFilter;
  onChange: (filter: QueueFilter) => void;
}) {
  const [hovered, setHovered] = useState<QueueFilter | null>(null);

  return (
    <div
      role="group"
      aria-label="Filter the queue"
      className="grid grid-cols-2 gap-3 lg:grid-cols-4"
    >
      {cards.map((card) => (
        <Card
          key={card.key}
          card={card}
          active={active === card.key}
          dimmed={hovered !== null && hovered !== card.key}
          onSelect={() => onChange(card.key)}
          onHoverStart={() => setHovered(card.key)}
          onHoverEnd={() => setHovered(null)}
        />
      ))}
    </div>
  );
}
