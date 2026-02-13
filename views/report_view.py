"""
Report View
PyQt6 view for generating reports.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QMessageBox, QLabel, QTextBrowser, QGroupBox,
                             QRadioButton, QDateEdit)
from PyQt6.QtCore import Qt, QDate, QUrl
from datetime import datetime
import webbrowser
from controllers.report_controller import report_controller

class ReportView(QWidget):
    """View for generating reports."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Report Generation')
        title.setStyleSheet('font-size: 16px; font-weight: bold;')
        layout.addWidget(title)
        
        # Report type selection
        type_group = QGroupBox('Select Report Type')
        type_layout = QVBoxLayout()
        
        self.instrument_radio = QRadioButton('Instrument Report')
        self.instrument_radio.setChecked(True)
        type_layout.addWidget(self.instrument_radio)
        
        self.calibration_radio = QRadioButton('Calibration Report')
        type_layout.addWidget(self.calibration_radio)
        
        self.inventory_radio = QRadioButton('Inventory Report')
        type_layout.addWidget(self.inventory_radio)
        
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)
        
        # Date range for calibration reports
        date_group = QGroupBox('Date Range (for Calibration Reports)')
        date_layout = QHBoxLayout()
        
        date_layout.addWidget(QLabel('From:'))
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addMonths(-12))
        date_layout.addWidget(self.start_date)
        
        date_layout.addWidget(QLabel('To:'))
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        date_layout.addWidget(self.end_date)
        
        date_layout.addStretch()
        date_group.setLayout(date_layout)
        layout.addWidget(date_group)
        
        # Generate button
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton('Generate Report')
        self.generate_button.clicked.connect(self.generate_report)
        self.generate_button.setFixedHeight(40)
        button_layout.addStretch()
        button_layout.addWidget(self.generate_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Preview area
        preview_label = QLabel('Report Preview:')
        preview_label.setStyleSheet('font-weight: bold;')
        layout.addWidget(preview_label)
        
        self.preview_browser = QTextBrowser()
        self.preview_browser.setOpenExternalLinks(False)
        layout.addWidget(self.preview_browser)
        
        # Save button
        save_layout = QHBoxLayout()
        self.save_button = QPushButton('Save Report to File')
        self.save_button.clicked.connect(self.save_report)
        self.save_button.setEnabled(False)
        save_layout.addStretch()
        save_layout.addWidget(self.save_button)
        save_layout.addStretch()
        layout.addLayout(save_layout)
        
        self.setLayout(layout)
        
        self.current_html = None
    
    def generate_report(self):
        """Generate the selected report."""
        try:
            if self.instrument_radio.isChecked():
                html = report_controller.generate_instrument_report()
                report_type = 'instrument'
            elif self.calibration_radio.isChecked():
                start = self.start_date.date().toPyDate()
                end = self.end_date.date().toPyDate()
                html = report_controller.generate_calibration_report(
                    start_date=datetime.combine(start, datetime.min.time()),
                    end_date=datetime.combine(end, datetime.min.time())
                )
                report_type = 'calibration'
            else:
                html = report_controller.generate_inventory_report()
                report_type = 'inventory'
            
            self.current_html = html
            self.preview_browser.setHtml(html)
            self.save_button.setEnabled(True)
            
            QMessageBox.information(self, 'Success', f'{report_type.capitalize()} report generated successfully')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to generate report: {str(e)}')
    
    def save_report(self):
        """Save the current report to file."""
        if not self.current_html:
            QMessageBox.warning(self, 'Warning', 'No report to save. Generate a report first.')
            return
        
        try:
            # Determine filename based on report type
            if self.instrument_radio.isChecked():
                report_type = 'instrument'
            elif self.calibration_radio.isChecked():
                report_type = 'calibration'
            else:
                report_type = 'inventory'
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'{report_type}_report_{timestamp}.html'
            
            filepath = report_controller.save_report(self.current_html, filename)
            
            reply = QMessageBox.question(
                self, 'Report Saved',
                f'Report saved to:\n{filepath}\n\nOpen in browser?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                webbrowser.open('file://' + filepath)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save report: {str(e)}')
