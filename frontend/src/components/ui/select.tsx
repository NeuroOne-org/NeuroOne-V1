import { forwardRef } from "react";
import { ChevronDown } from "@/components/icons";
import { cn } from "@/lib/utils";

interface SelectProps
  extends React.SelectHTMLAttributes<HTMLSelectElement> {
  error?: string;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, error, children, ...props }, ref) => {
    return (
      <div className="relative">
        <select
          ref={ref}
          className={cn(
            "h-10 w-full appearance-none rounded border bg-raised px-3 pr-9 text-sm text-text transition-colors",
            "focus:outline-none focus:ring-1 focus:ring-indigo focus:border-indigo",
            error ? "border-amber/60" : "border-line",
            className
          )}
          {...props}
        >
          {children}
        </select>
        <ChevronDown className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-faint" />
      </div>
    );
  }
);
Select.displayName = "Select";

export const Textarea = forwardRef<
  HTMLTextAreaElement,
  React.TextareaHTMLAttributes<HTMLTextAreaElement>
>(({ className, ...props }, ref) => (
  <textarea
    ref={ref}
    className={cn(
      "w-full rounded border border-line bg-raised px-3 py-2 text-sm text-text placeholder:text-text-faint transition-colors",
      "focus:outline-none focus:ring-1 focus:ring-indigo focus:border-indigo",
      className
    )}
    {...props}
  />
));
Textarea.displayName = "Textarea";

export const Checkbox = forwardRef<
  HTMLInputElement,
  React.InputHTMLAttributes<HTMLInputElement>
>(({ className, ...props }, ref) => (
  <input
    ref={ref}
    type="checkbox"
    className={cn(
      "h-4 w-4 rounded-sm border border-line bg-raised accent-indigo",
      className
    )}
    {...props}
  />
));
Checkbox.displayName = "Checkbox";
