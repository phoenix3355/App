# Instrument Management System

A comprehensive Python desktop application for managing and calibrating instruments, similar to QMSOFT.

## Features

- **Instrument Management**: Track gauges, sensors, meters, and other measuring instruments
- **Calibration Tracking**: Schedule and record calibrations, track due dates
- **Inventory Management**: Monitor instrument location, checkout/return instruments
- **Report Generation**: Generate HTML reports for instruments, calibrations, and inventory
- **User Authentication**: Secure login system with password hashing
- **Modern UI**: Clean PyQt6 interface with tabbed navigation

## Architecture

The application follows the **Model-View-Controller (MVC)** architecture:

- **Models**: SQLAlchemy ORM models for database entities (User, Instrument, Calibration, Inventory)
- **Views**: PyQt6-based user interface components
- **Controllers**: Business logic layer handling data operations

## Technology Stack

- **Python 3.x**
- **PyQt6**: Modern GUI framework
- **SQLAlchemy**: ORM for database operations
- **Jinja2**: HTML template engine for reports
- **bcrypt**: Password hashing for security
- **SQLite**: Default database (configurable)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/phoenix3355/App.git
   cd App
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

## Default Credentials

On first run, a default admin user is created:
- **Username**: `admin`
- **Password**: `Admin123`

**Important**: Change the password immediately after first login!

## Project Structure

```
App/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Example configuration file
├── config/                # Configuration management
│   └── __init__.py
├── models/                # Database models (SQLAlchemy)
│   ├── __init__.py
│   ├── user.py
│   ├── instrument.py
│   ├── calibration.py
│   └── inventory.py
├── views/                 # UI components (PyQt6)
│   ├── __init__.py
│   ├── login_window.py
│   ├── main_window.py
│   ├── instrument_view.py
│   ├── calibration_view.py
│   ├── inventory_view.py
│   └── report_view.py
├── controllers/           # Business logic
│   ├── __init__.py
│   ├── user_controller.py
│   ├── instrument_controller.py
│   ├── calibration_controller.py
│   ├── inventory_controller.py
│   └── report_controller.py
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── security.py
├── reports/              # Report templates and output
│   ├── templates/
│   │   ├── instrument_report.html
│   │   ├── calibration_report.html
│   │   └── inventory_report.html
│   └── output/           # Generated reports
└── docs/                 # Documentation
    ├── USER_GUIDE.md
    ├── CONFIGURATION.md
    └── EXTENSION_GUIDE.md
```

## Usage

### Managing Instruments

1. Navigate to the **Instruments** tab
2. Click **Add Instrument** to create a new instrument
3. Fill in the details (serial number, name, type, manufacturer, etc.)
4. Use **Edit** to modify existing instruments
5. Use **Delete** to remove instruments

### Tracking Calibrations

1. Navigate to the **Calibrations** tab
2. Click **Add Calibration** to record a new calibration
3. Select the instrument, enter calibration date and next due date
4. Record performer, status, and certificate number
5. Use **Show Due Calibrations** to view upcoming/overdue calibrations

### Managing Inventory

1. Navigate to the **Inventory** tab
2. Click **Add Inventory Item** to track instrument location/status
3. Use **Checkout** to assign instruments to users
4. Use **Return** to mark instruments as returned
5. Track quantities and locations

### Generating Reports

1. Navigate to the **Reports** tab
2. Select report type (Instrument, Calibration, or Inventory)
3. For calibration reports, set the date range
4. Click **Generate Report** to preview
5. Click **Save Report to File** to export as HTML

## Security Features

- **Password Hashing**: Uses bcrypt with configurable rounds
- **Input Validation**: Sanitizes all user inputs
- **Session Management**: Configurable session timeout
- **User Authentication**: Secure login system
- **Database Security**: Parameterized queries via SQLAlchemy ORM

## Configuration

Edit `.env` file to configure:

```env
# Database
DATABASE_URL=sqlite:///instrument_management.db

# Application
APP_NAME=Instrument Management System
APP_VERSION=1.0.0
DEBUG=False

# Security
SECRET_KEY=your-secret-key-here
SESSION_TIMEOUT=3600
```

## Extending the Application

The application is designed to be easily extensible:

### Adding New Instrument Types

Edit `models/instrument.py` and add to the `InstrumentType` enum:

```python
class InstrumentType(enum.Enum):
    # ... existing types
    NEW_TYPE = "new_type"
```

### Creating Custom Reports

1. Create a new Jinja2 template in `reports/templates/`
2. Add a method in `controllers/report_controller.py`
3. Add UI controls in `views/report_view.py`

### Adding New Models

1. Create model class in `models/`
2. Create controller in `controllers/`
3. Create view in `views/`
4. Add tab to `views/main_window.py`

## Requirements

- Python 3.8 or higher
- Windows, Linux, or macOS
- Minimum 4GB RAM
- 100MB disk space

## License

See LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub.

## Contributing

Contributions are welcome! Please read the contribution guidelines before submitting pull requests.