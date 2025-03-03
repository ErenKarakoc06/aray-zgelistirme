from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QProgressBar, QComboBox)
from PyQt6.QtCore import pyqtSignal

class CalibrationTools(QWidget):
    calibration_started = pyqtSignal(str)  # calibration type
    calibration_stopped = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Kalibrasyon tipi seçimi
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Kalibrasyon Tipi:"))
        self.cal_type = QComboBox()
        self.cal_type.addItems(["Pusula", "İvmeölçer", "Gyro", "Seviye"])
        type_layout.addWidget(self.cal_type)
        layout.addLayout(type_layout)
        
        # Durum göstergesi
        self.status_label = QLabel("Hazır")
        layout.addWidget(self.status_label)
        
        # İlerleme çubuğu
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        
        # Kontrol butonları
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Başlat")
        self.start_btn.clicked.connect(self.start_calibration)
        self.stop_btn = QPushButton("Durdur")
        self.stop_btn.clicked.connect(self.stop_calibration)
        
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)
        
        # Talimatlar
        self.instructions = QLabel()
        self.instructions.setWordWrap(True)
        layout.addWidget(self.instructions)
        
        self.setLayout(layout)
        
    def start_calibration(self):
        cal_type = self.cal_type.currentText()
        self.status_label.setText(f"{cal_type} kalibrasyonu başlatılıyor...")
        self.calibration_started.emit(cal_type)
        
        # Kalibrasyon tipine göre talimatları güncelle
        instructions = {
            "Pusula": "Aracı her eksende 360 derece döndürün.",
            "İvmeölçer": "Aracı her yüzü üzerinde tutun.",
            "Gyro": "Aracı sabit tutun.",
            "Seviye": "Aracı düz bir yüzeye yerleştirin."
        }
        self.instructions.setText(instructions[cal_type])
        
    def stop_calibration(self):
        self.status_label.setText("Kalibrasyon durduruldu")
        self.calibration_stopped.emit()
        
    def update_progress(self, value):
        self.progress.setValue(value)
        
    def update_status(self, status):
        self.status_label.setText(status)