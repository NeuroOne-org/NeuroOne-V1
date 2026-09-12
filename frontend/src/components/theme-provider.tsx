"use client";

import { ThemeProvider as NextThemeProvider } from "next-themes";

/**
 * Theme root.
 *
 * Dark is the default and the product's signature; light exists because a
 * clinic workstation in a bright room is a real place this gets used.
 *
 * `disableTransitionOnChange` matters here: without it, every element with a
 * colour transition animates at once on toggle and the whole page smears for
 * 150ms. The swap should be instantaneous — only the button animates.
 */
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  return (
    <NextThemeProvider
      attribute="class"
      defaultTheme="dark"
      enableSystem={false}
      disableTransitionOnChange
    >
      {children}
    </NextThemeProvider>
  );
}
