import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv is optional
    pass

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application lifespan started")
    yield
    logger.info("Application lifespan ended")

# Create FastAPI app
try:
    app = FastAPI(
        title="AI-Powered Todo Chatbot API - Temporary",
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

@app.get("/")
def read_root():
    return {"message": "AI-Powered Todo Chatbot API - Temporary Version"}

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


@app.post("/chat/{user_id}")
async def chat_endpoint(user_id: str, message: str = Form(...)):
    """Chat endpoint that processes natural language and returns AI response"""
    try:
        # Import the AIAgent only when needed to avoid model loading issues
        from services.ai_agent import AIAgent

        # Initialize AI agent
        ai_agent = AIAgent()
        result = ai_agent.process_message(user_id, message)
        return {
            "conversation_id": "temp_conversation_id",
            "response": result["response"],
            "tool_calls": result["tool_calls"],
            "timestamp": "2026-01-29T18:30:00Z"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred processing your request: {str(e)}"
        )