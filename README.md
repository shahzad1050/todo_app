## Todo App

A full-featured Todo application deployed on GitHub Pages.

## Live Demo

Check out the live application: [https://shahzad1050.github.io/todo_app/](https://shahzad1050.github.io/todo_app/)

## Project Structure

This Todo application consists of a frontend and a backend:

- **Frontend**: Built with Next.js, deployed statically on GitHub Pages
- **Backend**: FastAPI server providing the API endpoints

## Running the Application Locally

To run the application locally for development:

1. **Backend Server**: The backend needs to be running separately as it provides the API endpoints.
   - Navigate to the `backend` directory: `cd backend`
   - Install dependencies: `pip install -r requirements.txt`
   - Start the server: `uvicorn main:app --reload`
   - The backend will be available at `http://localhost:8000`

2. **Frontend**: The frontend connects to the backend API.
   - Navigate to the `frontend` directory: `cd frontend`
   - Install dependencies: `npm install`
   - Update the `NEXT_PUBLIC_API_URL` in `frontend/.env.local` to point to your local backend (default is `http://localhost:8000`)
   - Start the development server: `npm run dev`
   - The frontend will be available at `http://localhost:3000`

## GitHub Pages Deployment

This application is configured for automatic deployment to GitHub Pages. When changes are pushed to the main branch, GitHub Actions will:
1. Build the Next.js application
2. Export it as static files
3. Deploy to GitHub Pages at [https://shahzad1050.github.io/todo_app/](https://shahzad1050.github.io/todo_app/)

The deployment workflow is defined in `.github/workflows/github-pages.yml`.
