const express = require('express');
const cors = require('cors');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;
const BACKEND_PORT = 8001;

// Enable CORS for all routes
app.use(cors());

// Serve static files from the current directory
app.use(express.static('.'));

// Proxy API requests to the backend
app.use('/api', createProxyMiddleware({
  target: `http://127.0.0.1:${BACKEND_PORT}`,
  changeOrigin: true
  // No pathRewrite - forward paths as-is
}));

// Serve the frontend
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend.html'));
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'frontend is running', backend: `http://127.0.0.1:${BACKEND_PORT}` });
});

app.listen(PORT, '127.0.0.1', () => {
  console.log(`Frontend server running at http://127.0.0.1:${PORT}`);
  console.log(`Proxying API requests to http://127.0.0.1:${BACKEND_PORT}`);
  console.log('Open your browser and go to http://127.0.0.1:3000 to use the AI Todo Chatbot');
});