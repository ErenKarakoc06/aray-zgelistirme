from PyQt6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg
import numpy as np

class TelemetryGraphs(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Grafik widget'ları
        self.altitude_plot = self.create_plot("Yükseklik", "Zaman", "Metre")
        self.velocity_plot = self.create_plot("Hız", "Zaman", "m/s")
        self.attitude_plot = self.create_plot("Attitude", "Zaman", "Derece")
        
        layout.addWidget(self.altitude_plot)
        layout.addWidget(self.velocity_plot)
        layout.addWidget(self.attitude_plot)
        
        self.setLayout(layout)
        
        # Veri bufferları
        self.time_data = np.zeros(100)
        self.alt_data = np.zeros(100)
        self.vel_data = np.zeros(100)
        self.roll_data = np.zeros(100)
        self.pitch_data = np.zeros(100)
        self.yaw_data = np.zeros(100)
        
        self.ptr = 0
        
    def create_plot(self, title, x_label, y_label):
        plot_widget = pg.PlotWidget()
        plot_widget.setTitle(title)
        plot_widget.setLabel('left', y_label)
        plot_widget.setLabel('bottom', x_label)
        plot_widget.showGrid(x=True, y=True)
        return plot_widget
        
    def update_data(self, altitude, velocity, roll, pitch, yaw):
        self.time_data[:-1] = self.time_data[1:]
        self.alt_data[:-1] = self.alt_data[1:]
        self.vel_data[:-1] = self.vel_data[1:]
        self.roll_data[:-1] = self.roll_data[1:]
        self.pitch_data[:-1] = self.pitch_data[1:]
        self.yaw_data[:-1] = self.yaw_data[1:]
        
        self.time_data[-1] = self.ptr
        self.alt_data[-1] = altitude
        self.vel_data[-1] = velocity
        self.roll_data[-1] = roll
        self.pitch_data[-1] = pitch
        self.yaw_data[-1] = yaw
        
        self.ptr += 1
        
        # Grafikleri güncelle
        self.altitude_plot.plot(self.time_data, self.alt_data, clear=True)
        self.velocity_plot.plot(self.time_data, self.vel_data, clear=True)
        
        # Attitude grafiğinde roll, pitch ve yaw
        self.attitude_plot.plot(self.time_data, self.roll_data, pen='r', clear=True)
        self.attitude_plot.plot(self.time_data, self.pitch_data, pen='g')
        self.attitude_plot.plot(self.time_data, self.yaw_data, pen='b')