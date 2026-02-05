# Neon Database Setup Guide

## Overview
This document explains how to set up a Neon database for the AI Todo Chatbot application.

## Step-by-Step Setup

### 1. Create a Neon Account
- Go to [Neon](https://neon.tech)
- Sign up for a free account or sign in if you already have one

### 2. Create a New Project
- After logging in, click on "New Project"
- Choose your region closest to your users
- Select the "Free Tier" plan (or a paid tier if preferred)
- Give your project a name (e.g., "ai-todo-chatbot")
- Click "Create Project"

### 3. Access Database Credentials
Once your project is created, you'll see:
- **Connection String**: Format: `postgresql://username:password@ep-xxxxxxx.us-east-1.aws.neon.tech/neondb?sslmode=require`
- **Host**: The endpoint hostname
- **Database**: Usually "neondb"
- **Username**: Your database username
- **Password**: Your database password

### 4. Get Connection Details
1. Go to your Neon project dashboard
2. Click on "Connection Details" or "Settings"
3. Copy the connection string in the format:
   ```
   postgresql://username:password@hostname/database?sslmode=require
   ```

### 5. Configure Environment Variables
Use the connection string as your `DATABASE_URL` environment variable:

```
DATABASE_URL=postgresql://username:password@ep-xxxxxxx.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### 6. Verify Connection
You can test the connection using the Neon SQL Editor in the dashboard or by connecting through your application.

### 7. Database Schema
The application uses SQLModel which will automatically create the necessary tables:
- `users` table for user accounts
- `tasks` table for todo items
- `conversations` table for chat history
- `messages` table for individual messages

## Security Considerations
- Keep your connection string secure and never commit it to version control
- Rotate your database password periodically
- Monitor connection logs in the Neon dashboard
- Use Neon's branch feature for development and testing environments

## Connection Pooling
- Neon supports connection pooling which helps with performance
- The application uses connection pooling through the SQLAlchemy engine

## Backup and Recovery
- Neon automatically creates backups of your database
- You can restore to a specific point in time if needed
- Check the "Branches" section for backup options

## Monitoring
- Use the Neon dashboard to monitor database performance
- Check query performance and connection metrics
- Set up alerts if needed

## Troubleshooting
- If you get connection errors, verify your connection string format
- Check that SSL is enabled (required for Neon)
- Ensure your application has internet access to reach Neon's servers
- Verify that your Neon project is active and not paused