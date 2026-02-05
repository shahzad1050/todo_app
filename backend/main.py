import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path for imports
backend_dir = Path(__file__).parent.absolute()
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import modules with error handling
try:
    from core.database import engine
    logger.info("Successfully imported database module")
except ImportError as e:
    logger.error(f"Error importing database module: {e}")
    # Define a placeholder variable
    engine = None

# Import modules with error handling
try:
    from core.database import engine
    logger.info("Successfully imported database module")
except ImportError as e:
    logger.error(f"Error importing database module: {e}")
    # Define a placeholder variable
    engine = None

# Try to import API routers with proper error handling
# Temporarily disabling chat functionality to resolve model import issues
try:
    from api.chat import router as chat_router
    logger.info("Successfully imported chat API module")
except ImportError as e:
    logger.error(f"Error importing chat API module: {e}")
    from fastapi import APIRouter
    chat_router = APIRouter()

try:
    from api.auth import router as auth_router
    logger.info("Successfully imported auth module")
except ImportError as e:
    logger.error(f"Error importing auth module: {e}")
    from fastapi import APIRouter
    auth_router = APIRouter()

# Try to import tasks router
try:
    from api.tasks import router as tasks_router
    logger.info("Successfully imported tasks API module")
except ImportError as e:
    logger.error(f"Error importing tasks API module: {e}")
    from fastapi import APIRouter
    tasks_router = APIRouter()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database and create tables
    logger.info("Application lifespan started")
    try:
        if engine:
            # Create database tables for all registered models
            from sqlmodel import SQLModel
            SQLModel.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
        else:
            logger.warning("Database engine not available, skipping table creation")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
    yield
    logger.info("Application lifespan ended")

# Create FastAPI app
try:
    app = FastAPI(
        title="AI-Powered Todo Chatbot API",
        description="AI-powered Todo chatbot API that allows users to manage tasks using natural language",
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

# Include API routers
app.include_router(chat_router, prefix="/api", tags=["chat"])  # Re-enabled chat functionality
app.include_router(tasks_router, prefix="/api", tags=["tasks"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "AI-Powered Todo Chatbot API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "AI-powered Todo Chatbot API is running"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    try:
        from fastapi.responses import Response
        import base64
        # Return a minimal transparent favicon to avoid 404 errors
        transparent_favicon = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAA"
            "B3RJTUUH5AgQDC421wKJLgAAAB1pVFh0Q290bWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBk"
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