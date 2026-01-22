import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import modules with error handling
try:
    from database import create_db_and_tables
    logger.info("Successfully imported database module")
except ImportError as e:
    logger.error(f"Error importing database module: {e}")
    # Define a placeholder function
    def create_db_and_tables():
        logger.warning("Database module not available, using placeholder")

try:
    from api import tasks
    logger.info("Successfully imported tasks API module")
except ImportError as e:
    logger.error(f"Error importing tasks API module: {e}")
    # Define a placeholder module
    class tasks:
        router = None

try:
    from auth import auth_router
    logger.info("Successfully imported auth module")
except ImportError as e:
    logger.error(f"Error importing auth module: {e}")
    # Define a placeholder router
    from fastapi import APIRouter
    auth_router = APIRouter()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database and create tables
    logger.info("Application lifespan started")
    try:
        # Create database tables for all registered models
        from sqlmodel import SQLModel
        from database import engine
        SQLModel.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
    yield
    logger.info("Application lifespan ended")

# Create FastAPI app
try:
    app = FastAPI(
        title="Todo Web Application API",
        description="RESTful API for the Todo Web Application with user authentication and task management",
        version="1.0.0",
        lifespan=lifespan
    )
    logger.info("FastAPI app created successfully")
except Exception as e:
    logger.error(f"Error creating FastAPI app: {e}")
    raise

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers only if they exist
if tasks.router:
    app.include_router(tasks.router, prefix="/api")
    logger.info("Tasks router included")
else:
    logger.warning("Tasks router not available")

if auth_router:
    app.include_router(auth_router, prefix="/api/auth")
    logger.info("Auth router included")
else:
    logger.warning("Auth router not available")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Web Application API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    try:
        from fastapi.responses import Response
        import base64
        # Return a minimal transparent favicon to avoid 404 errors
        transparent_favicon = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAA"
            "B3RJTUUH5AgQDC421wKJLgAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBk"
            "LmUHAAAAFklEQVQ4y2P8//8/AzYwMjIyAAAc/Qv/rkZB4QAAAABJRU5ErkJggg=="
        )
        return Response(content=transparent_favicon, media_type="image/x-icon")
    except Exception as e:
        logger.error(f"Error serving favicon: {e}")
        # Return an empty transparent favicon as fallback
        # Base64 encoded 16x16 transparent PNG
        empty_favicon = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAALUlEQVR42mNkYPhf"
            "zMDAwMCg8J+BgeE/AwMDQ8D////9GQQYGBgYGBgYGP4zAADDTg1BLsyudgAAAABJRU5ErkJggg=="
        )
        return Response(content=empty_favicon, media_type="image/x-icon")