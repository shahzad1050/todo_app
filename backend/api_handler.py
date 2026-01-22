# Standalone API handler for local development without Vercel/Mangum
import logging
from main import app  # Import the FastAPI app from main.py

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("API Handler initialized for local development")