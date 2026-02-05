# AI Todo Chatbot - Vercel + Neon Deployment Guide

This guide explains how to deploy the AI Todo Chatbot application to Vercel with Neon database.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Neon Account**: Sign up at [neon.tech](https://neon.tech)
3. **GitHub Account**: For repository hosting

## Setup Instructions

### 1. Neon Database Setup

1. Log into your [Neon Console](https://console.neon.tech)
2. Create a new project
3. After project creation, go to the "Connection Details" section
4. Copy the connection string in the format: `postgresql://username:password@endpoint/project_name`
5. Take note of the connection details:
   - Database URL
   - Username
   - Password
   - Host
   - Database name

### 2. Environment Variables

Add these environment variables to your Vercel project:

#### Backend Environment Variables:
- `NEON_DATABASE_URL`: Your Neon database connection string
- `SECRET_KEY`: A strong secret key for JWT tokens (generate a random one)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins (e.g., `https://your-frontend.vercel.app,http://localhost:3000`)

#### Frontend Environment Variables:
- `NEXT_PUBLIC_API_URL`: Your deployed backend URL (e.g., `https://your-backend.vercel.app`)

### 3. Deploy Backend to Vercel

1. Push your backend code to a GitHub repository
2. Go to [vercel.com](https://vercel.com) and connect your GitHub account
3. Click "New Project" and select your backend repository
4. Configure the project:
   - Framework Preset: `None` or `Python`
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `api_handler.py` is the entry point
5. Add the environment variables in the Vercel dashboard
6. Deploy

### 4. Deploy Frontend to Vercel

1. Push your frontend code to a GitHub repository
2. Go to [vercel.com](https://vercel.com) and connect your GitHub account
3. Click "New Project" and select your frontend repository
4. The project should auto-detect as a Next.js app
5. Add the `NEXT_PUBLIC_API_URL` environment variable
6. Deploy

## Architecture

- **Frontend**: Next.js application hosted on Vercel
- **Backend**: FastAPI application with Neon PostgreSQL database
- **Authentication**: JWT-based authentication
- **API Gateway**: Vercel Functions handle API requests

## Environment Configuration

### Backend (api_handler.py)
- Uses `DATABASE_URL` for database connection
- Uses `SECRET_KEY` for JWT signing
- Uses `ALLOWED_ORIGINS` for CORS configuration

### Frontend
- Uses `NEXT_PUBLIC_API_URL` to connect to backend API

## Deployment Commands

### For local development:
```bash
# Start backend
cd backend
python -c "from api_handler import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8005)"

# Start frontend
cd frontend
npm run dev
```

## Troubleshooting

1. **Database Connection Issues**: Verify your Neon database connection string is correct and the environment variable is properly set
2. **CORS Issues**: Make sure the `ALLOWED_ORIGINS` includes your frontend URL
3. **Authentication Issues**: Verify that the `SECRET_KEY` is consistent between deployments
4. **API Connection Issues**: Check that the frontend is pointing to the correct backend URL

## Scaling Considerations

- Neon's serverless database automatically scales with demand
- Vercel automatically scales your API functions based on traffic
- For high-traffic applications, consider upgrading your Neon database plan

## Security Best Practices

- Never expose database credentials in client-side code
- Use strong, randomly generated secret keys
- Implement proper rate limiting for API endpoints
- Regularly rotate database passwords and secret keys