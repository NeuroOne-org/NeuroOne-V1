import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Log in — NeuroOne",
  description: "Sign in to NeuroOne, clinical decision support for neurological case evaluation.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
