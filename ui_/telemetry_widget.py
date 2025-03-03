from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel
from PyQt6.QtCore import pyqtSignal, QTimer
from instruments import QFI_ADI, QFI_ALT, QFI_ASI, QFI_HSI, QFI_VSI

class TelemetryWidget(QWidget):
    telemetry_updated = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Test için timer
        self.test_timer = QTimer()
        self.test_timer.timeout.connect(self.update_test_data)
        self.test_timer.start(100)  # 10 Hz güncelleme

    def init_ui(self):
        layout = QGridLayout()
        
        # Uçuş enstrümanları
        self.adi = QFI_ADI(self)
        self.alt = QFI_ALT(self)
        self.asi = QFI_ASI(self)
        self.hsi = QFI_HSI(self)
        self.vsi = QFI_VSI(self)
        
        # Sol panel - Enstrümanlar
        layout.addWidget(self.adi, 0, 0)
        layout.addWidget(self.alt, 1, 0)
        layout.addWidget(self.asi, 2, 0)
        layout.addWidget(self.hsi, 3, 0)
        layout.addWidget(self.vsi, 4, 0)
        
        # Sağ panel - Sayısal veriler
        self.data_labels = {
            'altitude': QLabel('Yükseklik: 0 m'),
            'airspeed': QLabel('Hız: 0 m/s'),
            'groundspeed': QLabel('Yer Hızı: 0 m/s'),
            'climb': QLabel('Tırmanma: 0 m/s'),
            'heading': QLabel('Yön: 0°'),
            'roll': QLabel('Roll: 0°'),
            'pitch': QLabel('Pitch: 0°'),
            'battery': QLabel('Batarya: 0%'),
            'gps': QLabel('GPS: 0 uydu'),
            'mode': QLabel('Mod: --'),
            'armed': QLabel('Durum: Pasif')
        }
        
        row = 0
        for label in self.data_labels.values():
            layout.addWidget(label, row, 1)
            row += 1
        
        self.setLayout(layout)

    def update_test_data(self):
        # Test verileri
        import math
        import time
        
        t = time.time()
        
        test_data = {
            'roll': 30 * math.sin(t),
            'pitch': 20 * math.cos(t),
            'heading': (t * 10) % 360,
            'altitude': 1000 + 100 * math.sin(t/5),
            'airspeed': 50 + 10 * math.sin(t/3),
            'groundspeed': 45 + 5 * math.sin(t/3),
            'climb': 2 * math.cos(t),
            'battery': 75 + 5 * math.sin(t/10),
            'gps_satellites': 8,
            'mode': 'GUIDED',
            'armed': True
        }
        
        self.update_telemetry(test_data)

    def update_telemetry(self, data):
        # Enstrümanları güncelle
        if 'roll' in data:
            self.adi.setRoll(data['roll'])
        if 'pitch' in data:
            self.adi.setPitch(data['pitch'])
        if 'altitude' in data:
            self.alt.setAltitude(data['altitude'])
        if 'airspeed' in data:
            self.asi.setAirspeed(data['airspeed'])
        if 'heading' in data:
            self.hsi.setHeading(data['heading'])
        if 'climb' in data:
            self.vsi.setClimbRate(data['climb'])
        
        # Label'ları güncelle
        self.data_labels['altitude'].setText(f"Yükseklik: {data.get('altitude', 0):.1f} m")
        self.data_labels['airspeed'].setText(f"Hız: {data.get('airspeed', 0):.1f} m/s")
        self.data_labels['groundspeed'].setText(f"Yer Hızı: {data.get('groundspeed', 0):.1f} m/s")
        self.data_labels['climb'].setText(f"Tırmanma: {data.get('climb', 0):.1f} m/s")
        self.data_labels['heading'].setText(f"Yön: {data.get('heading', 0):.1f}°")
        self.data_labels['roll'].setText(f"Roll: {data.get('roll', 0):.1f}°")
        self.data_labels['pitch'].setText(f"Pitch: {data.get('pitch', 0):.1f}°")
        self.data_labels['battery'].setText(f"Batarya: {data.get('battery', 0):.0f}%")
        self.data_labels['gps'].setText(f"GPS: {data.get('gps_satellites', 0)} uydu") ▋