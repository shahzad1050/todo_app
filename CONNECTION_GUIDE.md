# Frontend-Backend Connection Guide

This document explains how the Next.js frontend connects to the FastAPI backend in the TaskMaster application.

## Architecture Overview

- **Frontend**: Next.js 14 application running on http://localhost:3000
- **Backend**: FastAPI application running on http://localhost:8000
- **Communication**: REST API with JWT-based authentication

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Authenticate user and get JWT token
- `POST /api/auth/logout` - Logout user (client-side token removal)

### Task Management Endpoints
- `GET /api/users/{user_id}/tasks` - Get all tasks for a user
- `POST /api/users/{user_id}/tasks` - Create a new task
- `GET /api/users/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/users/{user_id}/tasks/{task_id}` - Update a task
- `PATCH /api/users/{user_id}/tasks/{task_id}/complete` - Toggle task completion
- `DELETE /api/users/{user_id}/tasks/{task_id}` - Delete a task

## Authentication Flow

1. User registers/signs in through the frontend
2. Backend returns JWT token upon successful authentication
3. Frontend stores the token in localStorage
4. Frontend includes the token in Authorization header for protected API calls
5. Backend validates the token on each request to protected endpoints

## Environment Configuration

### Frontend Configuration
Create `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend Configuration
Create `backend/.env`:
```
DATABASE_URL=sqlite:///./todo_app.db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running the Application

### Start Backend Server
```bash
cd backend
python -m uvicorn main:app --reload
```

### Start Frontend Server
```bash
cd frontend
npm run dev
```

## Database Configuration

The application uses SQLModel with SQLite as the default database:
- Development: SQLite database stored as `todo_app.db`
- Production: Configurable via DATABASE_URL environment variable

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- User-specific task access control
- CORS middleware for cross-origin requests
- Input validation with Pydantic models

## Error Handling

- Backend returns appropriate HTTP status codes
- Frontend handles network errors gracefully
- Authentication errors are caught and handled appropriately
- Form validation occurs on both frontend and backend