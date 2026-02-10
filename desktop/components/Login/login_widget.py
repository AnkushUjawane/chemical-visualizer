from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class LoginWidget(QWidget):
    def __init__(self, on_login, on_register):
        super().__init__()
        self.on_login = on_login
        self.on_register = on_register
        self.init_ui()
    
    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 30px;
            }
            QLabel {
                font-size: 14px;
                color: #212529;
            }
            QLineEdit {
                padding: 12px;
                font-size: 14px;
                border: 1px solid #ced4da;
                border-radius: 6px;
                background-color: white;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 6px;
                color: white;
                font-weight: 500;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        
        card = QFrame()
        card.setStyleSheet('background-color: white; border-radius: 8px; padding: 30px;')
        card.setMaximumWidth(350)
        
        login_layout = QVBoxLayout()
        login_layout.setSpacing(15)
        
        title = QLabel('Chemical Equipment Visualizer')
        title.setFont(QFont('Arial', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('color: #007bff; margin-bottom: 20px;')
        
        subtitle = QLabel('Login to your account')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet('color: #666; margin-bottom: 10px;')
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        self.username_input.setMinimumHeight(40)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        
        login_btn = QPushButton('Login')
        login_btn.setMinimumHeight(40)
        login_btn.setStyleSheet('background-color: #007bff; font-size: 14px; font-weight: bold;')
        login_btn.clicked.connect(self.handle_login)
        
        register_btn = QPushButton('Register')
        register_btn.setMinimumHeight(40)
        register_btn.setStyleSheet('background-color: #28a745; font-size: 14px; font-weight: bold;')
        register_btn.clicked.connect(self.handle_register)
        
        login_layout.addWidget(title)
        login_layout.addWidget(subtitle)
        login_layout.addWidget(self.username_input)
        login_layout.addWidget(self.password_input)
        login_layout.addWidget(login_btn)
        login_layout.addWidget(register_btn)
        
        card.setLayout(login_layout)
        main_layout.addWidget(card)
        self.setLayout(main_layout)
    
    def handle_login(self):
        self.on_login(self.username_input.text(), self.password_input.text())
    
    def handle_register(self):
        self.on_register(self.username_input.text(), self.password_input.text())
