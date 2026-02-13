"""
Instrument Model
Represents instruments/gauges that need to be calibrated.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from models import Base

class InstrumentStatus(enum.Enum):
    """Instrument status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    RETIRED = "retired"
    MAINTENANCE = "maintenance"

class InstrumentType(enum.Enum):
    """Instrument type enumeration."""
    GAUGE = "gauge"
    SENSOR = "sensor"
    METER = "meter"
    ANALYZER = "analyzer"
    OTHER = "other"

class Instrument(Base):
    """Instrument model for managing gauges and measuring devices."""
    
    __tablename__ = 'instruments'
    
    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    type = Column(SQLEnum(InstrumentType), nullable=False, default=InstrumentType.GAUGE)
    manufacturer = Column(String(100))
    model = Column(String(100))
    description = Column(String(500))
    location = Column(String(200))
    status = Column(SQLEnum(InstrumentStatus), nullable=False, default=InstrumentStatus.ACTIVE)
    accuracy = Column(Float)
    range_min = Column(Float)
    range_max = Column(Float)
    unit = Column(String(20))
    purchase_date = Column(DateTime)
    purchase_cost = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    calibrations = relationship("Calibration", back_populates="instrument", cascade="all, delete-orphan")
    inventory_items = relationship("Inventory", back_populates="instrument", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Instrument(id={self.id}, serial='{self.serial_number}', name='{self.name}')>"
    
    @property
    def display_name(self):
        """Get display name for the instrument."""
        return f"{self.name} ({self.serial_number})"
