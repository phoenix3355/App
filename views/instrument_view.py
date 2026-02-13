"""
Instrument View
PyQt6 view for managing instruments.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit,
                             QLabel, QDialog, QFormLayout, QComboBox, QDoubleSpinBox,
                             QDateEdit)
from PyQt6.QtCore import Qt, QDate
from datetime import datetime
from controllers.instrument_controller import instrument_controller
from models.instrument import InstrumentType, InstrumentStatus

class InstrumentView(QWidget):
    """View for managing instruments."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_instruments()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        
        # Search and action buttons
        top_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search by serial number or name...')
        self.search_input.textChanged.connect(self.filter_instruments)
        top_layout.addWidget(QLabel('Search:'))
        top_layout.addWidget(self.search_input)
        
        self.add_button = QPushButton('Add Instrument')
        self.add_button.clicked.connect(self.add_instrument)
        top_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton('Edit')
        self.edit_button.clicked.connect(self.edit_instrument)
        top_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_instrument)
        top_layout.addWidget(self.delete_button)
        
        layout.addLayout(top_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Serial Number', 'Name', 'Type', 'Manufacturer', 'Location', 'Status'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_instruments(self):
        """Load instruments into the table."""
        try:
            instruments = instrument_controller.get_all_instruments()
            self.display_instruments(instruments)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load instruments: {str(e)}')
    
    def display_instruments(self, instruments):
        """Display instruments in the table."""
        self.table.setRowCount(len(instruments))
        
        for row, instrument in enumerate(instruments):
            self.table.setItem(row, 0, QTableWidgetItem(str(instrument.id)))
            self.table.setItem(row, 1, QTableWidgetItem(instrument.serial_number))
            self.table.setItem(row, 2, QTableWidgetItem(instrument.name))
            self.table.setItem(row, 3, QTableWidgetItem(instrument.type.value))
            self.table.setItem(row, 4, QTableWidgetItem(instrument.manufacturer or ''))
            self.table.setItem(row, 5, QTableWidgetItem(instrument.location or ''))
            self.table.setItem(row, 6, QTableWidgetItem(instrument.status.value))
    
    def filter_instruments(self):
        """Filter instruments based on search input."""
        search_term = self.search_input.text().strip()
        
        if not search_term:
            self.load_instruments()
            return
        
        try:
            instruments = instrument_controller.search_instruments(search_term)
            self.display_instruments(instruments)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Search failed: {str(e)}')
    
    def add_instrument(self):
        """Show dialog to add a new instrument."""
        dialog = InstrumentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_instruments()
    
    def edit_instrument(self):
        """Edit selected instrument."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Warning', 'Please select an instrument to edit')
            return
        
        instrument_id = int(self.table.item(current_row, 0).text())
        instrument = instrument_controller.get_instrument(instrument_id)
        
        if instrument:
            dialog = InstrumentDialog(self, instrument)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_instruments()
    
    def delete_instrument(self):
        """Delete selected instrument."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Warning', 'Please select an instrument to delete')
            return
        
        instrument_id = int(self.table.item(current_row, 0).text())
        serial = self.table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f'Are you sure you want to delete instrument {serial}?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                instrument_controller.delete_instrument(instrument_id)
                self.load_instruments()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to delete instrument: {str(e)}')


class InstrumentDialog(QDialog):
    """Dialog for adding/editing instruments."""
    
    def __init__(self, parent=None, instrument=None):
        super().__init__(parent)
        self.instrument = instrument
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('Add Instrument' if not self.instrument else 'Edit Instrument')
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        # Serial Number
        self.serial_input = QLineEdit()
        if self.instrument:
            self.serial_input.setText(self.instrument.serial_number)
        layout.addRow('Serial Number:', self.serial_input)
        
        # Name
        self.name_input = QLineEdit()
        if self.instrument:
            self.name_input.setText(self.instrument.name)
        layout.addRow('Name:', self.name_input)
        
        # Type
        self.type_combo = QComboBox()
        for itype in InstrumentType:
            self.type_combo.addItem(itype.value, itype)
        if self.instrument:
            index = self.type_combo.findData(self.instrument.type)
            self.type_combo.setCurrentIndex(index)
        layout.addRow('Type:', self.type_combo)
        
        # Manufacturer
        self.manufacturer_input = QLineEdit()
        if self.instrument:
            self.manufacturer_input.setText(self.instrument.manufacturer or '')
        layout.addRow('Manufacturer:', self.manufacturer_input)
        
        # Model
        self.model_input = QLineEdit()
        if self.instrument:
            self.model_input.setText(self.instrument.model or '')
        layout.addRow('Model:', self.model_input)
        
        # Location
        self.location_input = QLineEdit()
        if self.instrument:
            self.location_input.setText(self.instrument.location or '')
        layout.addRow('Location:', self.location_input)
        
        # Status
        self.status_combo = QComboBox()
        for status in InstrumentStatus:
            self.status_combo.addItem(status.value, status)
        if self.instrument:
            index = self.status_combo.findData(self.instrument.status)
            self.status_combo.setCurrentIndex(index)
        layout.addRow('Status:', self.status_combo)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save)
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addRow(button_layout)
        
        self.setLayout(layout)
    
    def save(self):
        """Save the instrument."""
        serial = self.serial_input.text().strip()
        name = self.name_input.text().strip()
        
        if not serial or not name:
            QMessageBox.warning(self, 'Warning', 'Serial number and name are required')
            return
        
        try:
            instrument_type = self.type_combo.currentData()
            status = self.status_combo.currentData()
            
            if self.instrument:
                # Update existing
                instrument_controller.update_instrument(
                    self.instrument.id,
                    serial_number=serial,
                    name=name,
                    type=instrument_type,
                    manufacturer=self.manufacturer_input.text().strip(),
                    model=self.model_input.text().strip(),
                    location=self.location_input.text().strip(),
                    status=status,
                )
            else:
                # Create new
                instrument_controller.create_instrument(
                    serial_number=serial,
                    name=name,
                    instrument_type=instrument_type,
                    manufacturer=self.manufacturer_input.text().strip(),
                    model=self.model_input.text().strip(),
                    location=self.location_input.text().strip(),
                    status=status,
                )
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save instrument: {str(e)}')
