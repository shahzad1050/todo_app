/** @type {import('next').NextConfig} */
const nextConfig = {
  // Removed static export to support API rewrites
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:8000/api/:path*',  // Forward /api/* to backend's /api/*
      },
    ]
  },
};

module.exports = nextConfig;

module.exports = nextConfig;
