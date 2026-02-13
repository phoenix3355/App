"""
Instrument Controller
Business logic for instrument management.
"""
from typing import Optional, List
from datetime import datetime
from models import get_db
from models.instrument import Instrument, InstrumentStatus, InstrumentType
from utils.security import security

class InstrumentController:
    """Controller for instrument management operations."""
    
    def create_instrument(self, serial_number: str, name: str, 
                         instrument_type: InstrumentType = InstrumentType.GAUGE,
                         **kwargs) -> Instrument:
        """
        Create a new instrument.
        
        Args:
            serial_number: Unique serial number
            name: Instrument name
            instrument_type: Type of instrument
            **kwargs: Additional fields
            
        Returns:
            Created Instrument object
        """
        db = get_db()
        try:
            # Check if serial number already exists
            existing = db.query(Instrument).filter(
                Instrument.serial_number == serial_number
            ).first()
            
            if existing:
                raise ValueError("Serial number already exists")
            
            # Create instrument
            instrument = Instrument(
                serial_number=security.sanitize_input(serial_number),
                name=security.sanitize_input(name),
                type=instrument_type,
                manufacturer=security.sanitize_input(kwargs.get('manufacturer', '')),
                model=security.sanitize_input(kwargs.get('model', '')),
                description=security.sanitize_input(kwargs.get('description', '')),
                location=security.sanitize_input(kwargs.get('location', '')),
                status=kwargs.get('status', InstrumentStatus.ACTIVE),
                accuracy=kwargs.get('accuracy'),
                range_min=kwargs.get('range_min'),
                range_max=kwargs.get('range_max'),
                unit=security.sanitize_input(kwargs.get('unit', '')),
                purchase_date=kwargs.get('purchase_date'),
                purchase_cost=kwargs.get('purchase_cost'),
            )
            
            db.add(instrument)
            db.commit()
            db.refresh(instrument)
            return instrument
        except ValueError:
            raise
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to create instrument: {str(e)}")
        finally:
            db.close()
    
    def get_instrument(self, instrument_id: int) -> Optional[Instrument]:
        """Get instrument by ID."""
        db = get_db()
        try:
            return db.query(Instrument).filter(Instrument.id == instrument_id).first()
        finally:
            db.close()
    
    def get_all_instruments(self, status: Optional[InstrumentStatus] = None) -> List[Instrument]:
        """Get all instruments, optionally filtered by status."""
        db = get_db()
        try:
            query = db.query(Instrument)
            if status:
                query = query.filter(Instrument.status == status)
            return query.all()
        finally:
            db.close()
    
    def search_instruments(self, search_term: str) -> List[Instrument]:
        """Search instruments by serial number or name."""
        db = get_db()
        try:
            return db.query(Instrument).filter(
                (Instrument.serial_number.contains(search_term)) |
                (Instrument.name.contains(search_term))
            ).all()
        finally:
            db.close()
    
    def update_instrument(self, instrument_id: int, **kwargs) -> Optional[Instrument]:
        """Update instrument fields."""
        db = get_db()
        try:
            instrument = db.query(Instrument).filter(Instrument.id == instrument_id).first()
            if not instrument:
                return None
            
            for key, value in kwargs.items():
                if hasattr(instrument, key):
                    if isinstance(value, str):
                        value = security.sanitize_input(value)
                    setattr(instrument, key, value)
            
            instrument.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(instrument)
            return instrument
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to update instrument: {str(e)}")
        finally:
            db.close()
    
    def delete_instrument(self, instrument_id: int) -> bool:
        """Delete instrument by ID."""
        db = get_db()
        try:
            instrument = db.query(Instrument).filter(Instrument.id == instrument_id).first()
            if not instrument:
                return False
            
            db.delete(instrument)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to delete instrument: {str(e)}")
        finally:
            db.close()

# Create singleton instance
instrument_controller = InstrumentController()
