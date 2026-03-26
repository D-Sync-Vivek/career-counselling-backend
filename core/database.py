import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

# 1. Fetch the Database URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("CRITICAL: DATABASE_URL is missing in .env file.")

# 2. Clean the URL for SQLAlchemy
# SQLAlchemy prefers 'postgresql://' or 'postgresql+psycopg2://'
clean_db_url = DATABASE_URL.replace("postgres://", "postgresql://")
if clean_db_url.startswith("postgresql://"):
    clean_db_url = clean_db_url.replace("postgresql://", "postgresql+psycopg2://")

# 3. Create the Connection Pool Engine
# This is the most important part for a Serverless DB like Neon
engine = create_engine(
    clean_db_url,
    pool_pre_ping=True,  # Actively tests connections before using them to prevent crashes
    pool_size=10,        # Keeps 10 connections permanently open and ready
    max_overflow=20      # Allows up to 20 extra connections during traffic spikes
)

# 4. Create the Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Create the Base Model Class
Base = declarative_base()

# 6. Dependency Injection for FastAPI
def get_db():
    """
    FastAPI dependency that creates a new database session for each request
    and securely closes it when the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()