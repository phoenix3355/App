"""
Database Module
SQLAlchemy database setup and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import config

# Create database engine
engine = create_engine(
    config.get('database.url'),
    echo=config.get('database.echo', False),
    pool_pre_ping=True,
)

# Create session factory
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# Create base class for models
Base = declarative_base()

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise

def init_db():
    """Initialize database tables."""
    # Import all models here to ensure they are registered
    from models.user import User
    from models.instrument import Instrument
    from models.calibration import Calibration
    from models.inventory import Inventory
    
    Base.metadata.create_all(bind=engine)

def close_db():
    """Close database session."""
    SessionLocal.remove()
