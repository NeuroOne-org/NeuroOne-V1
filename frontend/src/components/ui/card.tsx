import { cn } from "@/lib/utils";

export function Card({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return <div className={cn("panel", className)}>{children}</div>;
}

export function CardHeader({
  eyebrow,
  title,
  action,
}: {
  eyebrow?: string;
  title: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="flex items-start justify-between border-b border-line px-5 py-4">
      <div>
        {eyebrow && <p className="label-eyebrow mb-1">{eyebrow}</p>}
        <h2 className="font-display text-[15px] font-medium text-text">
          {title}
        </h2>
      </div>
      {action}
    </div>
  );
}

export function CardBody({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return <div className={cn("p-5", className)}>{children}</div>;
}
