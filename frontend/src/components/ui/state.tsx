import {
  ChevronLeft,
  ChevronRight,
  CircleAlert,
  RefreshCw,
} from "@/components/icons";
import { cn } from "@/lib/utils";

/**
 * Loading, empty, error and paging — the four states every list in this app
 * has to render, kept together so they look the same wherever they appear.
 */

export function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={cn("animate-pulse rounded bg-raised", className)}
      aria-hidden="true"
    />
  );
}

export function TableSkeleton({ rows = 6, cols = 4 }: { rows?: number; cols?: number }) {
  return (
    <div className="divide-y divide-line">
      {Array.from({ length: rows }).map((_, r) => (
        <div key={r} className="flex items-center gap-4 px-5 py-4">
          {Array.from({ length: cols }).map((_, c) => (
            <Skeleton
              key={c}
              className={cn("h-4", c === 0 ? "w-48" : "flex-1")}
              // A short, offset stagger reads as one surface filling in
              // rather than N independent blocks pulsing at random.
            />
          ))}
        </div>
      ))}
    </div>
  );
}

export function ErrorState({
  message,
  onRetry,
}: {
  message: string;
  onRetry?: () => void;
}) {
  return (
    <div className="flex flex-col items-center gap-3 px-5 py-12 text-center">
      <CircleAlert className="h-6 w-6 text-amber" />
      <p className="max-w-sm text-[13px] text-text-muted">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className={cn(
            "inline-flex items-center gap-2 rounded border border-line px-3 py-1.5 text-[13px] text-text",
            "transition-[background-color,border-color,transform] duration-150 ease-out",
            "hover:border-text-faint hover:bg-raised active:scale-[0.97]"
          )}
        >
          <RefreshCw className="h-3.5 w-3.5" />
          Try again
        </button>
      )}
    </div>
  );
}

export function EmptyState({
  icon: Icon,
  title,
  hint,
  action,
}: {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  hint?: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="flex flex-col items-center gap-3 px-5 py-14 text-center">
      <div className="flex h-11 w-11 items-center justify-center rounded-full border border-line bg-raised">
        <Icon className="h-5 w-5 text-text-faint" />
      </div>
      <div>
        <p className="text-sm text-text">{title}</p>
        {hint && <p className="mt-1 text-[13px] text-text-muted">{hint}</p>}
      </div>
      {action}
    </div>
  );
}

export function Pager({
  page,
  pageCount,
  total,
  pageSize,
  onPrev,
  onNext,
}: {
  page: number;
  pageCount: number;
  total: number;
  pageSize: number;
  onPrev: () => void;
  onNext: () => void;
}) {
  const first = total === 0 ? 0 : (page - 1) * pageSize + 1;
  const last = Math.min(total, page * pageSize);

  const buttonClass = cn(
    "rounded border border-line p-1.5 text-text-muted",
    "transition-[background-color,border-color,color,transform] duration-150 ease-out",
    "hover:border-text-faint hover:bg-raised hover:text-text active:scale-[0.94]",
    "disabled:pointer-events-none disabled:opacity-30"
  );

  return (
    <div className="flex items-center justify-between border-t border-line px-5 py-3">
      <span className="data-num text-[12px] text-text-faint">
        {total === 0 ? "0" : `${first}–${last}`} of {total}
      </span>
      <div className="flex items-center gap-2">
        <button
          onClick={onPrev}
          disabled={page <= 1}
          className={buttonClass}
          aria-label="Previous page"
        >
          <ChevronLeft className="h-4 w-4" />
        </button>
        <span className="data-num text-[12px] text-text-faint">
          {page} / {pageCount}
        </span>
        <button
          onClick={onNext}
          disabled={page >= pageCount}
          className={buttonClass}
          aria-label="Next page"
        >
          <ChevronRight className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
