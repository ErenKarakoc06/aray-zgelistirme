from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from pymavlink import mavutil
import time

class TelemetryManager(QObject):
    # Sinyaller
    attitude_data = pyqtSignal(dict)
    position_data = pyqtSignal(dict)
    system_status = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.connection = None
        self.connected = False
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update)
        
    def connect(self, connection_string):
        try:
            self.connection = mavutil.mavlink_connection(connection_string)
            self.connection.wait_heartbeat()
            self.connected = True
            self.update_timer.start(50)  # 20 Hz
            return True
        except Exception as e:
            print(f"Bağlantı hatası: {e}")
            return False
            
    def disconnect(self):
        if self.connection:
            self.update_timer.stop()
            self.connection.close()
            self.connected = False
            
    def update(self):
        if not self.connected:
            return
            
        try:
            # Attitude verileri
            msg = self.connection.recv_match(type='ATTITUDE', blocking=False)
            if msg:
                attitude_data = {
                    'roll': msg.roll,
                    'pitch': msg.pitch,
                    'yaw': msg.yaw,
                    'rollspeed': msg.rollspeed,
                    'pitchspeed': msg.pitchspeed,
                    'yawspeed': msg.yawspeed
                }
                self.attitude_data.emit(attitude_data)
                
            # Pozisyon verileri
            msg = self.connection.recv_match(type='GLOBAL_POSITION_INT', blocking=False)
            if msg:
                position_data = {
                    'lat': msg.lat / 1e7,
                    'lon': msg.lon / 1e7,
                    'alt': msg.alt / 1000.0,
                    'relative_alt': msg.relative_alt / 1000.0,
                    'vx': msg.vx / 100.0,
                    'vy': msg.vy / 100.0,
                    'vz': msg.vz / 100.0,
                    'hdg': msg.hdg / 100.0
                }
                self.position_data.emit(position_data)
                
            # Sistem durumu
            msg = self.connection.recv_match(type='SYS_STATUS', blocking=False)
            if msg:
                status_data = {
                    'voltage_battery': msg.voltage_battery / 1000.0,
                    'current_battery': msg.current_battery / 100.0,
                    'battery_remaining': msg.battery_remaining,
                    'onboard_control_sensors_present': msg.onboard_control_sensors_present,
                    'onboard_control_sensors_enabled': msg.onboard_control_sensors_enabled,
                    'onboard_control_sensors_health': msg.onboard_control_sensors_health
                }
                self.system_status.emit(status_data)
                
        except Exception as e:
            print(f"Telemetri güncelleme hatası: {e}")