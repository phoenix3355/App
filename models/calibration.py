"""
Calibration Model
Represents calibration records for instruments.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from models import Base

class CalibrationStatus(enum.Enum):
    """Calibration status enumeration."""
    PASSED = "passed"
    FAILED = "failed"
    PENDING = "pending"

class Calibration(Base):
    """Calibration model for tracking instrument calibrations."""
    
    __tablename__ = 'calibrations'
    
    id = Column(Integer, primary_key=True, index=True)
    instrument_id = Column(Integer, ForeignKey('instruments.id'), nullable=False, index=True)
    calibration_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    next_calibration_date = Column(DateTime)
    performed_by = Column(String(100))
    status = Column(SQLEnum(CalibrationStatus), nullable=False, default=CalibrationStatus.PENDING)
    certificate_number = Column(String(100), unique=True)
    standard_used = Column(String(200))
    temperature = Column(Float)
    humidity = Column(Float)
    notes = Column(String(1000))
    results = Column(String(2000))  # JSON string for detailed results
    is_due = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    instrument = relationship("Instrument", back_populates="calibrations")
    
    def __repr__(self):
        return f"<Calibration(id={self.id}, instrument_id={self.instrument_id}, date='{self.calibration_date}')>"
    
    @property
    def is_overdue(self):
        """Check if calibration is overdue."""
        if self.next_calibration_date:
            return datetime.utcnow() > self.next_calibration_date
        return False
