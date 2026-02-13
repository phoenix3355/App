"""
Inventory View
PyQt6 view for managing inventory.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QLabel, QDialog, QFormLayout, QComboBox, QLineEdit,
                             QTextEdit, QSpinBox)
from PyQt6.QtCore import Qt
from controllers.inventory_controller import inventory_controller
from controllers.instrument_controller import instrument_controller
from models.inventory import InventoryStatus

class InventoryView(QWidget):
    """View for managing inventory."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_inventory()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        
        # Action buttons
        top_layout = QHBoxLayout()
        
        self.add_button = QPushButton('Add Inventory Item')
        self.add_button.clicked.connect(self.add_inventory)
        top_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton('Edit')
        self.edit_button.clicked.connect(self.edit_inventory)
        top_layout.addWidget(self.edit_button)
        
        self.checkout_button = QPushButton('Checkout')
        self.checkout_button.clicked.connect(self.checkout_instrument)
        top_layout.addWidget(self.checkout_button)
        
        self.return_button = QPushButton('Return')
        self.return_button.clicked.connect(self.return_instrument)
        top_layout.addWidget(self.return_button)
        
        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_inventory)
        top_layout.addWidget(self.delete_button)
        
        top_layout.addStretch()
        
        layout.addLayout(top_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Instrument', 'Location', 'Status', 'Assigned To', 'Checkout Date', 'Quantity'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_inventory(self):
        """Load inventory items into the table."""
        try:
            items = inventory_controller.get_all_inventory()
            self.display_inventory(items)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load inventory: {str(e)}')
    
    def display_inventory(self, items):
        """Display inventory items in the table."""
        self.table.setRowCount(len(items))
        
        for row, item in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(str(item.id)))
            self.table.setItem(row, 1, QTableWidgetItem(item.instrument.display_name))
            self.table.setItem(row, 2, QTableWidgetItem(item.location or ''))
            self.table.setItem(row, 3, QTableWidgetItem(item.status.value))
            self.table.setItem(row, 4, QTableWidgetItem(item.assigned_to or ''))
            checkout = item.checkout_date.strftime('%Y-%m-%d') if item.checkout_date else ''
            self.table.setItem(row, 5, QTableWidgetItem(checkout))
            self.table.setItem(row, 6, QTableWidgetItem(str(item.quantity)))
    
    def add_inventory(self):
        """Show dialog to add a new inventory item."""
        dialog = InventoryDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_inventory()
    
    def edit_inventory(self):
        """Edit selected inventory item."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Warning', 'Please select an inventory item to edit')
            return
        
        item_id = int(self.table.item(current_row, 0).text())
        item = inventory_controller.get_inventory_item(item_id)
        
        if item:
            dialog = InventoryDialog(self, item)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_inventory()
    
    def checkout_instrument(self):
        """Checkout selected instrument."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Warning', 'Please select an item to checkout')
            return
        
        item_id = int(self.table.item(current_row, 0).text())
        
        # Get assigned person name
        from PyQt6.QtWidgets import QInputDialog
        assigned_to, ok = QInputDialog.getText(self, 'Checkout', 'Assign to:')
        
        if ok and assigned_to:
            try:
                inventory_controller.checkout_instrument(item_id, assigned_to)
                self.load_inventory()
                QMessageBox.information(self, 'Success', 'Instrument checked out successfully')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to checkout: {str(e)}')
    
    def return_instrument(self):
        """Return selected instrument."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Warning', 'Please select an item to return')
            return
        
        item_id = int(self.table.item(current_row, 0).text())
        
        try:
            inventory_controller.return_instrument(item_id)
            self.load_inventory()
            QMessageBox.information(self, 'Success', 'Instrument returned successfully')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to return: {str(e)}')
    
    def delete_inventory(self):
        """Delete selected inventory item."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Warning', 'Please select an item to delete')
            return
        
        item_id = int(self.table.item(current_row, 0).text())
        
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            'Are you sure you want to delete this inventory item?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                inventory_controller.delete_inventory(item_id)
                self.load_inventory()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to delete: {str(e)}')


class InventoryDialog(QDialog):
    """Dialog for adding/editing inventory items."""
    
    def __init__(self, parent=None, inventory_item=None):
        super().__init__(parent)
        self.inventory_item = inventory_item
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('Add Inventory' if not self.inventory_item else 'Edit Inventory')
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        # Instrument
        self.instrument_combo = QComboBox()
        instruments = instrument_controller.get_all_instruments()
        for instrument in instruments:
            self.instrument_combo.addItem(instrument.display_name, instrument.id)
        
        if self.inventory_item:
            index = self.instrument_combo.findData(self.inventory_item.instrument_id)
            self.instrument_combo.setCurrentIndex(index)
        layout.addRow('Instrument:', self.instrument_combo)
        
        # Status
        self.status_combo = QComboBox()
        for status in InventoryStatus:
            self.status_combo.addItem(status.value, status)
        if self.inventory_item:
            index = self.status_combo.findData(self.inventory_item.status)
            self.status_combo.setCurrentIndex(index)
        layout.addRow('Status:', self.status_combo)
        
        # Location
        self.location_input = QLineEdit()
        if self.inventory_item:
            self.location_input.setText(self.inventory_item.location or '')
        layout.addRow('Location:', self.location_input)
        
        # Quantity
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(1000)
        if self.inventory_item:
            self.quantity_spin.setValue(self.inventory_item.quantity)
        else:
            self.quantity_spin.setValue(1)
        layout.addRow('Quantity:', self.quantity_spin)
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        if self.inventory_item:
            self.notes_input.setPlainText(self.inventory_item.notes or '')
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
        """Save the inventory item."""
        try:
            instrument_id = self.instrument_combo.currentData()
            status = self.status_combo.currentData()
            
            if self.inventory_item:
                # Update existing
                inventory_controller.update_inventory(
                    self.inventory_item.id,
                    instrument_id=instrument_id,
                    status=status,
                    location=self.location_input.text().strip(),
                    quantity=self.quantity_spin.value(),
                    notes=self.notes_input.toPlainText().strip(),
                )
            else:
                # Create new
                inventory_controller.create_inventory_item(
                    instrument_id=instrument_id,
                    status=status,
                    location=self.location_input.text().strip(),
                    quantity=self.quantity_spin.value(),
                    notes=self.notes_input.toPlainText().strip(),
                )
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save inventory item: {str(e)}')
