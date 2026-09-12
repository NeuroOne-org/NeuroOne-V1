interface Rule {
  label: string;
  test: (value: string) => boolean;
}

const RULES: Rule[] = [
  { label: "8+ characters", test: (v) => v.length >= 8 },
  { label: "Uppercase letter", test: (v) => /[A-Z]/.test(v) },
  { label: "Lowercase letter", test: (v) => /[a-z]/.test(v) },
  { label: "Number", test: (v) => /[0-9]/.test(v) },
  { label: "Special character", test: (v) => /[^A-Za-z0-9]/.test(v) },
];

export function PasswordStrength({ value }: { value: string }) {
  if (!value) return null;

  const passed = RULES.filter((rule) => rule.test(value)).length;
  const barClass =
    passed <= 2 ? "bg-brand-amber" : passed <= 4 ? "bg-product-primary" : "bg-brand-teal";

  return (
    <div className="mt-3" aria-live="polite">
      <div className="mb-2 flex h-1 gap-1" aria-hidden="true">
        {RULES.map((_, i) => (
          <div
            key={i}
            className={`h-full flex-1 rounded-full transition-colors ${i < passed ? barClass : "bg-product-border"}`}
          />
        ))}
      </div>
      <ul className="grid grid-cols-2 gap-x-3 gap-y-1">
        {RULES.map((rule) => {
          const ok = rule.test(value);
          return (
            <li
              key={rule.label}
              className={`text-[12px] leading-5 transition-colors ${ok ? "text-product-ink" : "text-product-ink-soft"}`}
            >
              {ok ? "✓" : "·"} {rule.label}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
