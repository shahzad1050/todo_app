from sqlmodel import create_engine, Session, SQLModel
from models import User, Task  # Import models to register them with SQLModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment - default to SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create the database engine with connection pooling and proper settings
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections after 5 minutes
    pool_size=10,        # Number of connection pools
    max_overflow=20      # Maximum number of connections beyond pool_size
)

def create_db_and_tables():
    """Create database tables for all models"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get a database session"""
    with Session(engine) as session:
        yield session