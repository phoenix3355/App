# Configuration Guide

## Overview

The Instrument Management System uses a Laravel-style configuration system that allows flexible customization through environment variables and configuration files.

## Environment Variables

The application uses a `.env` file for configuration. Copy `.env.example` to `.env` and modify as needed.

### Database Configuration

```env
DATABASE_URL=sqlite:///instrument_management.db
```

**Options:**

- **SQLite** (default):
  ```env
  DATABASE_URL=sqlite:///instrument_management.db
  ```

- **PostgreSQL**:
  ```env
  DATABASE_URL=postgresql://username:password@localhost:5432/instrument_db
  ```

- **MySQL**:
  ```env
  DATABASE_URL=mysql://username:password@localhost:3306/instrument_db
  ```

- **SQL Server**:
  ```env
  DATABASE_URL=mssql+pyodbc://username:password@localhost/instrument_db?driver=ODBC+Driver+17+for+SQL+Server
  ```

### Application Configuration

```env
APP_NAME=Instrument Management System
APP_VERSION=1.0.0
DEBUG=False
```

**Parameters:**

- **APP_NAME**: Display name shown in the application title bar
- **APP_VERSION**: Version number for about dialog
- **DEBUG**: Enable/disable debug mode (True/False)
  - When True: Enables SQL query logging
  - When False: Disables verbose logging

### Security Configuration

```env
SECRET_KEY=your-secret-key-change-this
SESSION_TIMEOUT=3600
```

**Parameters:**

- **SECRET_KEY**: Secret key for session management
  - **Important**: Change this in production
  - Use a long, random string
  - Keep it confidential

- **SESSION_TIMEOUT**: Session timeout in seconds
  - Default: 3600 (1 hour)
  - Adjust based on your security requirements

## Advanced Configuration

### Password Security

The application uses bcrypt for password hashing. The number of hashing rounds is configurable in `config/__init__.py`:

```python
def _load_security_config(self) -> Dict[str, Any]:
    return {
        'secret_key': os.getenv('SECRET_KEY', 'change-this-secret-key'),
        'session_timeout': int(os.getenv('SESSION_TIMEOUT', '3600')),
        'bcrypt_rounds': 12,  # Increase for stronger security
    }
```

**Recommendations:**
- 10 rounds: Fast, suitable for development
- 12 rounds: Balanced (default)
- 14+ rounds: High security, slower

### Database Pool Settings

For production deployments with PostgreSQL or MySQL, you can configure connection pooling:

```python
# In models/__init__.py
engine = create_engine(
    config.get('database.url'),
    echo=config.get('database.echo', False),
    pool_pre_ping=True,
    pool_size=10,        # Number of connections to keep
    max_overflow=20,     # Max additional connections
    pool_recycle=3600,   # Recycle connections after 1 hour
)
```

### Custom Configuration Values

You can add custom configuration values by extending the config class:

```python
# In config/__init__.py

def _load_custom_config(self) -> Dict[str, Any]:
    """Load custom configuration."""
    return {
        'report_logo': os.getenv('REPORT_LOGO', ''),
        'company_name': os.getenv('COMPANY_NAME', 'Your Company'),
        'email_notifications': os.getenv('EMAIL_NOTIFICATIONS', 'False').lower() == 'true',
    }

# Add to _load_configs method:
self._config_cache = {
    'app': self._load_app_config(),
    'database': self._load_database_config(),
    'security': self._load_security_config(),
    'custom': self._load_custom_config(),  # Add this line
}
```

Then access via:
```python
from config import config
logo_path = config.get('custom.report_logo')
```

## Platform-Specific Configuration

### Windows

For Windows, ensure paths use forward slashes or escaped backslashes:

```env
DATABASE_URL=sqlite:///C:/Users/YourUser/Documents/instrument_db.db
```

### Linux/macOS

Use standard Unix paths:

```env
DATABASE_URL=sqlite:////home/user/instrument_db.db
```

## Configuration Loading Order

The application loads configuration in this order:

1. Environment variables from `.env` file
2. Default values in `config/__init__.py`
3. Runtime overrides via `config.set()`

## Production Configuration Checklist

Before deploying to production:

- [ ] Change SECRET_KEY to a strong random value
- [ ] Set DEBUG=False
- [ ] Configure appropriate database (not SQLite for multi-user)
- [ ] Set SESSION_TIMEOUT based on security policy
- [ ] Ensure database has proper backup strategy
- [ ] Set up proper file permissions on .env
- [ ] Configure database connection pooling
- [ ] Set up logging to file
- [ ] Configure regular database backups

## Configuration Examples

### Development Setup

```env
DATABASE_URL=sqlite:///dev_instrument_db.db
APP_NAME=Instrument Management System (Dev)
APP_VERSION=1.0.0-dev
DEBUG=True
SECRET_KEY=dev-secret-key-not-for-production
SESSION_TIMEOUT=86400
```

### Production Setup

```env
DATABASE_URL=postgresql://app_user:SecurePass123@db.company.com:5432/instruments_prod
APP_NAME=Instrument Management System
APP_VERSION=1.0.0
DEBUG=False
SECRET_KEY=tJT87nKLp9mQx5vR3wE2hB6nY8fC4dA1
SESSION_TIMEOUT=3600
```

### Testing Setup

```env
DATABASE_URL=sqlite:///:memory:
APP_NAME=Instrument Management System (Test)
APP_VERSION=1.0.0-test
DEBUG=True
SECRET_KEY=test-secret-key
SESSION_TIMEOUT=3600
```

## Troubleshooting Configuration Issues

### Database Connection Fails

1. Verify DATABASE_URL is correct
2. Check database server is running
3. Verify credentials are correct
4. Check firewall settings
5. Ensure database driver is installed (e.g., psycopg2 for PostgreSQL)

### Configuration Not Loading

1. Ensure .env file exists in project root
2. Check file permissions
3. Verify environment variable names are correct
4. Check for typos in .env file

### Permission Issues

Ensure the application has:
- Read access to .env file
- Write access to database file (for SQLite)
- Write access to reports/output/ directory
- Write access to log directory (if logging to file)

## Environment-Specific Configuration

You can use different .env files for different environments:

```bash
# Development
cp .env.example .env.development

# Production
cp .env.example .env.production

# Load specific environment
export ENV_FILE=.env.production
```

Then in your code:
```python
import os
from dotenv import load_dotenv

env_file = os.getenv('ENV_FILE', '.env')
load_dotenv(env_file)
```

## Validation

The configuration system includes validation for:
- Email format (in security module)
- Username format
- Password strength
- Input sanitization

Add custom validators as needed in `utils/security.py`.

## Configuration Best Practices

1. **Never commit .env files** - Add to .gitignore
2. **Use strong SECRET_KEY** - Generate with:
   ```python
   import secrets
   secrets.token_urlsafe(32)
   ```
3. **Document custom configs** - Update this guide when adding new configuration
4. **Validate input** - Always validate configuration values before use
5. **Use environment-specific configs** - Separate dev/test/prod configurations
6. **Back up configuration** - Keep secure backups of production .env
7. **Rotate secrets** - Periodically change SECRET_KEY and passwords
8. **Limit access** - Restrict who can view/modify configuration files
