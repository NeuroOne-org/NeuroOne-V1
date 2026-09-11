import { fileURLToPath } from "node:url";

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Reuse the existing frontend API client and validation without copying them.
  experimental: { externalDir: true },
  webpack(config) {
    // Shared source files live outside this preview's node_modules ancestry.
    config.resolve.modules.push(fileURLToPath(new URL('./node_modules', import.meta.url)));
    return config;
  },
};

export default nextConfig;
