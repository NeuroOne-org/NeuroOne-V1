import { forwardRef } from "react";
import { Loader } from "@/components/icons";
import { cn } from "@/lib/utils";

type Variant = "primary" | "secondary" | "ghost" | "danger";
type Size = "sm" | "md" | "lg";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
  isLoading?: boolean;
}

const variantClasses: Record<Variant, string> = {
  primary:
    "bg-indigo text-white hover:bg-indigo/90 border border-transparent",
  secondary:
    "bg-transparent text-text border border-line hover:border-text-faint hover:bg-raised",
  ghost: "bg-transparent text-text-muted hover:text-text hover:bg-raised border border-transparent",
  danger:
    "bg-transparent text-amber border border-amber/30 hover:bg-amber-soft",
};

const sizeClasses: Record<Size, string> = {
  sm: "h-8 px-3 text-[13px]",
  md: "h-10 px-4 text-sm",
  lg: "h-11 px-6 text-sm",
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    { className, variant = "primary", size = "md", isLoading, children, disabled, ...props },
    ref
  ) => {
    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(
          // Named properties rather than `all`, and a press scale so the
          // button confirms it heard the click before the network does.
          "inline-flex items-center justify-center gap-2 rounded font-medium",
          "transition-[transform,background-color,border-color,color,opacity] duration-150 ease-out",
          "active:scale-[0.97] disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100",
          variantClasses[variant],
          sizeClasses[size],
          className
        )}
        {...props}
      >
        {isLoading && <Loader className="h-4 w-4 animate-spin" />}
        {children}
      </button>
    );
  }
);
Button.displayName = "Button";
