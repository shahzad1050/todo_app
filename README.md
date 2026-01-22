## Deployment

[View the deployment on GitHub Pages](https://shahzad1050.github.io/Todo/)

## Running the Application

This Todo application consists of a frontend and a backend. For full functionality:

1. **Backend Server**: The backend needs to be running separately as it provides the API endpoints.
   - Navigate to the `backend` directory: `cd backend`
   - Install dependencies: `pip install -r requirements.txt`
   - Start the server: `uvicorn main:app --reload`
   - The backend will be available at `http://localhost:8000`

2. **Frontend**: The frontend is statically exported and served from GitHub Pages.
   - When developing locally, navigate to `frontend` directory
   - Install dependencies: `npm install`
   - Start the development server: `npm run dev`
   - The frontend will be available at `http://localhost:3000`

## Configuration

To connect the frontend to your backend server, set the `NEXT_PUBLIC_API_URL` environment variable to point to your backend server URL.

For GitHub Pages deployment, the backend must be accessible via a public URL, and CORS must be configured to allow requests from the GitHub Pages domain.
