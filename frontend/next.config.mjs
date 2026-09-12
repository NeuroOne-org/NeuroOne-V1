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
  images: {
    remotePatterns: [{ protocol: "http", hostname: "localhost" }],
  },
};

export default nextConfig;
