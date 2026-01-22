/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable static export for GitHub Pages deployment
  output: 'export',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
  // Disable experimental features not compatible with static export
  experimental: {
    // Remove server components external packages for static export
  },
};

module.exports = nextConfig;
