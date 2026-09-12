import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Channel triplets live in globals.css so both themes share these
        // class names; `<alpha-value>` keeps `/30`-style modifiers working.
        ink: "rgb(var(--ink) / <alpha-value>)",
        panel: "rgb(var(--panel) / <alpha-value>)",
        raised: "rgb(var(--raised) / <alpha-value>)",
        line: "rgb(var(--line) / <alpha-value>)",
        "line-soft": "rgb(var(--line-soft) / <alpha-value>)",
        text: {
          DEFAULT: "rgb(var(--text) / <alpha-value>)",
          muted: "rgb(var(--text-muted) / <alpha-value>)",
          faint: "rgb(var(--text-faint) / <alpha-value>)",
        },
        amber: {
          DEFAULT: "rgb(var(--amber) / <alpha-value>)",
          soft: "rgb(var(--amber) / 0.1)",
        },
        teal: {
          DEFAULT: "rgb(var(--teal) / <alpha-value>)",
          soft: "rgb(var(--teal) / 0.1)",
        },
        indigo: {
          DEFAULT: "rgb(var(--indigo) / <alpha-value>)",
          soft: "rgb(var(--indigo) / 0.1)",
        },
      },
      fontFamily: {
        display: ["var(--font-display)", "sans-serif"],
        body: ["var(--font-body)", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"],
      },
      transitionTimingFunction: {
        out: "var(--ease-out)",
        "in-out": "var(--ease-in-out)",
        drawer: "var(--ease-drawer)",
      },
      borderRadius: {
        sm: "4px",
        DEFAULT: "6px",
        md: "8px",
        lg: "12px",
      },
      keyframes: {
        scan: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100%)" },
        },
        "dial-sweep": {
          "0%": { strokeDashoffset: "var(--dial-full)" },
          "100%": { strokeDashoffset: "var(--dial-target)" },
        },
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "node-pulse": {
          "0%, 100%": { opacity: "0.35", transform: "scale(1)" },
          "50%": { opacity: "1", transform: "scale(1.6)" },
        },
        "synapse-flow": {
          "0%": { strokeDashoffset: "1" },
          "100%": { strokeDashoffset: "0" },
        },
        "rotate-slow": {
          "0%": { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
        "drift": {
          "0%, 100%": { transform: "translate(0, 0)" },
          "50%": { transform: "translate(14px, -10px)" },
        },
        "tilt-3d": {
          "0%, 100%": { transform: "rotateX(8deg) rotateY(-14deg) rotateZ(0deg)" },
          "50%": { transform: "rotateX(-6deg) rotateY(14deg) rotateZ(2deg)" },
        },
        "float-particle": {
          "0%, 100%": { transform: "translate3d(0, 0, 0)", opacity: "0.2" },
          "50%": { transform: "translate3d(6px, -18px, 30px)", opacity: "0.9" },
        },
      },
      animation: {
        scan: "scan 2.4s linear infinite",
        "dial-sweep": "dial-sweep 1.1s cubic-bezier(0.16,1,0.3,1) forwards",
        "fade-up": "fade-up 0.4s var(--ease-out) both",
        "node-pulse": "node-pulse 2.8s ease-in-out infinite",
        "rotate-slow": "rotate-slow 60s linear infinite",
        drift: "drift 8s ease-in-out infinite",
        "tilt-3d": "tilt-3d 14s ease-in-out infinite",
        "float-particle": "float-particle 6s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};

export default config;
