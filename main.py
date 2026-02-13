"""
Main Application Entry Point
Instrument Management System - Desktop Application
"""
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from models import init_db, close_db
from views.login_window import LoginWindow
from views.main_window import MainWindow
from controllers.user_controller import user_controller
from config import config

class Application:
    """Main application class."""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(config.get('app.name', 'Instrument Management System'))
        self.app.setApplicationVersion(config.get('app.version', '1.0.0'))
        
        # Enable high DPI scaling
        self.app.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        
        self.login_window = None
        self.main_window = None
        self.current_user = None
    
    def initialize_database(self):
        """Initialize the database and create default admin user."""
        try:
            init_db()
            
            # Create default admin user if no users exist
            users = user_controller.get_all_users()
            if not users:
                print("Creating default admin user...")
                user_controller.create_user(
                    username='admin',
                    email='admin@example.com',
                    password='Admin123',
                    first_name='Admin',
                    last_name='User',
                    is_admin=True
                )
                print("Default admin user created:")
                print("  Username: admin")
                print("  Password: Admin123")
                print("  Please change the password after first login!")
        except Exception as e:
            QMessageBox.critical(None, 'Database Error', 
                               f'Failed to initialize database: {str(e)}')
            sys.exit(1)
    
    def show_login(self):
        """Show the login window."""
        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.on_login_success)
        self.login_window.show()
    
    def on_login_success(self, user):
        """Handle successful login."""
        self.current_user = user
        self.show_main_window()
    
    def show_main_window(self):
        """Show the main application window."""
        self.main_window = MainWindow(self.current_user)
        self.main_window.show()
    
    def run(self):
        """Run the application."""
        self.initialize_database()
        self.show_login()
        result = self.app.exec()
        close_db()
        return result

def main():
    """Main entry point."""
    app = Application()
    sys.exit(app.run())

if __name__ == '__main__':
    main()
