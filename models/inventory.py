"""
Inventory Model
Represents inventory tracking for instruments.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from models import Base

class InventoryStatus(enum.Enum):
    """Inventory status enumeration."""
    IN_STOCK = "in_stock"
    IN_USE = "in_use"
    CHECKED_OUT = "checked_out"
    MAINTENANCE = "maintenance"
    LOST = "lost"

class Inventory(Base):
    """Inventory model for tracking instrument location and status."""
    
    __tablename__ = 'inventory'
    
    id = Column(Integer, primary_key=True, index=True)
    instrument_id = Column(Integer, ForeignKey('instruments.id'), nullable=False, index=True)
    status = Column(SQLEnum(InventoryStatus), nullable=False, default=InventoryStatus.IN_STOCK)
    location = Column(String(200))
    assigned_to = Column(String(100))
    checkout_date = Column(DateTime)
    return_date = Column(DateTime)
    quantity = Column(Integer, default=1)
    notes = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    instrument = relationship("Instrument", back_populates="inventory_items")
    
    def __repr__(self):
        return f"<Inventory(id={self.id}, instrument_id={self.instrument_id}, status='{self.status.value}')>"
    
    @property
    def is_available(self):
        """Check if instrument is available."""
        return self.status == InventoryStatus.IN_STOCK
