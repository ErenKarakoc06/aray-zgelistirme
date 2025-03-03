from pymavlink import mavutil
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
import time

class MAVLinkHandler(QObject):
    # Sinyaller
    connection_status = pyqtSignal(bool, str)
    attitude_data = pyqtSignal(float, float, float)  # roll, pitch, yaw
    position_data = pyqtSignal(float, float, float)  # lat, lon, alt
    velocity_data = pyqtSignal(float, float, float)  # vx, vy, vz
    gps_data = pyqtSignal(int, int)  # fix type, satellite count
    battery_data = pyqtSignal(float, float)  # voltage, current
    mode_data = pyqtSignal(str)
    armed_status = pyqtSignal(bool)
    mission_current = pyqtSignal(int)
    mission_reached = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.connection = None
        self.connected = False
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update)
        self.heartbeat_timer = QTimer()
        self.heartbeat_timer.timeout.connect(self.send_heartbeat)

    def connect(self, connection_string):
        try:
            self.connection = mavutil.mavlink_connection(connection_string)
            self.wait_heartbeat()
            self.connected = True
            self.connection_status.emit(True, "Bağlantı başarılı")
            self.update_timer.start(100)  # 10 Hz
            self.heartbeat_timer.start(1000)  # 1 Hz
            return True
        except Exception as e:
            self.connection_status.emit(False, f"Bağlantı hatası: {str(e)}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connected = False
            self.update_timer.stop()
            self.heartbeat_timer.stop()
            self.connection_status.emit(False, "Bağlantı kesildi")

    def wait_heartbeat(self):
        self.connection.wait_heartbeat()

    def send_heartbeat(self):
        if self.connected:
            self.connection.mav.heartbeat_send(
                mavutil.mavlink.MAV_TYPE_GCS,
                mavutil.mavlink.MAV_AUTOPILOT_INVALID,
                0, 0, 0)

    def update(self):
        if not self.connected:
            return

        # Mesajları al
        while True:
            msg = self.connection.recv_match(blocking=False)
            if not msg:
                break

            msg_type = msg.get_type()

            if msg_type == "ATTITUDE":
                self.attitude_data.emit(
                    msg.roll, msg.pitch, msg.yaw)
            
            elif msg_type == "GLOBAL_POSITION_INT":
                self.position_data.emit(
                    msg.lat / 1e7,
                    msg.lon / 1e7,
                    msg.relative_alt / 1000.0)
            
            elif msg_type == "VFR_HUD":
                self.velocity_data.emit(
                    msg.airspeed,
                    msg.groundspeed,
                    msg.climb)
            
            elif msg_type == "GPS_RAW_INT":
                self.gps_data.emit(
                    msg.fix_type,
                    msg.satellites_visible)
            
            elif msg_type == "SYS_STATUS":
                self.battery_data.emit(
                    msg.voltage_battery / 1000.0,
                    msg.current_battery / 100.0)
            
            elif msg_type == "HEARTBEAT":
                flight_mode = mavutil.mode_string_v10(msg)
                self.mode_data.emit(flight_mode)
                self.armed_status.emit(msg.base_mode & 
                    mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)

    def set_mode(self, mode):
        if self.connected:
            if mode == "RTL":
                mode_id = mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED
                self.connection.set_mode(mode_id)
            # Diğer modlar için benzer şekilde...

    def arm(self, arm=True):
        if self.connected:
            self.connection.mav.command_long_send(
                self.connection.target_system,
                self.connection.target_component,
                mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                0, 1 if arm else 0, 0, 0, 0, 0, 0, 0)

    def upload_mission(self, mission_items):
        if not self.connected:
            return False

        # Mevcut görevi temizle
        self.connection.mav.mission_clear_all_send(
            self.connection.target_system,
            self.connection.target_component)
        
        # Yeni görevi yükle
        for i, item in enumerate(mission_items):
            self.connection.mav.mission_item_send(
                self.connection.target_system,
                self.connection.target_component,
                i,
                item.frame,
                item.command,
                item.current,
                item.autocontinue,
                item.param1,
                item.param2,
                item.param3,
                item.param4,
                item.x,
                item.y,
                item.z)

        return True

    def download_mission(self):
        if not self.connected:
            return None

        # Görev sayısını iste
        self.connection.mav.mission_request_list_send(
            self.connection.target_system,
            self.connection.target_component)
        
        msg = self.connection.recv_match(type=['MISSION_COUNT'],
                                       blocking=True,
                                       timeout=5)
        
        if not msg:
            return None

        mission_items = []
        
        # Her görev noktasını al
        for i in range(msg.count):
            self.connection.mav.mission_request_send(
                self.connection.target_system,
                self.connection.target_component,
                i)
            
            msg = self.connection.recv_match(type=['MISSION_ITEM'],
                                           blocking=True,
                                           timeout=5)
            
            if msg:
                mission_items.append(msg)

        return mission_items