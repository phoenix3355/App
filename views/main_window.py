"""
Main Window
PyQt6 main application window with tabbed interface.
"""
from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                             QMenuBar, QMenu, QStatusBar, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from config import config
from views.instrument_view import InstrumentView
from views.calibration_view import CalibrationView
from views.inventory_view import InventoryView
from views.report_view import ReportView

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        app_name = config.get('app.name', 'Instrument Management System')
        self.setWindowTitle(f'{app_name} - {self.user.full_name}')
        self.setGeometry(100, 100, 1200, 800)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget with tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Add tabs
        self.instrument_view = InstrumentView()
        self.calibration_view = CalibrationView()
        self.inventory_view = InventoryView()
        self.report_view = ReportView()
        
        self.tabs.addTab(self.instrument_view, 'Instruments')
        self.tabs.addTab(self.calibration_view, 'Calibrations')
        self.tabs.addTab(self.inventory_view, 'Inventory')
        self.tabs.addTab(self.report_view, 'Reports')
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        refresh_action = QAction('&Refresh', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_all)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def refresh_all(self):
        """Refresh all views."""
        self.instrument_view.load_instruments()
        self.calibration_view.load_calibrations()
        self.inventory_view.load_inventory()
        self.status_bar.showMessage('All views refreshed', 3000)
    
    def show_about(self):
        """Show about dialog."""
        app_name = config.get('app.name', 'Instrument Management System')
        version = config.get('app.version', '1.0.0')
        
        about_text = f"""
        <h3>{app_name}</h3>
        <p>Version {version}</p>
        <p>A comprehensive desktop application for managing and calibrating instruments.</p>
        <p><b>Features:</b></p>
        <ul>
            <li>Instrument Management</li>
            <li>Calibration Tracking</li>
            <li>Inventory Management</li>
            <li>Report Generation</li>
        </ul>
        <p>Built with PyQt6, SQLAlchemy, and Jinja2.</p>
        """
        
        QMessageBox.about(self, 'About', about_text)
