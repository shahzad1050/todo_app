# Neon Database Configuration for Todo App

## Overview
Your Todo application is now configured to use Neon PostgreSQL database. This document explains how to work with the database configuration.

## Environment Variables
The database connection is configured in `.env` file:

```env
DATABASE_URL=postgresql://neondb_owner:npg_5TUg6znQOicv@ep-gentle-grass-ahi8ua70-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

## Database Models
The application uses SQLModel with the following models:
- `User` - for user accounts
- `Task` - for todo tasks
- `Session` - for session management

## Connection Settings
The database connection is optimized for Neon with:
- SSL mode enabled for secure connections
- Connection pooling configured for serverless environments
- Timeout settings appropriate for Neon's connection handling
- Application name set to "todo-app" for monitoring

## Running the Application
To run your application with the Neon database:

```bash
cd backend
uvicorn main:app --reload
```

## Troubleshooting
If you encounter connection issues:
1. Verify your `.env` file contains the correct DATABASE_URL
2. Check that your Neon database is running
3. Confirm your network allows outbound connections to Neon
4. Make sure you haven't exceeded your Neon database limits

## Testing the Connection
You can verify the database connection by checking the application logs for:
```
INFO:__main__:Successfully connected to database!
INFO:__main__:Database tables created successfully!
```