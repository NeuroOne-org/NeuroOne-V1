"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Activity,
  DoorOpen,
  LayoutDashboard,
  Plus,
  Users,
} from "@/components/icons";
import SwitchButton from "@/components/ui/switch-button";
import { useAuth } from "@/components/auth-provider";
import { cn, initials } from "@/lib/utils";

const NAV_ITEMS = [
  { href: "/dashboard", label: "Queue", icon: LayoutDashboard },
  { href: "/dashboard/patients", label: "Patients", icon: Users },
  { href: "/dashboard/upload", label: "New intake", icon: Plus },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const displayName = user ? `${user.first_name} ${user.last_name}`.trim() : "—";

  return (
    <div className="flex min-h-screen bg-ink">
      <aside className="flex w-60 shrink-0 flex-col border-r border-line bg-panel">
        <div className="flex items-center gap-2 px-5 py-5 font-display text-base font-semibold">
          <Activity className="h-5 w-5 text-teal" />
          NeuroOne
        </div>

        <nav className="flex-1 space-y-1 px-3">
          {NAV_ITEMS.map((item) => {
            const active =
              item.href === "/dashboard"
                ? pathname === "/dashboard"
                : pathname.startsWith(item.href);
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                aria-current={active ? "page" : undefined}
                className={cn(
                  "flex items-center gap-2.5 rounded px-3 py-2 text-[13px]",
                  "transition-[background-color,color,transform] duration-150 ease-out active:scale-[0.98]",
                  active
                    ? "bg-raised text-text"
                    : "text-text-muted hover:bg-raised hover:text-text"
                )}
              >
                <Icon className={cn("h-4 w-4", active && "text-teal")} />
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="border-t border-line px-3 py-3">
          <div className="mb-2 px-0.5">
            <SwitchButton size="sm" />
          </div>

          <div className="flex items-center gap-2.5 rounded px-3 py-2 text-[13px]">
            <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full border border-line bg-raised font-mono text-[11px] text-text-muted">
              {user ? initials(displayName) : "—"}
            </span>
            <div className="min-w-0 flex-1">
              <p className="truncate text-text">{displayName}</p>
              <p className="truncate text-[11px] capitalize text-text-faint">
                {user?.role ?? ""}
              </p>
            </div>
          </div>
          <button
            onClick={logout}
            className={cn(
              "mt-1 flex w-full items-center gap-2.5 rounded px-3 py-2 text-[13px] text-text-muted",
              "transition-[background-color,color,transform] duration-150 ease-out",
              "hover:bg-raised hover:text-amber active:scale-[0.98]"
            )}
          >
            <DoorOpen className="h-4 w-4" />
            Sign out
          </button>
        </div>
      </aside>

      <main className="flex-1 overflow-y-auto px-8 py-8">{children}</main>
    </div>
  );
}
