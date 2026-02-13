# Extension and Plugin Guide

## Overview

The Instrument Management System is designed with extensibility in mind, following a modular MVC architecture that makes it easy to add new features, instrument types, and custom functionality.

## Architecture Overview

The application follows a clean separation of concerns:

- **Models**: Database entities (SQLAlchemy ORM)
- **Views**: User interface (PyQt6)
- **Controllers**: Business logic
- **Config**: Configuration management
- **Utils**: Shared utilities

## Adding New Instrument Types

### Step 1: Update the Model

Edit `models/instrument.py` and add to the `InstrumentType` enum:

```python
class InstrumentType(enum.Enum):
    GAUGE = "gauge"
    SENSOR = "sensor"
    METER = "meter"
    ANALYZER = "analyzer"
    OTHER = "other"
    THERMOMETER = "thermometer"  # New type
    PRESSURE_GAUGE = "pressure_gauge"  # New type
```

### Step 2: Update the Database

If you have existing data, you'll need to handle the migration. For SQLite:

```python
# Run in Python console
from models import engine
from sqlalchemy import text

with engine.connect() as conn:
    # SQLite allows adding enum values without migration
    # Just restart the application
    pass
```

For PostgreSQL/MySQL, you may need a proper migration tool like Alembic.

### Step 3: UI Updates

The UI automatically picks up new enum values, so no changes needed in most cases. However, if you want custom handling:

```python
# In views/instrument_view.py
# Add custom logic in InstrumentDialog.init_ui() if needed
```

## Adding Custom Fields to Instruments

### Step 1: Update the Model

Edit `models/instrument.py`:

```python
class Instrument(Base):
    __tablename__ = 'instruments'
    
    # ... existing fields ...
    
    # New custom fields
    barcode = Column(String(100), unique=True)
    warranty_expiry = Column(DateTime)
    supplier = Column(String(200))
    custom_field1 = Column(String(500))
```

### Step 2: Update the Controller

Edit `controllers/instrument_controller.py`:

```python
def create_instrument(self, serial_number: str, name: str, 
                     instrument_type: InstrumentType = InstrumentType.GAUGE,
                     **kwargs) -> Instrument:
    # ... existing code ...
    
    instrument = Instrument(
        # ... existing fields ...
        barcode=security.sanitize_input(kwargs.get('barcode', '')),
        warranty_expiry=kwargs.get('warranty_expiry'),
        supplier=security.sanitize_input(kwargs.get('supplier', '')),
        custom_field1=security.sanitize_input(kwargs.get('custom_field1', '')),
    )
```

### Step 3: Update the View

Edit `views/instrument_view.py`:

```python
class InstrumentDialog(QDialog):
    def init_ui(self):
        # ... existing code ...
        
        # Add new fields
        self.barcode_input = QLineEdit()
        if self.instrument:
            self.barcode_input.setText(self.instrument.barcode or '')
        layout.addRow('Barcode:', self.barcode_input)
        
        # Add to table headers in InstrumentView
        self.table.setColumnCount(8)  # Increase count
        self.table.setHorizontalHeaderLabels([
            'ID', 'Serial Number', 'Name', 'Type', 'Manufacturer', 
            'Location', 'Status', 'Barcode'  # Add new column
        ])
```

### Step 4: Migrate the Database

```python
from models import Base, engine

# This will add new columns (for SQLite)
Base.metadata.create_all(bind=engine)
```

## Creating Custom Reports

### Step 1: Create a Template

Create `reports/templates/custom_report.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <style>
        /* Your custom styles */
        body { font-family: Arial, sans-serif; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    <p>Generated: {{ report_date }}</p>
    
    <table>
        <thead>
            <tr>
                <th>Column 1</th>
                <th>Column 2</th>
            </tr>
        </thead>
        <tbody>
            {% for item in data %}
            <tr>
                <td>{{ item.field1 }}</td>
                <td>{{ item.field2 }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
```

### Step 2: Add Controller Method

Edit `controllers/report_controller.py`:

```python
def generate_custom_report(self, filters: dict = None) -> str:
    """
    Generate custom HTML report.
    
    Args:
        filters: Optional filters for the report
        
    Returns:
        HTML report string
    """
    db = get_db()
    try:
        # Your custom query
        data = db.query(YourModel).filter(...).all()
        
        template = self.env.get_template('custom_report.html')
        html = template.render(
            data=data,
            report_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            title='Custom Report'
        )
        
        return html
    finally:
        db.close()
```

