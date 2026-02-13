"""
Calibration Controller
Business logic for calibration tracking.
"""
from typing import Optional, List
from datetime import datetime
from models import get_db
from models.calibration import Calibration, CalibrationStatus
from utils.security import security

class CalibrationController:
    """Controller for calibration tracking operations."""
    
    def create_calibration(self, instrument_id: int, calibration_date: datetime,
                          **kwargs) -> Calibration:
        """
        Create a new calibration record.
        
        Args:
            instrument_id: ID of the instrument
            calibration_date: Date of calibration
            **kwargs: Additional fields
            
        Returns:
            Created Calibration object
        """
        db = get_db()
        try:
            calibration = Calibration(
                instrument_id=instrument_id,
                calibration_date=calibration_date,
                next_calibration_date=kwargs.get('next_calibration_date'),
                performed_by=security.sanitize_input(kwargs.get('performed_by', '')),
                status=kwargs.get('status', CalibrationStatus.PENDING),
                certificate_number=security.sanitize_input(kwargs.get('certificate_number', '')),
                standard_used=security.sanitize_input(kwargs.get('standard_used', '')),
                temperature=kwargs.get('temperature'),
                humidity=kwargs.get('humidity'),
                notes=security.sanitize_input(kwargs.get('notes', '')),
                results=security.sanitize_input(kwargs.get('results', '')),
                is_due=kwargs.get('is_due', False),
            )
            
            db.add(calibration)
            db.commit()
            db.refresh(calibration)
            return calibration
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to create calibration: {str(e)}")
        finally:
            db.close()
    
    def get_calibration(self, calibration_id: int) -> Optional[Calibration]:
        """Get calibration by ID."""
        db = get_db()
        try:
            return db.query(Calibration).filter(Calibration.id == calibration_id).first()
        finally:
            db.close()
    
    def get_all_calibrations(self, instrument_id: Optional[int] = None) -> List[Calibration]:
        """Get all calibrations, optionally filtered by instrument."""
        db = get_db()
        try:
            query = db.query(Calibration)
            if instrument_id:
                query = query.filter(Calibration.instrument_id == instrument_id)
            return query.order_by(Calibration.calibration_date.desc()).all()
        finally:
            db.close()
    
    def get_due_calibrations(self) -> List[Calibration]:
        """Get all due or overdue calibrations."""
        db = get_db()
        try:
            now = datetime.utcnow()
            return db.query(Calibration).filter(
                (Calibration.next_calibration_date <= now) |
                (Calibration.is_due == True)
            ).all()
        finally:
            db.close()
    
    def update_calibration(self, calibration_id: int, **kwargs) -> Optional[Calibration]:
        """Update calibration fields."""
        db = get_db()
        try:
            calibration = db.query(Calibration).filter(Calibration.id == calibration_id).first()
            if not calibration:
                return None
            
            for key, value in kwargs.items():
                if hasattr(calibration, key):
                    if isinstance(value, str):
                        value = security.sanitize_input(value)
                    setattr(calibration, key, value)
            
            calibration.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(calibration)
            return calibration
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to update calibration: {str(e)}")
        finally:
            db.close()
    
    def delete_calibration(self, calibration_id: int) -> bool:
        """Delete calibration by ID."""
        db = get_db()
        try:
            calibration = db.query(Calibration).filter(Calibration.id == calibration_id).first()
            if not calibration:
                return False
            
            db.delete(calibration)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to delete calibration: {str(e)}")
        finally:
            db.close()

# Create singleton instance
calibration_controller = CalibrationController()
