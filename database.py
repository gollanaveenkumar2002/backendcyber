"""
Database Configuration and Connection
Handles database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Import models
from models import Base, Admin, BlogPost

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://cogninode:19801980@98.130.114.230:3306/cyberanytime"
)

# Create database engine
engine = create_engine(
    DATABASE_URL, 
    echo=False,  # Set to True to see SQL queries in console
    pool_pre_ping=True  # Verify connections before using
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)


# Database session dependency for FastAPI
def get_db():
    """
    FastAPI dependency to get database session
    
    Usage:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            # Use db here
    
    Automatically closes the session after request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
