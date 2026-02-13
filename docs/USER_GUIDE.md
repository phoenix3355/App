# User Guide

## Getting Started

### First Login

1. Launch the application by running `python main.py`
2. Login with the default credentials:
   - Username: `admin`
   - Password: `Admin123`
3. **Important**: Change your password immediately after first login

### Changing Your Password

To change your password, you'll need to create a new user with admin privileges and use that account to manage users.

## Instrument Management

### Adding an Instrument

1. Click the **Instruments** tab
2. Click **Add Instrument** button
3. Fill in the required fields:
   - **Serial Number** (required, unique)
   - **Name** (required)
   - **Type**: Select from Gauge, Sensor, Meter, Analyzer, or Other
   - **Manufacturer**: Optional
   - **Model**: Optional
   - **Location**: Where the instrument is stored
   - **Status**: Active, Inactive, Retired, or Maintenance
4. Click **Save**

### Editing an Instrument

1. Select an instrument from the table
2. Click **Edit** button
3. Modify the fields as needed
4. Click **Save**

### Deleting an Instrument

1. Select an instrument from the table
2. Click **Delete** button
3. Confirm the deletion

**Warning**: Deleting an instrument will also delete all associated calibration records and inventory items.

### Searching for Instruments

Use the search box at the top to search by serial number or name. The search is case-insensitive and searches partial matches.

## Calibration Management

### Recording a Calibration

1. Click the **Calibrations** tab
2. Click **Add Calibration** button
3. Fill in the fields:
   - **Instrument**: Select from dropdown
   - **Calibration Date**: Date the calibration was performed
   - **Next Due Date**: When the next calibration is due
   - **Performed By**: Name of the person who performed the calibration
   - **Status**: Passed, Failed, or Pending
   - **Certificate #**: Optional calibration certificate number
   - **Notes**: Any additional notes
4. Click **Save**

### Viewing Due Calibrations

1. Click the **Calibrations** tab
2. Click **Show Due Calibrations** button
3. The table will display only calibrations that are due or overdue

### Editing a Calibration

1. Select a calibration from the table
2. Click **Edit** button
3. Modify the fields as needed
4. Click **Save**

### Deleting a Calibration

1. Select a calibration from the table
2. Click **Delete** button
3. Confirm the deletion

## Inventory Management

### Adding an Inventory Item

1. Click the **Inventory** tab
2. Click **Add Inventory Item** button
3. Fill in the fields:
   - **Instrument**: Select from dropdown
   - **Status**: In Stock, In Use, Checked Out, Maintenance, or Lost
   - **Location**: Current location
   - **Quantity**: Number of items (default: 1)
   - **Notes**: Any additional notes
4. Click **Save**

### Checking Out an Instrument

1. Select an inventory item from the table
2. Click **Checkout** button
3. Enter the name of the person to assign the instrument to
4. Click **OK**

The instrument status will change to "Checked Out" and the checkout date will be recorded.

### Returning an Instrument

1. Select a checked-out inventory item from the table
2. Click **Return** button
3. Confirm the return

The instrument status will change back to "In Stock" and the return date will be recorded.

### Editing Inventory

1. Select an inventory item from the table
2. Click **Edit** button
3. Modify the fields as needed
4. Click **Save**

### Deleting Inventory Items

1. Select an inventory item from the table
2. Click **Delete** button
3. Confirm the deletion

## Report Generation

### Generating an Instrument Report

1. Click the **Reports** tab
2. Select **Instrument Report** radio button
3. Click **Generate Report** button
4. Preview the report in the browser
5. Click **Save Report to File** to export as HTML
6. Optionally open the report in your web browser

The instrument report includes:
- All instruments with their details
- Serial numbers, names, types, manufacturers
- Current status and location

### Generating a Calibration Report

1. Click the **Reports** tab
2. Select **Calibration Report** radio button
3. Set the date range using the **From** and **To** date pickers
4. Click **Generate Report** button
5. Preview the report in the browser
6. Click **Save Report to File** to export as HTML

The calibration report includes:
- All calibrations within the date range
- Instrument details
- Calibration dates and next due dates
- Status and certificate numbers

### Generating an Inventory Report

1. Click the **Reports** tab
2. Select **Inventory Report** radio button
3. Click **Generate Report** button
4. Preview the report in the browser
5. Click **Save Report to File** to export as HTML

The inventory report includes:
- All inventory items
- Instrument details
- Current location and status
- Assigned personnel and checkout dates

### Viewing Saved Reports

Reports are saved in the `reports/output/` directory as HTML files. You can:
- Open them in any web browser
- Print them
- Email them as attachments
- Archive them for record keeping

## Tips and Best Practices

### Regular Calibration Checks

- Review due calibrations weekly
- Set next calibration dates appropriately based on instrument requirements
- Record all calibration details promptly

### Inventory Management

- Update inventory status when instruments move
- Use the checkout/return feature to track who has instruments
- Keep location information current

### Data Entry

- Use consistent naming conventions for instruments
- Always fill in manufacturer and model information when available
- Add detailed notes for future reference

### Report Generation

- Generate and save regular reports for compliance
- Use date ranges in calibration reports for specific time periods
- Keep historical reports for audit trails

## Troubleshooting

### Login Issues

- Ensure you're using the correct username and password
- Passwords are case-sensitive
- Contact an administrator if you've forgotten your password

### Database Issues

- Ensure the database file has write permissions
- Check that the DATABASE_URL in .env is correct
- Back up your database regularly

### Report Generation Issues

- Ensure you have data in the system before generating reports
- Check that the reports/output/ directory exists and is writable
- For calibration reports, ensure the date range includes calibrations

## Keyboard Shortcuts

- **F5**: Refresh all views
- **Ctrl+Q**: Exit application
- **Enter**: Submit forms/login

## Getting Help

If you encounter issues:
1. Check this user guide
2. Review the configuration documentation
3. Check the GitHub issues page
4. Contact your system administrator
