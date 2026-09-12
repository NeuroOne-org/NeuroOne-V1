"use client";

/**
 * Theme toggle.
 *
 * Adapted from kokonutui's Switch Button (MIT, @dorianbaffier,
 * https://kokonutui.com/docs/buttons/switch-button). Three changes were
 * needed to fit this codebase: the zinc scale is mapped onto our own surface
 * tokens so it themes with everything else, the Tailwind v4 gradient syntax
 * is rewritten for v3, and the icon comes from the Keyline set rather than
 * lucide. The rotating sun, the shimmer sweep and the crossfading label are
 * the original's.
 */

import { useTheme } from "next-themes";
import { Sun } from "@/components/icons";
import { useHydrated } from "@/hooks/use-hydrated";
import { cn } from "@/lib/utils";

interface SwitchButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  size?: "sm" | "default" | "lg";
  showLabel?: boolean;
}

const sizes = {
  sm: "h-8 px-3 text-[13px]",
  default: "h-10 px-4 text-sm",
  lg: "h-11 px-5 text-sm",
};

export default function SwitchButton({
  className,
  size = "default",
  showLabel = true,
  ...props
}: SwitchButtonProps) {
  const { setTheme, resolvedTheme } = useTheme();

  // The server cannot know the stored theme, so the button renders inert
  // until the client has read it. Without this it flashes the wrong label.
  const mounted = useHydrated();

  const isDark = resolvedTheme === "dark";

  if (!mounted) {
    return (
      <div
        className={cn(
          "w-full rounded-md border border-line bg-raised/50",
          sizes[size],
          className
        )}
        aria-hidden="true"
      />
    );
  }

  return (
    <button
      type="button"
      onClick={() => setTheme(isDark ? "light" : "dark")}
      aria-label={`Switch to ${isDark ? "light" : "dark"} theme`}
      className={cn(
        "group relative isolate w-full overflow-hidden rounded-md",
        "inline-flex items-center justify-center",
        "border border-line bg-gradient-to-b from-raised to-panel",
        "text-text-muted",
        "transition-[border-color,color,transform] duration-200 ease-out",
        "hover:border-text-faint/60 hover:text-text active:scale-[0.97]",
        sizes[size],
        className
      )}
      {...props}
    >
      <span className="relative z-10 flex items-center gap-2">
        <Sun
          className={cn(
            "transform-gpu transition-transform duration-700 ease-in-out",
            size === "sm" && "h-3.5 w-3.5",
            size === "default" && "h-4 w-4",
            size === "lg" && "h-5 w-5",
            "group-hover:rotate-[360deg] group-hover:scale-110",
            isDark ? "rotate-180 text-text-muted" : "rotate-0 text-amber",
            "group-active:scale-95"
          )}
        />
        {showLabel && (
          // Both labels are laid on top of each other and crossfaded, so the
          // button never changes width as the word changes.
          <span className="relative font-medium">
            <span
              className={cn(
                "absolute inset-0 transition-opacity duration-300 ease-out",
                isDark ? "opacity-0" : "opacity-100"
              )}
            >
              Light
            </span>
            <span
              className={cn(
                "absolute inset-0 transition-opacity duration-300 ease-out",
                isDark ? "opacity-100" : "opacity-0"
              )}
            >
              Dark
            </span>
            <span className="opacity-0">Light</span>
          </span>
        )}
      </span>

      {/* Shimmer sweep */}
      <span
        aria-hidden="true"
        className={cn(
          "pointer-events-none absolute inset-0 z-[1]",
          "bg-gradient-to-r from-transparent via-text/[0.07] to-transparent",
          "translate-x-[-100%] transition-transform duration-500 ease-in-out",
          "group-hover:translate-x-[100%]"
        )}
      />

      {/* Radial lift on hover */}
      <span
        aria-hidden="true"
        className={cn(
          "pointer-events-none absolute inset-0 z-[2] opacity-0",
          "bg-[radial-gradient(circle_at_50%_50%,rgb(var(--text)/0.06),transparent_70%)]",
          "transition-opacity duration-500 group-hover:opacity-100"
        )}
      />
    </button>
  );
}
