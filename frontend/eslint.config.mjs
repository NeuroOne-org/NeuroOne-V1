import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";

export default defineConfig([
  ...nextVitals,
  // web-page/ is a separate Next app with its own config and node_modules.
  globalIgnores([".next/**", ".next-verify/**", "out/**", "build/**", "next-env.d.ts", "web-page/**"]),
]);
