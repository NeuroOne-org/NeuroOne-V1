import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0B0D10",
        panel: "#14171B",
        raised: "#1B1F24",
        line: "#262B31",
        "line-soft": "#1D2126",
        text: {
          DEFAULT: "#E7E9EC",
          muted: "#8A9099",
          faint: "#565C66",
        },
        amber: {
          DEFAULT: "#FF6A3D",
          soft: "#FF6A3D1A",
        },
        teal: {
          DEFAULT: "#35D6C8",
          soft: "#35D6C81A",
        },
        indigo: {
          DEFAULT: "#6E7BFF",
          soft: "#6E7BFF1A",
        },
      },
      fontFamily: {
        display: ["var(--font-display)", "sans-serif"],
        body: ["var(--font-body)", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"],
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
          "0%": { opacity: "0", transform: "translateY(6px)" },
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
        "fade-up": "fade-up 0.4s ease-out forwards",
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
