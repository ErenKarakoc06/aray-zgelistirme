from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
import math

class FlightInstrumentsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Enstrüman etiketleri
        self.attitude_label = QLabel("Attitude: 0° 0° 0°")
        self.altitude_label = QLabel("Altitude: 0 m")
        self.airspeed_label = QLabel("Airspeed: 0 m/s")
        self.heading_label = QLabel("Heading: 0°")
        self.vertical_speed_label = QLabel("Vertical Speed: 0 m/s")
        
        # Label stilini ayarla
        for label in [self.attitude_label, self.altitude_label, 
                     self.airspeed_label, self.heading_label,
                     self.vertical_speed_label]:
            label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: white;
                    background-color: #2c3e50;
                    padding: 5px;
                    border-radius: 5px;
                    margin: 2px;
                }
            """)
            layout.addWidget(label)
        
        self.setLayout(layout)
        
    def update_instruments(self, data):
        """Enstrümanları güncelle"""
        if 'roll' in data and 'pitch' in data and 'yaw' in data:
            self.attitude_label.setText(
                f"Attitude: {data['roll']:.1f}° {data['pitch']:.1f}° {data['yaw']:.1f}°"
            )
            
        if 'altitude' in data:
            self.altitude_label.setText(f"Altitude: {data['altitude']:.1f} m")
            
        if 'airspeed' in data:
            self.airspeed_label.setText(f"Airspeed: {data['airspeed']:.1f} m/s")
            
        if 'heading' in data:
            self.heading_label.setText(f"Heading: {data['heading']:.1f}°")
            
        if 'vertical_speed' in data:
            self.vertical_speed_label.setText(
                f"Vertical Speed: {data['vertical_speed']:.1f} m/s"
            )