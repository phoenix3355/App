"""
Login Window
PyQt6 window for user authentication.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from utils.security import security, AuthenticationError

class LoginWindow(QWidget):
    """Login window for user authentication."""
    
    # Signal emitted when login is successful
    login_successful = pyqtSignal(object)  # Emits User object
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('Login - Instrument Management System')
        self.setFixedSize(400, 250)
        
        # Center window on screen
        self.center_on_screen()
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel('Instrument Management System')
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel('Username:')
        username_label.setFixedWidth(80)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter username')
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel('Password:')
        password_label.setFixedWidth(80)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText('Enter password')
        self.password_input.returnPressed.connect(self.handle_login)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        # Login button
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setFixedHeight(35)
        layout.addWidget(self.login_button)
        
        # Status label
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet('color: red;')
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        self.setLayout(layout)
    
    def center_on_screen(self):
        """Center the window on the screen."""
        from PyQt6.QtGui import QScreen
        screen = QScreen.availableGeometry(self.screen())
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def handle_login(self):
        """Handle login button click."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.status_label.setText('Please enter username and password')
            return
        
        try:
            # Authenticate user
            user = security.authenticate_user(username, password)
            
            if user:
                self.status_label.setText('')
                self.login_successful.emit(user)
                self.close()
            else:
                self.status_label.setText('Invalid credentials')
        except AuthenticationError as e:
            self.status_label.setText(str(e))
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Login error: {str(e)}')
    
    def clear_fields(self):
        """Clear input fields."""
        self.username_input.clear()
        self.password_input.clear()
        self.status_label.setText('')
