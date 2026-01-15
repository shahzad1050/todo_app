from sqlmodel import create_engine, Session, SQLModel
from .models import User, Task  # Import models to register them with SQLModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment - Vercel recommends using PostgreSQL for production
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_LDwYj29VvHhq@ep-winter-bread-a44joluf-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

# For serverless environments, use connection parameters suitable for serverless
if DATABASE_URL.startswith("postgres"):
    # PostgreSQL connection for production
    engine = create_engine(
        DATABASE_URL,
        echo=bool(os.getenv("DEBUG", False)),
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=5,
        max_overflow=10,
        # For serverless, we want shorter-lived connections
        connect_args={
            "connect_timeout": 10,
        }
    )
else:
    # Fallback to SQLite for local development
    engine = create_engine(
        DATABASE_URL,
        echo=bool(os.getenv("DEBUG", False)),
        # For SQLite in serverless, we shouldn't use connection pooling
        # but this is just for local testing
    )

def create_db_and_tables():
    """Create database tables for all models"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get a database session"""
    with Session(engine) as session:
        yield session