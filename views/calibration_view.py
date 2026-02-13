"""
Calibration View
PyQt6 view for managing calibrations.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QLabel, QDialog, QFormLayout, QComboBox, QLineEdit,
                             QDateEdit, QTextEdit, QDoubleSpinBox)
from PyQt6.QtCore import Qt, QDate
from datetime import datetime
from controllers.calibration_controller import calibration_controller
from controllers.instrument_controller import instrument_controller
from models.calibration import CalibrationStatus

class CalibrationView(QWidget):
    """View for managing calibrations."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_calibrations()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        
        # Action buttons
        top_layout = QHBoxLayout()
        
        self.add_button = QPushButton('Add Calibration')
        self.add_button.clicked.connect(self.add_calibration)
        top_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton('Edit')
        self.edit_button.clicked.connect(self.edit_calibration)
        top_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_calibration)
        top_layout.addWidget(self.delete_button)
        
        self.show_due_button = QPushButton('Show Due Calibrations')
        self.show_due_button.clicked.connect(self.show_due_calibrations)
        top_layout.addWidget(self.show_due_button)
        
        top_layout.addStretch()
        
        layout.addLayout(top_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Instrument', 'Calibration Date', 'Next Due', 'Performed By', 'Status', 'Certificate #'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_calibrations(self):
        """Load calibrations into the table."""
        try:
            calibrations = calibration_controller.get_all_calibrations()
            self.display_calibrations(calibrations)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load calibrations: {str(e)}')
    
    def display_calibrations(self, calibrations):
        """Display calibrations in the table."""
        self.table.setRowCount(len(calibrations))
        
        for row, calibration in enumerate(calibrations):
            self.table.setItem(row, 0, QTableWidgetItem(str(calibration.id)))
            self.table.setItem(row, 1, QTableWidgetItem(calibration.instrument.display_name))
            self.table.setItem(row, 2, QTableWidgetItem(calibration.calibration_date.strftime('%Y-%m-%d')))
            next_due = calibration.next_calibration_date.strftime('%Y-%m-%d') if calibration.next_calibration_date else 'N/A'
            self.table.setItem(row, 3, QTableWidgetItem(next_due))
            self.table.setItem(row, 4, QTableWidgetItem(calibration.performed_by or ''))
            self.table.setItem(row, 5, QTableWidgetItem(calibration.status.value))
            self.table.setItem(row, 6, QTableWidgetItem(calibration.certificate_number or ''))
    
    def show_due_calibrations(self):
        """Show only due calibrations."""
        try:
            calibrations = calibration_controller.get_due_calibrations()
            self.display_calibrations(calibrations)
            QMessageBox.information(self, 'Info', f'Found {len(calibrations)} due calibrations')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load due calibrations: {str(e)}')
    
    def add_calibration(self):
        """Show dialog to add a new calibration."""
        dialog = CalibrationDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_calibrations()
    
    def edit_calibration(self):
        """Edit selected calibration."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Warning', 'Please select a calibration to edit')
            return
        
        calibration_id = int(self.table.item(current_row, 0).text())
        calibration = calibration_controller.get_calibration(calibration_id)
        
        if calibration:
            dialog = CalibrationDialog(self, calibration)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_calibrations()
    
    def delete_calibration(self):
        """Delete selected calibration."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Warning', 'Please select a calibration to delete')
            return
        
        calibration_id = int(self.table.item(current_row, 0).text())
        
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            'Are you sure you want to delete this calibration?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                calibration_controller.delete_calibration(calibration_id)
                self.load_calibrations()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to delete calibration: {str(e)}')


class CalibrationDialog(QDialog):
    """Dialog for adding/editing calibrations."""
    
    def __init__(self, parent=None, calibration=None):
        super().__init__(parent)
        self.calibration = calibration
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('Add Calibration' if not self.calibration else 'Edit Calibration')
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        # Instrument
        self.instrument_combo = QComboBox()
        instruments = instrument_controller.get_all_instruments()
        for instrument in instruments:
            self.instrument_combo.addItem(instrument.display_name, instrument.id)
        
        if self.calibration:
            index = self.instrument_combo.findData(self.calibration.instrument_id)
            self.instrument_combo.setCurrentIndex(index)
        layout.addRow('Instrument:', self.instrument_combo)
        
        # Calibration Date
        self.cal_date = QDateEdit()
        self.cal_date.setCalendarPopup(True)
        if self.calibration:
            self.cal_date.setDate(QDate(self.calibration.calibration_date.year,
                                        self.calibration.calibration_date.month,
                                        self.calibration.calibration_date.day))
        else:
            self.cal_date.setDate(QDate.currentDate())
        layout.addRow('Calibration Date:', self.cal_date)
        
        # Next Calibration Date
        self.next_date = QDateEdit()
        self.next_date.setCalendarPopup(True)
        if self.calibration and self.calibration.next_calibration_date:
            self.next_date.setDate(QDate(self.calibration.next_calibration_date.year,
                                        self.calibration.next_calibration_date.month,
                                        self.calibration.next_calibration_date.day))
        else:
            self.next_date.setDate(QDate.currentDate().addYears(1))
        layout.addRow('Next Due Date:', self.next_date)
        
        # Performed By
        self.performed_by_input = QLineEdit()
        if self.calibration:
            self.performed_by_input.setText(self.calibration.performed_by or '')
        layout.addRow('Performed By:', self.performed_by_input)
        
        # Status
        self.status_combo = QComboBox()
        for status in CalibrationStatus:
            self.status_combo.addItem(status.value, status)
        if self.calibration:
            index = self.status_combo.findData(self.calibration.status)
            self.status_combo.setCurrentIndex(index)
        layout.addRow('Status:', self.status_combo)
        
        # Certificate Number
        self.cert_input = QLineEdit()
        if self.calibration:
            self.cert_input.setText(self.calibration.certificate_number or '')
        layout.addRow('Certificate #:', self.cert_input)
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)
        if self.calibration:
            self.notes_input.setPlainText(self.calibration.notes or '')
        layout.addRow('Notes:', self.notes_input)
        
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
        """Save the calibration."""
        try:
            instrument_id = self.instrument_combo.currentData()
            cal_date = self.cal_date.date().toPyDate()
            next_date = self.next_date.date().toPyDate()
            status = self.status_combo.currentData()
            
            if self.calibration:
                # Update existing
                calibration_controller.update_calibration(
                    self.calibration.id,
                    instrument_id=instrument_id,
                    calibration_date=datetime.combine(cal_date, datetime.min.time()),
                    next_calibration_date=datetime.combine(next_date, datetime.min.time()),
                    performed_by=self.performed_by_input.text().strip(),
                    status=status,
                    certificate_number=self.cert_input.text().strip(),
                    notes=self.notes_input.toPlainText().strip(),
                )
            else:
                # Create new
                calibration_controller.create_calibration(
                    instrument_id=instrument_id,
                    calibration_date=datetime.combine(cal_date, datetime.min.time()),
                    next_calibration_date=datetime.combine(next_date, datetime.min.time()),
                    performed_by=self.performed_by_input.text().strip(),
                    status=status,
                    certificate_number=self.cert_input.text().strip(),
                    notes=self.notes_input.toPlainText().strip(),
                )
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save calibration: {str(e)}')
