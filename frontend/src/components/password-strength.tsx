import { cn } from "@/lib/utils";

interface Rule {
  label: string;
  test: (v: string) => boolean;
}

const RULES: Rule[] = [
  { label: "8+ characters", test: (v) => v.length >= 8 },
  { label: "Uppercase letter", test: (v) => /[A-Z]/.test(v) },
  { label: "Lowercase letter", test: (v) => /[a-z]/.test(v) },
  { label: "Number", test: (v) => /[0-9]/.test(v) },
  { label: "Special character", test: (v) => /[^A-Za-z0-9]/.test(v) },
];

export function PasswordStrength({ value }: { value: string }) {
  const passed = RULES.filter((r) => r.test(value)).length;
  const tone =
    passed <= 2 ? "amber" : passed <= 4 ? "indigo" : "teal";

  if (!value) return null;

  return (
    <div className="mt-2">
      <div className="mb-2 flex h-1 gap-1">
        {RULES.map((_, i) => (
          <div
            key={i}
            className={cn(
              "h-full flex-1 rounded-full transition-colors",
              i < passed
                ? tone === "amber"
                  ? "bg-amber"
                  : tone === "indigo"
                  ? "bg-indigo"
                  : "bg-teal"
                : "bg-line"
            )}
          />
        ))}
      </div>
      <ul className="grid grid-cols-2 gap-x-3 gap-y-1">
        {RULES.map((rule) => {
          const ok = rule.test(value);
          return (
            <li
              key={rule.label}
              className={cn(
                "text-[11px] transition-colors",
                ok ? "text-teal" : "text-text-faint"
              )}
            >
              {ok ? "✓" : "·"} {rule.label}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
