from sqlmodel import create_engine, Session, SQLModel
from .models import User, Task  # Import models to register them with SQLModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_LDwYj29VvHhq@ep-winter-bread-a44joluf-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require")

# For serverless environments, use connection parameters suitable for serverless
try:
    if DATABASE_URL.startswith("postgres"):
        # PostgreSQL connection for production with serverless-friendly settings
        engine = create_engine(
            DATABASE_URL,
            echo=bool(os.getenv("DEBUG", False)),
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=1,  # Minimal pool size for serverless
            max_overflow=2,  # Minimal overflow for serverless
            connect_args={
                "connect_timeout": 15,
                "command_timeout": 15,
            }
        )
    else:
        # Fallback to SQLite for local development
        engine = create_engine(
            DATABASE_URL,
            echo=bool(os.getenv("DEBUG", False)),
        )
except Exception as e:
    print(f"Database connection error: {e}")
    # Fallback to in-memory database to prevent complete failure
    from sqlalchemy import create_engine as sqlalchemy_create_engine
    engine = sqlalchemy_create_engine("sqlite:///:memory:")

def create_db_and_tables():
    """Create database tables for all models"""
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"Error creating database tables: {e}")
        # Don't raise here to allow the app to start even if table creation fails

def get_session():
    """Get a database session"""
    # Attempt to create tables when session is requested
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"Warning: Could not create tables: {e}")

    with Session(engine) as session:
        yield session