from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class HeaderWidget(QFrame):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.init_ui()
    
    def init_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 5px;
                border: 1px solid #dee2e6;
            }
            QLabel {
                font-size: 1.2rem;
                color: #212529;
                border: none;
            }
        """)
        
        layout = QVBoxLayout()
        
        title = QLabel('Chemical Equipment Visualizer')
        title.setFont(QFont("Rajdhani", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('color: #212529; border: none;')
        
        subtitle = QLabel(f'Welcome, {self.username}')
        subtitle.setFont(QFont("Rajdhani", 13))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet('color: #6c757d; border: none;')
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        self.setLayout(layout)
