/** @type {import('next').NextConfig} */
const nextConfig = {
  // A `next build` writes over the `.next` a running `next dev` is serving
  // from, which leaves the dev server handing out 404s for its own CSS until
  // it is restarted. Setting NEXT_DIST_DIR lets a second server (a build, or
  // a throwaway dev instance) use its own directory instead. Defaults to the
  // usual `.next`, so nothing changes unless the variable is set.
  distDir: process.env.NEXT_DIST_DIR || ".next",
  reactStrictMode: true,
  output: "standalone",
  // Serves the API from the page's own origin, so a single public tunnel
  // (cloudflared on port 3000) carries both and the SameSite=Strict session
  // cookie still applies. Used only when NEXT_PUBLIC_API_URL=/api/v1.
  async rewrites() {
    const target = process.env.API_PROXY_TARGET || "http://localhost:8000";
    return [{ source: "/api/v1/:path*", destination: `${target}/api/v1/:path*` }];
  },
  images: {
    remotePatterns: [{ protocol: "http", hostname: "localhost" }],
  },
};

export default nextConfig;
