"""
Configuration Module
Laravel-style configuration system for the application.
"""
import os
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class with Laravel-style config management."""
    
    _instance = None
    _config_cache: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self._load_configs()
    
    def _load_configs(self):
        """Load all configuration files."""
        self._config_cache = {
            'app': self._load_app_config(),
            'database': self._load_database_config(),
            'security': self._load_security_config(),
        }
    
    def _load_app_config(self) -> Dict[str, Any]:
        """Load application configuration."""
        return {
            'name': os.getenv('APP_NAME', 'Instrument Management System'),
            'version': os.getenv('APP_VERSION', '1.0.0'),
            'debug': os.getenv('DEBUG', 'False').lower() == 'true',
        }
    
    def _load_database_config(self) -> Dict[str, Any]:
        """Load database configuration."""
        return {
            'url': os.getenv('DATABASE_URL', f'sqlite:///{self.BASE_DIR}/instrument_management.db'),
            'echo': os.getenv('DEBUG', 'False').lower() == 'true',
        }
    
    def _load_security_config(self) -> Dict[str, Any]:
        """Load security configuration."""
        return {
            'secret_key': os.getenv('SECRET_KEY', 'change-this-secret-key'),
            'session_timeout': int(os.getenv('SESSION_TIMEOUT', '3600')),
            'bcrypt_rounds': 12,
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        Example: config.get('database.url')
        """
        keys = key.split('.')
        value = self._config_cache
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set configuration value using dot notation.
        Example: config.set('app.debug', True)
        """
        keys = key.split('.')
        config = self._config_cache
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value

# Singleton instance
config = Config()