### Step 3: Add UI Controls

Edit `views/report_view.py`:

```python
# Add radio button in init_ui()
self.custom_radio = QRadioButton('Custom Report')
type_layout.addWidget(self.custom_radio)

# Update generate_report()
def generate_report(self):
    # ... existing code ...
    elif self.custom_radio.isChecked():
        html = report_controller.generate_custom_report()
        report_type = 'custom'
```

## Adding a New Module

### Step 1: Create the Model

Create `models/maintenance.py`:

```python
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

class Maintenance(Base):
    """Maintenance tracking model."""
    
    __tablename__ = 'maintenance'
    
    id = Column(Integer, primary_key=True, index=True)
    instrument_id = Column(Integer, ForeignKey('instruments.id'), nullable=False)
    maintenance_date = Column(DateTime, nullable=False)
    performed_by = Column(String(100))
    description = Column(String(1000))
    cost = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    instrument = relationship("Instrument", back_populates="maintenance_records")
    
    def __repr__(self):
        return f"<Maintenance(id={self.id}, instrument_id={self.instrument_id})>"
```

Update `models/instrument.py` to add the relationship:

```python
class Instrument(Base):
    # ... existing code ...
    maintenance_records = relationship("Maintenance", back_populates="instrument", cascade="all, delete-orphan")
```

### Step 2: Create the Controller

Create `controllers/maintenance_controller.py`:

```python
from typing import Optional, List
from datetime import datetime
from models import get_db
from models.maintenance import Maintenance
from utils.security import security

class MaintenanceController:
    """Controller for maintenance operations."""
    
    def create_maintenance(self, instrument_id: int, maintenance_date: datetime,
                          **kwargs) -> Maintenance:
        """Create a new maintenance record."""
        db = get_db()
        try:
            maintenance = Maintenance(
                instrument_id=instrument_id,
                maintenance_date=maintenance_date,
                performed_by=security.sanitize_input(kwargs.get('performed_by', '')),
                description=security.sanitize_input(kwargs.get('description', '')),
                cost=kwargs.get('cost'),
            )
            
            db.add(maintenance)
            db.commit()
            db.refresh(maintenance)
            return maintenance
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to create maintenance record: {str(e)}")
        finally:
            db.close()
    
    # Add other CRUD methods...

maintenance_controller = MaintenanceController()
```

### Step 3: Create the View

Create `views/maintenance_view.py`:

```python
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox)
from controllers.maintenance_controller import maintenance_controller

class MaintenanceView(QWidget):
    """View for managing maintenance records."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_maintenance()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        
        # Add buttons
        top_layout = QHBoxLayout()
        self.add_button = QPushButton('Add Maintenance')
        self.add_button.clicked.connect(self.add_maintenance)
        top_layout.addWidget(self.add_button)
        layout.addLayout(top_layout)
        
        # Add table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Instrument', 'Date', 'Performed By', 'Description', 'Cost'
        ])
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_maintenance(self):
        """Load maintenance records."""
        # Implementation...
        pass
    
    def add_maintenance(self):
        """Add new maintenance record."""
        # Implementation...
        pass

# Add dialog class similar to other views...
```

### Step 4: Register in Main Window

Edit `views/main_window.py`:

```python
from views.maintenance_view import MaintenanceView

class MainWindow(QMainWindow):
    def init_ui(self):
        # ... existing code ...
        
        self.maintenance_view = MaintenanceView()
        self.tabs.addTab(self.maintenance_view, 'Maintenance')
```

### Step 5: Update Database Initialization

Edit `models/__init__.py`:

```python
def init_db():
    """Initialize database tables."""
    from models.user import User
    from models.instrument import Instrument
    from models.calibration import Calibration
    from models.inventory import Inventory
    from models.maintenance import Maintenance  # Add this
    
    Base.metadata.create_all(bind=engine)
```

## Creating Custom Validators

Add to `utils/security.py`:

```python
@staticmethod
def validate_barcode(barcode: str) -> bool:
    """
    Validate barcode format.
    
    Args:
        barcode: Barcode to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Example: 13-digit EAN barcode
    pattern = r'^\d{13}$'
    return bool(re.match(pattern, barcode))

@staticmethod
def validate_serial_format(serial: str) -> bool:
    """
    Validate serial number format.
    
    Args:
        serial: Serial number to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Example: XXX-NNNN-YYYY format
    pattern = r'^[A-Z]{3}-\d{4}-\d{4}$'
    return bool(re.match(pattern, serial))
```

