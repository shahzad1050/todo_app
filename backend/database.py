import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

from sqlmodel import create_engine, Session, SQLModel

# Import models to register them with SQLModel, but handle import errors
try:
    from models import User, Task
    logger.info("Successfully imported User and Task models")
except ImportError as e:
    logger.warning(f"Could not import User and Task models: {e}")
    # Define placeholder classes if models can't be imported
    class User:
        pass
    class Task:
        pass

# Get database URL from environment
# Don't load .env in serverless environments as it's not needed
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Fallback for development only
    DATABASE_URL = "sqlite:///./test.db"  # Use SQLite for local testing

# For serverless environments, use connection parameters suitable for serverless
try:
    if DATABASE_URL and DATABASE_URL.startswith("postgres"):
        # PostgreSQL connection for production with serverless-friendly settings
        # Updated for Neon database compatibility
        engine = create_engine(
            DATABASE_URL,
            echo=bool(os.getenv("DEBUG", False)),
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=1,  # Minimal pool size for serverless
            max_overflow=2,  # Minimal overflow for serverless
            connect_args={
                "connect_timeout": 15,
                "application_name": "todo-app",  # For Neon connection monitoring
            }
        )
        logger.info("Initialized PostgreSQL engine for Neon")
    elif DATABASE_URL and DATABASE_URL.startswith("sqlite"):
        # SQLite for local development
        engine = create_engine(
            DATABASE_URL,
            echo=bool(os.getenv("DEBUG", False)),
        )
        logger.info("Initialized SQLite engine")
    else:
        # Fallback to in-memory database if no DATABASE_URL is provided
        from sqlalchemy import create_engine as sqlalchemy_create_engine
        engine = sqlalchemy_create_engine("sqlite:///:memory:")
        logger.warning("Using in-memory database as fallback")

    # Test the engine by attempting to connect
    try:
        with engine.connect() as conn:
            logger.info("Database connection successful")
    except Exception as conn_e:
        logger.warning(f"Database connection test failed: {conn_e}")

except Exception as e:
    logger.error(f"Database connection error: {e}")
    # Fallback to in-memory database to prevent complete failure
    from sqlalchemy import create_engine as sqlalchemy_create_engine
    engine = sqlalchemy_create_engine("sqlite:///:memory:")
    logger.warning("Using in-memory database due to connection error")

def create_db_and_tables():
    """Create database tables for all models"""
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        # Don't raise here to allow the app to start even if table creation fails

def get_session():
    """Get a database session"""
    # Attempt to create tables when session is requested
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        logger.warning(f"Could not create tables: {e}")

    with Session(engine) as session:
        yield session