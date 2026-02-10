from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont

class UploadWidget(QFrame):
    def __init__(self, on_select, on_upload):
        super().__init__()
        self.on_select = on_select
        self.on_upload = on_upload
        self.init_ui()
    
    def init_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 5px;
            }
            QLabel {
                font-size: 1.2rem;
                color: #212529;
                border: none;
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
        
        layout = QVBoxLayout()
        
        title = QLabel('Upload CSV File')
        title.setFont(QFont("Rajdhani",15, QFont.Bold))
        title.setStyleSheet('color: #212529; border: none; margin-bottom: 10px;')
        
        file_row = QHBoxLayout()
        file_row.setSpacing(12)
        
        self.file_label = QLabel('No file selected')
        self.file_label.setStyleSheet('color: #6c757d; background-color: #f8f9fa; padding: 12px; border-radius: 6px; border: 1px solid #ced4da;')
        self.file_label.setMinimumWidth(300)
        
        select_btn = QPushButton('Choose File')
        select_btn.setStyleSheet('background-color: #28a745; min-width: 120px;')
        select_btn.clicked.connect(self.on_select)
        
        upload_btn = QPushButton('Upload')
        upload_btn.setStyleSheet('background-color: #007bff; min-width: 100px;')
        upload_btn.clicked.connect(self.on_upload)
        
        file_row.addWidget(self.file_label, 1)
        file_row.addWidget(select_btn)
        file_row.addWidget(upload_btn)
        
        layout.addWidget(title)
        layout.addLayout(file_row)
        self.setLayout(layout)
    
    def set_file_label(self, text):
        self.file_label.setText(text)
