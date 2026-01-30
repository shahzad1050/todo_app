/** @type {import('next').NextConfig} */
const nextConfig = {
  // Removed static export to support API rewrites
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
};

module.exports = nextConfig;
