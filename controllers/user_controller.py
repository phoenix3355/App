"""
User Controller
Business logic for user management and authentication.
"""
from typing import Optional, List
from datetime import datetime
from models import get_db
from models.user import User
from utils.security import security, ValidationError

class UserController:
    """Controller for user management operations."""
    
    def create_user(self, username: str, email: str, password: str, 
                   first_name: str = "", last_name: str = "", 
                   is_admin: bool = False) -> User:
        """
        Create a new user.
        
        Args:
            username: Username
            email: Email address
            password: Plain text password
            first_name: First name
            last_name: Last name
            is_admin: Admin flag
            
        Returns:
            Created User object
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate inputs
        if not security.validate_username(username):
            raise ValidationError("Invalid username format")
        
        if not security.validate_email(email):
            raise ValidationError("Invalid email format")
        
        is_valid, message = security.validate_password(password)
        if not is_valid:
            raise ValidationError(message)
        
        db = get_db()
        try:
            # Check if username or email already exists
            existing = db.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing:
                raise ValidationError("Username or email already exists")
            
            # Create user
            user = User(
                username=security.sanitize_input(username),
                email=security.sanitize_input(email),
                password_hash=security.hash_password(password),
                first_name=security.sanitize_input(first_name),
                last_name=security.sanitize_input(last_name),
                is_admin=is_admin,
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except ValidationError:
            raise
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to create user: {str(e)}")
        finally:
            db.close()
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        db = get_db()
        try:
            return db.query(User).filter(User.id == user_id).first()
        finally:
            db.close()
    
    def get_all_users(self) -> List[User]:
        """Get all users."""
        db = get_db()
        try:
            return db.query(User).all()
        finally:
            db.close()
    
    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """Update user fields."""
        db = get_db()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            for key, value in kwargs.items():
                if hasattr(user, key) and key != 'password_hash':
                    setattr(user, key, value)
            
            user.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to update user: {str(e)}")
        finally:
            db.close()
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID."""
        db = get_db()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            db.delete(user)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to delete user: {str(e)}")
        finally:
            db.close()
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user password."""
        db = get_db()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            # Verify old password
            if not security.verify_password(old_password, user.password_hash):
                raise ValidationError("Current password is incorrect")
            
            # Validate new password
            is_valid, message = security.validate_password(new_password)
            if not is_valid:
                raise ValidationError(message)
            
            # Update password
            user.password_hash = security.hash_password(new_password)
            user.updated_at = datetime.utcnow()
            db.commit()
            return True
        except ValidationError:
            raise
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to change password: {str(e)}")
        finally:
            db.close()

# Create singleton instance
user_controller = UserController()
