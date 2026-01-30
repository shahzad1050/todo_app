from sqlmodel import create_engine
import os
from urllib.parse import urlparse

# Get database URL from environment, with Neon as default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_5TUg6znQOicv@ep-gentle-grass-ahi8ua70-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

# For Neon/PostgreSQL, we may need to handle special URL parsing
if DATABASE_URL.startswith("postgres://"):
    # Replace postgres:// with postgresql:// for compatibility
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=True)