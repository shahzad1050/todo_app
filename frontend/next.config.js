/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // Enables static exports for GitHub Pages
  images: {
    unoptimized: true,
  },
};

module.exports = nextConfig;
