"""
Inventory Controller
Business logic for inventory management.
"""
from typing import Optional, List
from datetime import datetime
from models import get_db
from models.inventory import Inventory, InventoryStatus
from utils.security import security

class InventoryController:
    """Controller for inventory management operations."""
    
    def create_inventory_item(self, instrument_id: int, **kwargs) -> Inventory:
        """
        Create a new inventory item.
        
        Args:
            instrument_id: ID of the instrument
            **kwargs: Additional fields
            
        Returns:
            Created Inventory object
        """
        db = get_db()
        try:
            inventory = Inventory(
                instrument_id=instrument_id,
                status=kwargs.get('status', InventoryStatus.IN_STOCK),
                location=security.sanitize_input(kwargs.get('location', '')),
                assigned_to=security.sanitize_input(kwargs.get('assigned_to', '')),
                checkout_date=kwargs.get('checkout_date'),
                return_date=kwargs.get('return_date'),
                quantity=kwargs.get('quantity', 1),
                notes=security.sanitize_input(kwargs.get('notes', '')),
            )
            
            db.add(inventory)
            db.commit()
            db.refresh(inventory)
            return inventory
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to create inventory item: {str(e)}")
        finally:
            db.close()
    
    def get_inventory_item(self, inventory_id: int) -> Optional[Inventory]:
        """Get inventory item by ID."""
        db = get_db()
        try:
            return db.query(Inventory).filter(Inventory.id == inventory_id).first()
        finally:
            db.close()
    
    def get_all_inventory(self, instrument_id: Optional[int] = None,
                         status: Optional[InventoryStatus] = None) -> List[Inventory]:
        """Get all inventory items, optionally filtered."""
        db = get_db()
        try:
            query = db.query(Inventory)
            if instrument_id:
                query = query.filter(Inventory.instrument_id == instrument_id)
            if status:
                query = query.filter(Inventory.status == status)
            return query.all()
        finally:
            db.close()
    
    def checkout_instrument(self, inventory_id: int, assigned_to: str) -> Optional[Inventory]:
        """Checkout an instrument."""
        db = get_db()
        try:
            inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
            if not inventory:
                return None
            
            inventory.status = InventoryStatus.CHECKED_OUT
            inventory.assigned_to = security.sanitize_input(assigned_to)
            inventory.checkout_date = datetime.utcnow()
            inventory.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(inventory)
            return inventory
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to checkout instrument: {str(e)}")
        finally:
            db.close()
    
    def return_instrument(self, inventory_id: int) -> Optional[Inventory]:
        """Return a checked out instrument."""
        db = get_db()
        try:
            inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
            if not inventory:
                return None
            
            inventory.status = InventoryStatus.IN_STOCK
            inventory.return_date = datetime.utcnow()
            inventory.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(inventory)
            return inventory
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to return instrument: {str(e)}")
        finally:
            db.close()
    
    def update_inventory(self, inventory_id: int, **kwargs) -> Optional[Inventory]:
        """Update inventory item fields."""
        db = get_db()
        try:
            inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
            if not inventory:
                return None
            
            for key, value in kwargs.items():
                if hasattr(inventory, key):
                    if isinstance(value, str):
                        value = security.sanitize_input(value)
                    setattr(inventory, key, value)
            
            inventory.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(inventory)
            return inventory
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to update inventory: {str(e)}")
        finally:
            db.close()
    
    def delete_inventory(self, inventory_id: int) -> bool:
        """Delete inventory item by ID."""
        db = get_db()
        try:
            inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
            if not inventory:
                return False
            
            db.delete(inventory)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to delete inventory: {str(e)}")
        finally:
            db.close()

# Create singleton instance
inventory_controller = InventoryController()
