import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        product: {
          bg: "#EAF3FB",
          surface: "#FFFFFF",
          ink: "#0F2A43",
          "ink-soft": "#4B6076",
          border: "rgba(15,42,67,0.12)",
          primary: "#2F6FA6",
          "primary-hover": "#255A87",
        },
        brand: {
          navy: "#151B4D",
          indigo: "#3D3AA8",
          violet: "#6C4FE0",
          teal: "#2FB6A3",
          amber: "#F4C338",
        },
      },
      fontFamily: { body: ["IBM Plex Sans", "sans-serif"] },
      borderRadius: { DEFAULT: "6px", md: "8px", lg: "12px" },
    },
  },
  plugins: [],
};

export default config;
