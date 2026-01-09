from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_db_and_tables
from api import tasks
from auth import auth_router
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database and create tables
    create_db_and_tables()
    yield

# Create FastAPI app
app = FastAPI(
    title="Todo Web Application API",
    description="RESTful API for the Todo Web Application with user authentication and task management",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(tasks.router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Web Application API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    from fastapi.responses import Response
    import base64
    # Return a minimal transparent favicon to avoid 404 errors
    transparent_favicon = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAA"
        "B3RJTUUH5AgQDC421wKJLgAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBk"
        "LmUHAAAAFklEQVQ4y2P8//8/AzYwMjIyAAAc/Qv/rkZB4QAAAABJRU5ErkJggg=="
    )
    return Response(content=transparent_favicon, media_type="image/x-icon")