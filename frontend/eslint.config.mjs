import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";

export default defineConfig([
  ...nextVitals,
  {
    // eslint-config-next 16 ships the React Compiler rules as errors. The
    // existing hooks predate them, and rewriting those hooks is a behaviour
    // change of its own, so they report as warnings until that is done.
    rules: {
      "react-hooks/set-state-in-effect": "warn",
      "react-hooks/refs": "warn",
      "react-hooks/purity": "warn",
    },
  },
  // web-page/ is a separate Next app with its own config and node_modules.
  globalIgnores([".next/**", ".next-verify/**", "out/**", "build/**", "next-env.d.ts", "web-page/**"]),
]);
