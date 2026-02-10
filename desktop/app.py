import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFileDialog, QTabWidget, QMessageBox
from PyQt5.QtGui import QFont
from components.Login.login_widget import LoginWidget
from components.Header.header_widget import HeaderWidget
from components.Upload.upload_widget import UploadWidget
from components.History.history_widget import HistoryWidget
from components.Data.data_widget import DataWidget
from components.Chart.chart_widget import ChartWidget

API_URL = 'http://localhost:8000/api'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.username = None
        self.password = None
        self.datasets = []
        self.selected_dataset = None
        self.selected_file = None
        
        self.setWindowTitle('Chemical Equipment Visualizer')
        self.setGeometry(100, 100, 1200, 800)
        self.apply_styles()
        
        if not self.check_saved_login():
            self.show_login()
        else:
            self.show_main_ui()
            self.load_datasets()
    
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                color: #495057;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #007bff;
                border-bottom: 3px solid #007bff;
            }
        """)
    
    def check_saved_login(self):
        try:
            with open('.desktop_user.txt', 'r') as f:
                lines = f.read().strip().split('\n')
                if len(lines) == 2:
                    self.username = lines[0]
                    self.password = lines[1]
                    return True
        except:
            pass
        return False
    
    def save_login(self):
        with open('.desktop_user.txt', 'w') as f:
            f.write(f'{self.username}\n{self.password}')
    
    def show_login(self):
        self.setGeometry(100, 100, 450, 500)
        login_widget = LoginWidget(self.handle_login, self.handle_register)
        self.setCentralWidget(login_widget)
    
    def handle_login(self, username, password):
        try:
            response = requests.post(f'{API_URL}/login/', json={'username': username, 'password': password})
            if response.status_code == 200:
                self.username = username
                self.password = password
                self.save_login()
                self.setGeometry(100, 100, 1200, 800)
                self.show_main_ui()
                self.load_datasets()
            else:
                QMessageBox.warning(self, 'Error', 'Invalid credentials')
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))
    
    def handle_register(self, username, password):
        try:
            response = requests.post(f'{API_URL}/register/', json={'username': username, 'password': password})
            if response.status_code == 200:
                QMessageBox.information(self, 'Success', 'Registration successful! Please login.')
            else:
                QMessageBox.warning(self, 'Error', response.json().get('error', 'Registration failed'))
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))
    
    def show_main_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add components
        header = HeaderWidget(self.username)
        main_layout.addWidget(header)
        
        self.upload_widget = UploadWidget(self.select_file, self.upload_file)
        main_layout.addWidget(self.upload_widget)
        
        # Tabs
        tabs = QTabWidget()
        tabs.setFont(QFont('Arial', 11))
        
        self.history_widget = HistoryWidget(self.load_datasets, self.view_dataset)
        self.data_widget = DataWidget()
        self.chart_widget = ChartWidget()
        
        tabs.addTab(self.history_widget, 'History')
        tabs.addTab(self.data_widget, 'Data')
        tabs.addTab(self.chart_widget, 'Charts')
        
        main_layout.addWidget(tabs)
        central_widget.setLayout(main_layout)
    
    def select_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        if filename:
            self.selected_file = filename
            self.upload_widget.set_file_label(filename.split('/')[-1])
    
    def upload_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, 'Error', 'Please select a file')
            return
        
        try:
            with open(self.selected_file, 'rb') as f:
                files = {'file': f}
                response = requests.post(f'{API_URL}/upload/', files=files, auth=(self.username, self.password))
                if response.status_code == 201:
                    QMessageBox.information(self, 'Success', 'Upload successful!')
                    self.load_datasets()
                    self.selected_file = None
                    self.upload_widget.set_file_label('No file selected')
                else:
                    QMessageBox.warning(self, 'Error', response.json().get('error', 'Upload failed'))
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))
    
    def load_datasets(self):
        try:
            response = requests.get(f'{API_URL}/datasets/', auth=(self.username, self.password))
            if response.status_code == 200:
                self.datasets = response.json()
                self.history_widget.update_table(self.datasets)
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))
    
    def view_dataset(self, dataset_id):
        try:
            response = requests.get(f'{API_URL}/datasets/{dataset_id}/', auth=(self.username, self.password))
            if response.status_code == 200:
                self.selected_dataset = response.json()
                self.data_widget.update_data(self.selected_dataset)
                self.chart_widget.plot_data(self.selected_dataset)
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
