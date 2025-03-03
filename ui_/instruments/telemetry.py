from PyQt6.QtCore import QObject, pyqtSignal, QTimer
import math

class TelemetryManager(QObject):
    # Sinyaller
    attitude_data = pyqtSignal(dict)
    position_data = pyqtSignal(dict)
    system_status = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.connected = False
        
        # Test için timer
        self.test_timer = QTimer()
        self.test_timer.timeout.connect(self.generate_test_data)
        self.test_timer.start(100)  # 10 Hz
        
        self.test_values = {
            'roll': 0,
            'pitch': 0,
            'yaw': 0,
            'altitude': 100,
            'airspeed': 15,
            'vertical_speed': 0
        }
        
    def generate_test_data(self):
        """Test için telemetri verileri üret"""
        # Test değerlerini güncelle
        self.test_values['roll'] += 1
        if self.test_values['roll'] > 360:
            self.test_values['roll'] = 0
            
        self.test_values['pitch'] = 20 * math.sin(math.radians(self.test_values['roll']))
        self.test_values['yaw'] += 0.5
        if self.test_values['yaw'] > 360:
            self.test_values['yaw'] = 0
            
        # Verileri emit et
        self.attitude_data.emit(self.test_values)
        
        position_data = {
            'lat': 39.925533 + math.sin(math.radians(self.test_values['roll'])) * 0.001,
            'lon': 32.866287 + math.cos(math.radians(self.test_values['roll'])) * 0.001,
            'alt': self.test_values['altitude'],
            'heading': self.test_values['yaw']
        }
        self.position_data.emit(position_data)
        
        status_data = {
            'battery': 75,
            'gps_fix': True,
            'satellites': 8
        }
        self.system_status.emit(status_data)