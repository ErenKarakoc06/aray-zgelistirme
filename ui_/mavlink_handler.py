from pymavlink import mavutil
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
import time

class MAVLinkHandler(QObject):
    # Temel sinyaller
    connection_status = pyqtSignal(bool, str)
    telemetry_data = pyqtSignal(dict)
    parameter_received = pyqtSignal(str, float)
    calibration_progress = pyqtSignal(str, int)
    mission_received = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.vehicle = None
        self.connected = False
        
    def connect(self, connection_string):
        try:
            self.vehicle = mavutil.mavlink_connection(connection_string)
            self.vehicle.wait_heartbeat()
            self.connected = True
            self.connection_status.emit(True, "Bağlandı")
            self.start_telemetry()
            return True
        except Exception as e:
            self.connection_status.emit(False, str(e))
            return False
            
    def start_telemetry(self):
        self.telemetry_timer = QTimer()
        self.telemetry_timer.timeout.connect(self.update_telemetry)
        self.telemetry_timer.start(100)  # 10 Hz
        
    def update_telemetry(self):
        if not self.connected:
            return
            
        try:
            msg