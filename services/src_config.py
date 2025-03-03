import os
from pathlib import Path

# Proje kök dizini
ROOT_DIR = Path(__file__).parent.parent

# QFlightinstruments lib dizini
QFI_LIB_DIR = ROOT_DIR / 'libs' / 'QFlightinstruments'

# Varsayılan harita merkezi (Ankara)
DEFAULT_LAT = 39.925533
DEFAULT_LON = 32.866287

# Mavlink bağlantı ayarları
DEFAULT_CONNECTION_TYPE = 'udp'
DEFAULT_PORT = 14550
DEFAULT_BAUD = 57600

# Arayüz ayarları
WINDOW_TITLE = "Drone Ground Control Station"
UPDATE_RATE = 50  # ms
MAP_UPDATE_RATE = 100  # ms

# Görev planlama ayarları
DEFAULT_ALTITUDE = 50  # metre
MIN_WAYPOINT_DISTANCE = 5  # metre