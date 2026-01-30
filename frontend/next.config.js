/** @type {import('next').NextConfig} */
const nextConfig = {
  // Removed static export to support API rewrites
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
  env: {
    BACKEND_API_URL: process.env.BACKEND_API_URL || 'http://127.0.0.1:8001',
  },
};

module.exports = nextConfig;
