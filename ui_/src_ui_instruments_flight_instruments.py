from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
import sys
import os

# QFlightinstruments kütüphanesini import et
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../libs/QFlightinstruments'))
from qfi import qfi_ADI, qfi_ALT, qfi_ASI, qfi_HSI, qfi_VSI

class FlightInstrumentsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Üst sıra - ADI ve HSI
        top_row = QHBoxLayout()
        
        # Artificial Horizon (ADI)
        self.adi = qfi_ADI.qfi_ADI(self)
        self.adi.setFixedSize(200, 200)
        adi_container = QWidget()
        adi_layout = QVBoxLayout()
        adi_layout.addWidget(self.adi)
        adi_layout.addWidget(QLabel("Artificial Horizon"))
        adi_container.setLayout(adi_layout)
        top_row.addWidget(adi_container)
        
        # Heading Indicator (HSI)
        self.hsi = qfi_HSI.qfi_HSI(self)
        self.hsi.setFixedSize(200, 200)
        hsi_container = QWidget()
        hsi_layout = QVBoxLayout()
        hsi_layout.addWidget(self.hsi)
        hsi_layout.addWidget(QLabel("Heading"))
        hsi_container.setLayout(hsi_layout)
        top_row.addWidget(hsi_container)
        
        main_layout.addLayout(top_row)
        
        # Alt sıra - ASI, ALT ve VSI
        bottom_row = QHBoxLayout()
        
        # Airspeed Indicator (ASI)
        self.asi = qfi_ASI.qfi_ASI(self)
        self.asi.setFixedSize(200, 200)
        asi_container = QWidget()
        asi_layout = QVBoxLayout()
        asi_layout.addWidget(self.asi)
        asi_layout.addWidget(QLabel("Airspeed"))
        asi_container.setLayout(asi_layout)
        bottom_row.addWidget(asi_container)
        
        # Altimeter (ALT)
        self.alt = qfi_ALT.qfi_ALT(self)
        self.alt.setFixedSize(200, 200)
        alt_container = QWidget()
        alt_layout = QVBoxLayout()
        alt_layout.addWidget(self.alt)
        alt_layout.addWidget(QLabel("Altitude"))
        alt_container.setLayout(alt_layout)
        bottom_row.addWidget(alt_container)
        
        # Vertical Speed Indicator (VSI)
        self.vsi = qfi_VSI.qfi_VSI(self)
        self.vsi.setFixedSize(200, 200)
        vsi_container = QWidget()
        vsi_layout = QVBoxLayout()
        vsi_layout.addWidget(self.vsi)
        vsi_layout.addWidget(QLabel("Vertical Speed"))
        vsi_container.setLayout(vsi_layout)
        bottom_row.addWidget(vsi_container)
        
        main_layout.addLayout(bottom_row)
        self.setLayout(main_layout)
        
    def update_instruments(self, data):
        """Tüm göstergeleri güncelle"""
        # Roll ve Pitch
        self.adi.setRoll(data.get('roll', 0))
        self.adi.setPitch(data.get('pitch', 0))
        
        # Heading
        self.hsi.setHeading(data.get('heading', 0))
        
        # Airspeed
        self.asi.setAirspeed(data.get('airspeed', 0))
        
        # Altitude
        self.alt.setAltitude(data.get('altitude', 0))
        self.alt.setPressure(data.get('pressure', 29.92))
        
        # Vertical Speed
        self.vsi.setClimbRate(data.get('vertical_speed', 0))