## Adding Custom Configuration

Edit `config/__init__.py`:

```python
def _load_custom_config(self) -> Dict[str, Any]:
    """Load custom configuration."""
    return {
        'calibration_interval_days': int(os.getenv('CALIBRATION_INTERVAL_DAYS', '365')),
        'require_certificate': os.getenv('REQUIRE_CERTIFICATE', 'True').lower() == 'true',
        'max_checkout_days': int(os.getenv('MAX_CHECKOUT_DAYS', '30')),
    }

# Add to _load_configs:
self._config_cache['custom'] = self._load_custom_config()
```

## Plugin System (Advanced)

For a more sophisticated plugin system:

### Step 1: Create Plugin Interface

Create `utils/plugin_interface.py`:

```python
from abc import ABC, abstractmethod

class PluginInterface(ABC):
    """Base interface for plugins."""
    
    @abstractmethod
    def initialize(self, app):
        """Initialize the plugin."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get plugin name."""
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Get plugin version."""
        pass
```

### Step 2: Create Plugin Loader

Create `utils/plugin_loader.py`:

```python
import importlib
import os
from pathlib import Path
from typing import List

class PluginLoader:
    """Load and manage plugins."""
    
    def __init__(self, plugin_dir: str = 'plugins'):
        self.plugin_dir = Path(plugin_dir)
        self.plugins = []
    
    def discover_plugins(self) -> List:
        """Discover available plugins."""
        if not self.plugin_dir.exists():
            return []
        
        plugins = []
        for file in self.plugin_dir.glob('*.py'):
            if file.name.startswith('_'):
                continue
            
            module_name = f'plugins.{file.stem}'
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, 'Plugin'):
                    plugins.append(module.Plugin())
            except Exception as e:
                print(f"Failed to load plugin {file.name}: {e}")
        
        return plugins
    
    def load_plugins(self, app):
        """Load all plugins."""
        self.plugins = self.discover_plugins()
        for plugin in self.plugins:
            plugin.initialize(app)
```

### Step 3: Create Example Plugin

Create `plugins/example_plugin.py`:

```python
from utils.plugin_interface import PluginInterface

class Plugin(PluginInterface):
    """Example plugin."""
    
    def initialize(self, app):
        """Initialize the plugin."""
        print(f"Initializing {self.get_name()} v{self.get_version()}")
        # Add custom functionality here
    
    def get_name(self) -> str:
        return "Example Plugin"
    
    def get_version(self) -> str:
        return "1.0.0"
```

## Best Practices

1. **Follow MVC Pattern**: Keep models, views, and controllers separate
2. **Use Controllers**: Don't put business logic in views
3. **Sanitize Input**: Always use `security.sanitize_input()` for user input
4. **Validate Data**: Add validators for custom fields
5. **Document Code**: Add docstrings to all classes and methods
6. **Handle Errors**: Use try/except blocks and show user-friendly messages
7. **Test Extensions**: Test thoroughly before deploying
8. **Version Control**: Use git branches for new features
9. **Database Migrations**: Plan for schema changes carefully
10. **Configuration**: Use config system for customizable values

## Testing Extensions

Create test files in a `tests/` directory:

```python
import unittest
from controllers.your_controller import your_controller

class TestYourController(unittest.TestCase):
    def setUp(self):
        # Setup test database
        pass
    
    def test_create(self):
        # Test create functionality
        pass
    
    def tearDown(self):
        # Cleanup
        pass

if __name__ == '__main__':
    unittest.main()
```

## Debugging Tips

1. **Enable Debug Mode**: Set `DEBUG=True` in .env
2. **Check Logs**: Enable SQL query logging
3. **Use Print Statements**: Add debug output temporarily
4. **PyQt Debugger**: Use Qt Creator for UI debugging
5. **Database Browser**: Use tools like DB Browser for SQLite

## Resources

- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **PyQt6 Documentation**: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- **Jinja2 Documentation**: https://jinja.palletsprojects.com/
- **Python Best Practices**: https://docs.python-guide.org/

## Getting Help

For questions about extending the application:
1. Review this guide and other documentation
2. Check the source code for examples
3. Open an issue on GitHub
4. Consult the community forums
