"""
SQLAlchemy database models and connection setup
"""

from sqlalchemy import create_engine, Column, String, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
import enum
import uuid

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://competeintel:dev_password_change_in_prod@localhost:5432/competitor_intel"
)

# Create engine
engine = create_engine(DATABASE_URL, echo=True if os.getenv("ENVIRONMENT") == "development" else False)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class DemoRequestStatus(str, enum.Enum):
    """Status of a demo request"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DemoRequest(Base):
    """Demo request model - stores requests from landing page"""
    __tablename__ = "demo_requests"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=True)
    category = Column(String, nullable=False)
    status = Column(SQLEnum(DemoRequestStatus), nullable=False, default=DemoRequestStatus.PENDING)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    analysis_results = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)

    def __repr__(self):
        return f"<DemoRequest(id={self.id}, business_name={self.business_name}, email={self.email}, status={self.status})>"


# Database dependency for FastAPI
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize database tables
def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
