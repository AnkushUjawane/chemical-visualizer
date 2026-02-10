from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
        
        ax1 = self.figure.add_subplot(221)
        types = list(dataset['type_distribution'].keys())
        counts = list(dataset['type_distribution'].values())
        ax1.pie(counts, labels=types, autopct='%1.1f%%')
        ax1.set_title('Equipment Type Distribution')
        
        ax2 = self.figure.add_subplot(222)
        metrics = ['Flowrate', 'Pressure', 'Temperature']
        values = [dataset['avg_flowrate'], dataset['avg_pressure'], dataset['avg_temperature']]
        ax2.bar(metrics, values, color=['blue', 'red', 'green'])
        ax2.set_title('Average Parameters')
        ax2.set_ylabel('Value')
        
        self.canvas.draw()
