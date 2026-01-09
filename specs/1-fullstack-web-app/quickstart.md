# Quickstart: Full-Stack Web Application

## Prerequisites

- Node.js 18+ with npm/yarn
- Python 3.11+
- PostgreSQL (or access to Neon Serverless PostgreSQL)
- Git

## Setup Instructions

### 1. Clone and Initialize Repository

```bash
git clone <repository-url>
cd todo_webapp
```

### 2. Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database connection details
```

5. Run database migrations:
```bash
python -m alembic upgrade head
```

6. Start the backend server:
```bash
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
# or
yarn install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your backend API URL
```

4. Start the development server:
```bash
npm run dev
# or
yarn dev
```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
NEON_DATABASE_URL=your-neon-database-url
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_URL=http://localhost:8000/auth
```

## API Endpoints

Once running, the backend will be available at `http://localhost:8000` with:
- API documentation at `http://localhost:8000/docs`
- API endpoints under `/api/`
- Authentication under `/auth/`

The frontend will be available at `http://localhost:3000`.

## Development Commands

### Backend
```bash
# Run tests
python -m pytest

# Format code
black .

# Lint code
flake8
```

### Frontend
```bash
# Run tests
npm test

# Build for production
npm run build

# Run linting
npm run lint
```

## Database Setup

The application uses SQLModel with Neon Serverless PostgreSQL. After setting up your database:

1. Create the database tables:
```bash
cd backend
python -c "from database import create_db_and_tables; create_db_and_tables()"
```

2. Or use alembic migrations if available:
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Running the Application

1. Start the backend server (port 8000)
2. Start the frontend server (port 3000)
3. Access the application at `http://localhost:3000`
4. API documentation is available at `http://localhost:8000/docs`

## Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

### End-to-End Tests
```bash
cd frontend
npm run test:e2e
```