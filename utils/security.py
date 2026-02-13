"""
Security Utilities
Provides authentication, validation, and security functions.
"""
import re
import bcrypt
from datetime import datetime
from typing import Optional
from models import get_db
from models.user import User
from config import config

class AuthenticationError(Exception):
    """Exception raised for authentication failures."""
    pass

class ValidationError(Exception):
    """Exception raised for validation failures."""
    pass

class Security:
    """Security utilities for authentication and validation."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        rounds = config.get('security.bcrypt_rounds', 12)
        salt = bcrypt.gensalt(rounds=rounds)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verify a password against a hash.
        
        Args:
            password: Plain text password
            password_hash: Hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception:
            return False
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[User]:
        """
        Authenticate a user with username and password.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            User object if authentication succeeds, None otherwise
            
        Raises:
            AuthenticationError: If authentication fails
        """
        db = get_db()
        try:
            user = db.query(User).filter(User.username == username).first()
            
            if not user:
                raise AuthenticationError("Invalid username or password")
            
            if not user.is_active:
                raise AuthenticationError("User account is disabled")
            
            if not Security.verify_password(password, user.password_hash):
                raise AuthenticationError("Invalid username or password")
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.commit()
            
            return user
        except AuthenticationError:
            raise
        except Exception as e:
            db.rollback()
            raise AuthenticationError(f"Authentication error: {str(e)}")
        finally:
            db.close()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: Email address
            
        Returns:
            True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """
        Validate username format.
        
        Args:
            username: Username
            
        Returns:
            True if valid, False otherwise
        """
        # Username must be 3-50 characters, alphanumeric and underscores only
        pattern = r'^[a-zA-Z0-9_]{3,50}$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """
        Validate password strength.
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one digit"
        
        return True, "Password is valid"
    
    @staticmethod
    def sanitize_input(input_str: str, max_length: int = 500) -> str:
        """
        Sanitize user input to prevent injection attacks.
        
        Args:
            input_str: Input string to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not input_str:
            return ""
        
        # Remove null bytes
        sanitized = input_str.replace('\x00', '')
        
        # Truncate to max length
        sanitized = sanitized[:max_length]
        
        # Strip leading/trailing whitespace
        sanitized = sanitized.strip()
        
        return sanitized

# Create singleton instance
security = Security()
