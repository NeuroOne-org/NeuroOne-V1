import { forwardRef } from "react";
import { cn } from "@/lib/utils";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, error, ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={cn(
          "h-10 w-full rounded border bg-raised px-3 text-sm text-text placeholder:text-text-faint transition-colors",
          "focus:outline-none focus:ring-1 focus:ring-indigo focus:border-indigo",
          error ? "border-amber/60" : "border-line",
          className
        )}
        {...props}
      />
    );
  }
);
Input.displayName = "Input";

export function FieldError({ message }: { message?: string }) {
  if (!message) return null;
  return <p className="mt-1 text-[12px] text-amber">{message}</p>;
}

export function Label({
  children,
  htmlFor,
}: {
  children: React.ReactNode;
  htmlFor?: string;
}) {
  return (
    <label
      htmlFor={htmlFor}
      className="mb-1.5 block text-[13px] font-medium text-text-muted"
    >
      {children}
    </label>
  );
}
