## Running the Application Locally

This Todo application consists of a frontend and a backend. For full functionality:

1. **Backend Server**: The backend needs to be running separately as it provides the API endpoints.
   - Navigate to the `backend` directory: `cd backend`
   - Install dependencies: `pip install -r requirements.txt`
   - Start the server: `uvicorn main:app --reload`
   - The backend will be available at `http://localhost:8000`

2. **Frontend**: The frontend connects to the backend API.
   - Navigate to the `frontend` directory: `cd frontend`
   - Install dependencies: `npm install`
   - Start the development server: `npm run dev`
   - The frontend will be available at `http://localhost:3000`

## Configuration

To connect the frontend to your backend server, ensure the `NEXT_PUBLIC_API_URL` environment variable in `frontend/.env.local` points to your backend server URL (default is `http://localhost:8000`).
