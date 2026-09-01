"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity, LayoutGrid, LogOut, UploadCloud, User } from "lucide-react";
import { useAuth } from "@/components/auth-provider";
import { cn } from "@/lib/utils";
const NAV_ITEMS = [
  { href: "/dashboard", label: "Patients", icon: LayoutGrid },
  { href: "/dashboard/upload", label: "New scan", icon: UploadCloud },
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
                className={cn(
                  "flex items-center gap-2.5 rounded px-3 py-2 text-[13px] transition-colors",
                  active
                    ? "bg-raised text-text"
                    : "text-text-muted hover:bg-raised hover:text-text"
                )}
              >
                <Icon className="h-4 w-4" />
                {item.label}
              </Link>
            );
          })}
        </nav>
        <div className="border-t border-line px-3 py-3">
          <div className="flex items-center gap-2.5 rounded px-3 py-2 text-[13px] text-text-muted">
            <User className="h-4 w-4" />
            <div className="min-w-0 flex-1">
              <p className="truncate text-text">{displayName}</p>
              <p className="truncate text-[11px] text-text-faint">
                {user?.role ?? ""}
              </p>
            </div>
          </div>
          <button
            onClick={logout}
            className="mt-1 flex w-full items-center gap-2.5 rounded px-3 py-2 text-[13px] text-text-muted transition-colors hover:bg-raised hover:text-amber"
          >
            <LogOut className="h-4 w-4" />
            Sign out
          </button>
        </div>
      </aside>
      <main className="flex-1 overflow-y-auto px-8 py-8">{children}</main>
    </div>
  );
}