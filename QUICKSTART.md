# Quick Start Guide

## Installation

1. **Install Python 3.8+**
   - Download from [python.org](https://www.python.org/downloads/)
   - Ensure Python is added to PATH

2. **Clone the repository**
   ```bash
   git clone https://github.com/phoenix3355/App.git
   cd App
   ```

3. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Linux/macOS:
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure the application**
   ```bash
   # Copy example configuration
   cp .env.example .env
   
   # Edit .env if needed (optional for quick start)
   ```

## First Run

1. **Launch the application**
   ```bash
   python main.py
   ```

2. **Login with default credentials**
   - Username: `admin`
   - Password: `Admin123`

3. **Change password immediately** (security best practice)

## Basic Usage

### Add Your First Instrument

1. Click the **Instruments** tab
2. Click **Add Instrument**
3. Fill in:
   - Serial Number: e.g., "SN-001"
   - Name: e.g., "Digital Pressure Gauge"
   - Type: Select from dropdown
   - Other fields as needed
4. Click **Save**

### Record a Calibration

1. Click the **Calibrations** tab
2. Click **Add Calibration**
3. Select the instrument
4. Set calibration date (today) and next due date (e.g., 1 year from now)
5. Enter performer name
6. Select status (Passed/Failed/Pending)
7. Click **Save**

### Track Inventory

1. Click the **Inventory** tab
2. Click **Add Inventory Item**
3. Select the instrument
4. Set location (e.g., "Storage Room A")
5. Click **Save**

### Generate Reports

1. Click the **Reports** tab
2. Select report type (Instrument/Calibration/Inventory)
3. Click **Generate Report**
4. Preview the report
5. Click **Save Report to File** to export
6. Open in browser to view/print

## Common Tasks

### Search for Instruments
- Use the search box in the Instruments tab
- Type serial number or name
- Results update as you type

### Check Due Calibrations
- Go to Calibrations tab
- Click **Show Due Calibrations**
- View all calibrations that need attention

### Checkout Instruments
- Go to Inventory tab
- Select an item
- Click **Checkout**
- Enter person's name
- Click OK

### Return Instruments
- Go to Inventory tab
- Select checked out item
- Click **Return**
- Confirm

## Keyboard Shortcuts

- **F5**: Refresh all views
- **Ctrl+Q**: Exit application
- **Enter**: Submit forms

## Troubleshooting

### Application won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)
- Try deleting the database and restarting: Delete `instrument_management.db`

### Can't login
- Use default credentials: admin / Admin123
- Check caps lock is off (passwords are case-sensitive)

### Database errors
- Delete the database file: `instrument_management.db`
- Restart the application (it will create a new database)

### UI not displaying correctly
- Ensure PyQt6 is properly installed: `pip install --upgrade PyQt6`
- Check system display scaling settings

## Next Steps

- Read the [User Guide](docs/USER_GUIDE.md) for detailed instructions
- Review [Configuration Guide](docs/CONFIGURATION.md) for customization
- Check [Extension Guide](docs/EXTENSION_GUIDE.md) for adding features

## Getting Help

- Check documentation in the `docs/` directory
- Review the README.md
- Open an issue on GitHub
- Contact system administrator

## Tips

- **Regular Backups**: Back up your database file regularly
- **Document Processes**: Use the notes fields to record important details
- **Export Reports**: Generate and save reports periodically for records
- **Keep Updated**: Check for software updates regularly
- **Calibration Intervals**: Set realistic next calibration dates based on requirements

## Security Reminders

- Change default admin password immediately
- Use strong passwords (8+ characters, mixed case, numbers)
- Don't share passwords
- Lock your computer when away
- Keep software updated

---

For detailed documentation, see:
- [README.md](README.md) - Full project overview
- [docs/USER_GUIDE.md](docs/USER_GUIDE.md) - Complete user manual
- [docs/CONFIGURATION.md](docs/CONFIGURATION.md) - Configuration options
- [docs/EXTENSION_GUIDE.md](docs/EXTENSION_GUIDE.md) - Developer guide
