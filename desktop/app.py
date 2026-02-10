import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QLineEdit, QLabel, QFileDialog, QTableWidget, 
                              QTableWidgetItem, QTabWidget, QMessageBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

API_URL = 'http://localhost:8000/api'

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle('Chemical Equipment Visualizer - Login')
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f4f8;
                font-family: Arial, sans-serif;
            }
            QLineEdit {
                padding: 12px;
                font-size: 14px;
                border: 2px solid #cbd5e0;
                border-radius: 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #4299e1;
            }
            QPushButton {
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                background-color: #4299e1;
                color: white;
            }
            QPushButton:hover {
                background-color: #3182ce;
            }
            QPushButton:pressed {
                background-color: #2c5282;
            }
            QLabel {
                font-size: 16px;
                color: #2d3748;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)
        
        title = QLabel('Chemical Equipment Visualizer')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('color: #2b6cb0; margin-bottom: 20px;')
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.login)
        register_btn = QPushButton('Register')
        register_btn.clicked.connect(self.register)
        register_btn.setStyleSheet('background-color: #48bb78;')
        
        layout.addWidget(title)
        layout.addWidget(QLabel('Username:'))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password_input)
        layout.addWidget(login_btn)
        layout.addWidget(register_btn)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            response = requests.post(f'{API_URL}/login/', json={'username': username, 'password': password})
            if response.status_code == 200:
                self.parent.set_credentials(username, password)
                self.close()
            else:
                QMessageBox.warning(self, 'Error', 'Invalid credentials')
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))
    
    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            response = requests.post(f'{API_URL}/register/', json={'username': username, 'password': password})
            if response.status_code == 200:
                QMessageBox.information(self, 'Success', 'Registration successful! Please login.')
            else:
                QMessageBox.warning(self, 'Error', response.json().get('error', 'Registration failed'))
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))

class ChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def plot_data(self, dataset):
        self.figure.clear()
        
        # Pie chart for type distribution
        ax1 = self.figure.add_subplot(221)
        types = list(dataset['type_distribution'].keys())
        counts = list(dataset['type_distribution'].values())
        ax1.pie(counts, labels=types, autopct='%1.1f%%')
        ax1.set_title('Equipment Type Distribution')
        
        # Bar chart for averages
        ax2 = self.figure.add_subplot(222)
        metrics = ['Flowrate', 'Pressure', 'Temperature']
        values = [dataset['avg_flowrate'], dataset['avg_pressure'], dataset['avg_temperature']]
        ax2.bar(metrics, values, color=['blue', 'red', 'green'])
        ax2.set_title('Average Parameters')
        ax2.set_ylabel('Value')
        
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.username = None
        self.password = None
        self.datasets = []
        self.selected_dataset = None
        
        self.setWindowTitle('Chemical Equipment Visualizer')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f7fafc;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                background-color: #4299e1;
                color: white;
            }
            QPushButton:hover {
                background-color: #3182ce;
            }
            QLabel {
                font-size: 13px;
                color: #2d3748;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                gridline-color: #e2e8f0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #4299e1;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
            }
            QTabWidget::pane {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #edf2f7;
                color: #4a5568;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #4299e1;
                color: white;
            }
        """)
        
        self.init_ui()
        self.show_login()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QFrame()
        header.setStyleSheet('background-color: #2b6cb0; border-radius: 10px; padding: 15px;')
        header_layout = QHBoxLayout()
        title = QLabel('📊 Chemical Equipment Visualizer')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setStyleSheet('color: white;')
        header_layout.addWidget(title)
        header.setLayout(header_layout)
        main_layout.addWidget(header)
        
        # Upload section
        upload_frame = QFrame()
        upload_frame.setStyleSheet('background-color: white; border-radius: 8px; padding: 15px;')
        upload_frame.setMaximumHeight(100)
        upload_layout = QHBoxLayout()
        upload_layout.setSpacing(10)
        
        upload_label = QLabel('📤 Upload CSV:')
        upload_label.setFont(QFont('Arial', 12, QFont.Bold))
        upload_label.setFixedWidth(100)
        
        self.file_label = QLabel('No file selected')
        self.file_label.setStyleSheet('color: #718096; font-style: italic; background-color: #f7fafc; padding: 10px; border-radius: 4px; border: 1px dashed #cbd5e0;')
        self.file_label.setMinimumWidth(250)
        
        select_btn = QPushButton('📁 Choose File')
        select_btn.setStyleSheet('background-color: #48bb78; padding: 10px 20px; min-width: 120px;')
        select_btn.clicked.connect(self.select_file)
        
        upload_btn = QPushButton('⬆️ Upload')
        upload_btn.setStyleSheet('background-color: #4299e1; padding: 10px 20px; min-width: 100px;')
        upload_btn.clicked.connect(self.upload_file)
        
        upload_layout.addWidget(upload_label)
        upload_layout.addWidget(self.file_label, 1)
        upload_layout.addWidget(select_btn)
        upload_layout.addWidget(upload_btn)
        upload_layout.addStretch(0)
        upload_frame.setLayout(upload_layout)
        main_layout.addWidget(upload_frame)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont('Arial', 11))
        
        # History tab
        history_widget = QWidget()
        history_layout = QVBoxLayout()
        history_layout.setContentsMargins(15, 15, 15, 15)
        
        history_header = QLabel('📜 Upload History (Last 5)')
        history_header.setFont(QFont('Arial', 14, QFont.Bold))
        history_header.setStyleSheet('color: #2d3748; margin-bottom: 10px;')
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(['Filename', 'Upload Date', 'Total Count', 'Actions'])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setAlternatingRowColors(True)
        
        refresh_btn = QPushButton('🔄 Refresh')
        refresh_btn.setStyleSheet('background-color: #ed8936;')
        refresh_btn.clicked.connect(self.load_datasets)
        
        history_layout.addWidget(history_header)
        history_layout.addWidget(self.history_table)
        history_layout.addWidget(refresh_btn)
        history_widget.setLayout(history_layout)
        
        # Data tab
        data_widget = QWidget()
        data_layout = QVBoxLayout()
        data_layout.setContentsMargins(15, 15, 15, 15)
        
        self.summary_label = QLabel('Select a dataset to view details')
        self.summary_label.setFont(QFont('Arial', 12))
        self.summary_label.setStyleSheet('background-color: #edf2f7; padding: 15px; border-radius: 8px; color: #2d3748;')
        self.summary_label.setWordWrap(True)
        
        data_header = QLabel('📋 Equipment Data')
        data_header.setFont(QFont('Arial', 14, QFont.Bold))
        data_header.setStyleSheet('color: #2d3748; margin-top: 15px; margin-bottom: 10px;')
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels(['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        self.data_table.horizontalHeader().setStretchLastSection(True)
        self.data_table.setAlternatingRowColors(True)
        
        data_layout.addWidget(self.summary_label)
        data_layout.addWidget(data_header)
        data_layout.addWidget(self.data_table)
        data_widget.setLayout(data_layout)
        
        # Charts tab
        self.chart_widget = ChartWidget()
        
        self.tabs.addTab(history_widget, '📜 History')
        self.tabs.addTab(data_widget, '📋 Data')
        self.tabs.addTab(self.chart_widget, '📊 Charts')
        
        main_layout.addWidget(self.tabs)
        central_widget.setLayout(main_layout)
        
        self.selected_file = None
    
    def show_login(self):
        self.login_window = LoginWindow(self)
        self.login_window.show()
    
    def set_credentials(self, username, password):
        self.username = username
        self.password = password
        self.setWindowTitle(f'Chemical Equipment Visualizer - {username}')
        self.statusBar().showMessage(f'Logged in as {username}', 3000)
        self.load_datasets()
    
    def select_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        if filename:
            self.selected_file = filename
            self.file_label.setText(filename.split('/')[-1])
    
    def upload_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, 'Error', 'Please select a file')
            return
        
        try:
            with open(self.selected_file, 'rb') as f:
                files = {'file': f}
                response = requests.post(f'{API_URL}/upload/', files=files, 
                                        auth=(self.username, self.password))
                if response.status_code == 201:
                    QMessageBox.information(self, 'Success', 'Upload successful!')
                    self.load_datasets()
                    self.selected_file = None
                    self.file_label.setText('No file selected')
                else:
                    QMessageBox.warning(self, 'Error', response.json().get('error', 'Upload failed'))
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))
    
    def load_datasets(self):
        try:
            response = requests.get(f'{API_URL}/datasets/', auth=(self.username, self.password))
            if response.status_code == 200:
                self.datasets = response.json()
                self.update_history_table()
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))
    
    def update_history_table(self):
        self.history_table.setRowCount(len(self.datasets))
        for i, ds in enumerate(self.datasets):
            self.history_table.setItem(i, 0, QTableWidgetItem(ds['filename']))
            self.history_table.setItem(i, 1, QTableWidgetItem(ds['uploaded_at']))
            self.history_table.setItem(i, 2, QTableWidgetItem(str(ds['total_count'])))
            
            view_btn = QPushButton('👁️ View Details')
            view_btn.setStyleSheet('background-color: #4299e1; padding: 10px 20px; font-size: 13px;')
            view_btn.clicked.connect(lambda checked, ds_id=ds['id']: self.view_dataset(ds_id))
            self.history_table.setCellWidget(i, 3, view_btn)
        
        self.history_table.resizeColumnsToContents()
        self.history_table.setColumnWidth(3, 150)
    
    def view_dataset(self, dataset_id):
        try:
            response = requests.get(f'{API_URL}/datasets/{dataset_id}/', auth=(self.username, self.password))
            if response.status_code == 200:
                self.selected_dataset = response.json()
                self.update_data_view()
                self.chart_widget.plot_data(self.selected_dataset)
                self.tabs.setCurrentIndex(1)
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))
    
    def update_data_view(self):
        ds = self.selected_dataset
        summary_text = f"""
        <b>Dataset:</b> {ds['filename']}<br>
        <b>Total Equipment:</b> {ds['total_count']}<br>
        <b>Average Flowrate:</b> {ds['avg_flowrate']:.2f}<br>
        <b>Average Pressure:</b> {ds['avg_pressure']:.2f}<br>
        <b>Average Temperature:</b> {ds['avg_temperature']:.2f}
        """
        self.summary_label.setText(summary_text)
        
        equipment = ds['equipment']
        self.data_table.setRowCount(len(equipment))
        for i, eq in enumerate(equipment):
            self.data_table.setItem(i, 0, QTableWidgetItem(eq['name']))
            self.data_table.setItem(i, 1, QTableWidgetItem(eq['type']))
            self.data_table.setItem(i, 2, QTableWidgetItem(str(eq['flowrate'])))
            self.data_table.setItem(i, 3, QTableWidgetItem(str(eq['pressure'])))
            self.data_table.setItem(i, 4, QTableWidgetItem(str(eq['temperature'])))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
