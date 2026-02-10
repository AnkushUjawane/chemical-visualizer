from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtGui import QFont

class HistoryWidget(QWidget):
    def __init__(self, on_refresh, on_view):
        super().__init__()
        self.on_refresh = on_refresh
        self.on_view = on_view
        self.init_ui()
    
    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
            QLabel {
                font-size: 14px;
                color: #212529;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                gridline-color: #e9ecef;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 12px;
                color: #212529;
            }
            QHeaderView::section {
                background-color: #495057;
                color: white;
                padding: 14px;
                font-weight: 600;
                font-size: 13px;
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
        layout.setContentsMargins(15, 15, 15, 15)
        
        header = QLabel('Upload History (Last 5)')
        header.setFont(QFont('Arial', 15, QFont.Bold))
        header.setStyleSheet('color: #212529; margin-bottom: 15px;')
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Filename', 'Upload Date', 'Total Count', 'Actions'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        
        refresh_btn = QPushButton('Refresh')
        refresh_btn.setStyleSheet('background-color: #6c757d;')
        refresh_btn.clicked.connect(self.on_refresh)
        
        layout.addWidget(header)
        layout.addWidget(self.table)
        layout.addWidget(refresh_btn)
        self.setLayout(layout)
    
    def update_table(self, datasets):
        self.table.setRowCount(len(datasets))
        for i, ds in enumerate(datasets):
            self.table.setItem(i, 0, QTableWidgetItem(ds['filename']))
            self.table.setItem(i, 1, QTableWidgetItem(ds['uploaded_at']))
            self.table.setItem(i, 2, QTableWidgetItem(str(ds['total_count'])))
            
            view_btn = QPushButton('View')
            view_btn.setStyleSheet('background-color: #007bff; padding: 10px; font-size: 13px; min-width: 80px; max-width: 100px;')
            view_btn.clicked.connect(lambda checked, ds_id=ds['id']: self.on_view(ds_id))
            self.table.setCellWidget(i, 3, view_btn)
        
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(3, 110)
