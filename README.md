## Deployment

[View the deployment on GitHub Pages](https://shahzad1050.github.io/Todo/)

⚠️ **Important**: The GitHub Pages deployment is static and requires a running backend server to function fully. See "Backend Deployment" below.

## Running the Application Locally

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

## Backend Deployment

For the GitHub Pages frontend to work properly, you need to deploy the backend server to a public hosting service. Here's how to deploy to popular platforms:

### Deploy to Render
1. Create a new Web Service on [Render](https://render.com)
2. Connect to your GitHub repository
3. Set the runtime to Python
4. Set the build command: `pip install -r requirements.txt`
5. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add your database URL as an environment variable

### Deploy to Railway
1. Create a new project on [Railway](https://railway.app)
2. Connect to your GitHub repository
3. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

After deploying your backend, update the `NEXT_PUBLIC_API_URL` in your frontend environment files to point to your deployed backend URL.

## Configuration

To connect the frontend to your backend server, set the `NEXT_PUBLIC_API_URL` environment variable to point to your backend server URL.

For GitHub Pages deployment, the backend must be accessible via a public URL, and CORS must be configured to allow requests from the GitHub Pages domain (https://shahzad1050.github.io).
