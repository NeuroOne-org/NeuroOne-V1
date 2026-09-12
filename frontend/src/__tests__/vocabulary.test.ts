import { readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";

/**
 * Copy rules from ADR-006 and the REPORT-01D checklist, enforced on source.
 *
 * Scoped to the clinical UI: the dashboard and shared components. The
 * marketing landing page is out of scope for this check.
 */
const SRC = path.resolve(__dirname, "..");
const ROOTS = ["app/dashboard", "components"];
const EXCLUDED = [path.join("components", "landing")];

const RULES: { name: string; pattern: RegExp }[] = [
  { name: '"certainty" copy', pattern: /certainty/i },
  {
    name: "severity vocabulary with no backing in the model",
    pattern: /\b(Critical|Stable|Monitoring)\b/,
  },
  { name: "a stage label rendered as a headline", pattern: /stageLabel\(/ },
  {
    name: "a hardcoded confidence above the 0.92 ceiling",
    pattern: /confidence\s*[:=]\s*(0?\.9[3-9]|1(\.0+)?)\b/,
  },
];

function sourceFiles(dir: string): string[] {
  return readdirSync(dir).flatMap((name) => {
    const full = path.join(dir, name);
    const relative = path.relative(SRC, full);
    if (EXCLUDED.some((excluded) => relative.startsWith(excluded))) return [];
    if (statSync(full).isDirectory()) return sourceFiles(full);
    return /\.(ts|tsx)$/.test(name) ? [full] : [];
  });
}

describe("clinical UI vocabulary", () => {
  const files = ROOTS.flatMap((root) => sourceFiles(path.join(SRC, root)));

  it("scans a non-trivial set of files", () => {
    expect(files.length).toBeGreaterThan(10);
  });

  for (const rule of RULES) {
    it(`contains no ${rule.name}`, () => {
      const offenders = files.flatMap((file) =>
        readFileSync(file, "utf8")
          .split("\n")
          .map((line, i) => ({ line, i }))
          .filter(({ line }) => rule.pattern.test(line))
          .map(({ line, i }) => `${path.relative(SRC, file)}:${i + 1}: ${line.trim()}`)
      );
      expect(offenders).toEqual([]);
    });
  }
});
