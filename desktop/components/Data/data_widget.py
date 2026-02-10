from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont

class DataWidget(QWidget):
    def __init__(self):
        super().__init__()
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
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        self.summary_label = QLabel('Select a dataset to view details')
        self.summary_label.setFont(QFont('Arial', 12))
        self.summary_label.setStyleSheet('background-color: #e7f3ff; padding: 20px; border-radius: 8px; color: #004085; border: 1px solid #b8daff;')
        self.summary_label.setWordWrap(True)
        
        header = QLabel('Equipment Data')
        header.setFont(QFont('Arial', 15, QFont.Bold))
        header.setStyleSheet('color: #212529; margin-top: 15px; margin-bottom: 10px;')
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.summary_label)
        layout.addWidget(header)
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def update_data(self, dataset):
        summary_text = f"""
        <b>Dataset:</b> {dataset['filename']}<br>
        <b>Total Equipment:</b> {dataset['total_count']}<br>
        <b>Average Flowrate:</b> {dataset['avg_flowrate']:.2f}<br>
        <b>Average Pressure:</b> {dataset['avg_pressure']:.2f}<br>
        <b>Average Temperature:</b> {dataset['avg_temperature']:.2f}
        """
        self.summary_label.setText(summary_text)
        
        equipment = dataset['equipment']
        self.table.setRowCount(len(equipment))
        for i, eq in enumerate(equipment):
            self.table.setItem(i, 0, QTableWidgetItem(eq['name']))
            self.table.setItem(i, 1, QTableWidgetItem(eq['type']))
            self.table.setItem(i, 2, QTableWidgetItem(str(eq['flowrate'])))
            self.table.setItem(i, 3, QTableWidgetItem(str(eq['pressure'])))
            self.table.setItem(i, 4, QTableWidgetItem(str(eq['temperature'])))
