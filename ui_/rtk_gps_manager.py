from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                          QLabel, QTableWidget, QTableWidgetItem, QGroupBox,
                          QLineEdit, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
import time
from datetime import datetime

class RTKGPSManager(QWidget):
    gps_status = pyqtSignal(str, bool)  # status_message, success

    def __init__(self):
        super().__init__()
        self.current_time_utc = "2025-03-02 19:48:01"
        self.current_user = "ErenKarakoc06"
        self.init_ui()
        self.start_gps_update()

    def init_ui(self):
        layout = QVBoxLayout()

        # Üst bilgi paneli
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel(f"Kullanıcı: {self.current_user}"))
        info_layout.addWidget(QLabel(f"UTC: {self.current_time_utc}"))
        layout.addLayout(info_layout)

        # RTK Ayarları
        settings_group = QGroupBox("RTK GPS Ayarları")
        settings_layout = QVBoxLayout()

        # NTRIP Sunucu Ayarları
        server_layout = QHBoxLayout()
        server_layout.addWidget(QLabel("NTRIP Sunucu:"))
        self.server_input = QLineEdit("rtk.gazi.edu.tr")
        server_layout.addWidget(self.server_input)
        server_layout.addWidget(QLabel("Port:"))
        self.port_input = QLineEdit("2101")
        server_layout.addWidget(self.port_input)
        settings_layout.addLayout(server_layout)

        # Kullanıcı bilgileri
        auth_layout = QHBoxLayout()
        auth_layout.addWidget(QLabel("Kullanıcı Adı:"))
        self.username_input = QLineEdit()
        auth_layout.addWidget(self.username_input)
        auth_layout.addWidget(QLabel("Şifre:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        auth_layout.addWidget(self.password_input)
        settings_layout.addLayout(auth_layout)

        # Mount point seçimi
        mount_layout = QHBoxLayout()
        mount_layout.addWidget(QLabel("Mount Point:"))
        self.mount_select = QComboBox()
        self.mount_select.addItems(["RTCM3", "CMR", "CMR+"])
        mount_layout.addWidget(self.mount_select)
        settings_layout.addLayout(mount_layout)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # Konum Bilgileri
        position_group = QGroupBox("GPS Konum Bilgileri")
        position_layout = QVBoxLayout()

        self.position_table = QTableWidget(3, 2)
        self.position_table.setHorizontalHeaderLabels(["Parametre", "Değer"])
        self.position_table.setVerticalHeaderLabels(["Enlem", "Boylam", "Yükseklik"])
        self.position_table.horizontalHeader().setStretchLastSection(True)
        position_layout.addWidget(self.position_table)

        position_group.setLayout(position_layout)
        layout.addWidget(position_group)

        # RTK Durum Bilgileri
        status_group = QGroupBox("RTK Durum")
        status_layout = QVBoxLayout()

        self.status_table = QTableWidget(4, 2)
        self.status_table.setHorizontalHeaderLabels(["Parametre", "Değer"])
        self.status_table.setVerticalHeaderLabels(["Bağlantı", "Fix Tipi", "Uydu Sayısı", "HDOP"])
        self.status_table.horizontalHeader().setStretchLastSection(True)
        status_layout.addWidget(self.status_table)

        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        # Kontrol butonları
        btn_layout = QHBoxLayout()
        
        self.connect_btn = QPushButton("Bağlan")
        self.connect_btn.clicked.connect(self.connect_rtk)
        btn_layout.addWidget(self.connect_btn)
        
        self.disconnect_btn = QPushButton("Bağlantıyı Kes")
        self.disconnect_btn.clicked.connect(self.disconnect_rtk)
        self.disconnect_btn.setEnabled(False)
        btn_layout.addWidget(self.disconnect_btn)
        
        layout.addLayout(btn_layout)

        # Durum bildirimi
        self.status_label = QLabel("Hazır")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def start_gps_update(self):
        self.gps_timer = QTimer()
        self.gps_timer.timeout.connect(self.update_gps_data)
        self.gps_timer.start(1000)  # Her saniye güncelle

    def update_gps_data(self):
        try:
            # Simüle edilmiş GPS verileri
            lat = 39.925018
            lon = 32.836956
            alt = 938.5
            
            # Konum tablosunu güncelle
            self.position_table.setItem(0, 1, QTableWidgetItem(f"{lat:.6f}°"))
            self.position_table.setItem(1, 1, QTableWidgetItem(f"{lon:.6f}°"))
            self.position_table.setItem(2, 1, QTableWidgetItem(f"{alt:.2f}m"))

            # Simüle edilmiş RTK durumu
            self.status_table.setItem(0, 1, QTableWidgetItem("Bağlı"))
            self.status_table.setItem(1, 1, QTableWidgetItem("RTK Fixed"))
            self.status_table.setItem(2, 1, QTableWidgetItem("12"))
            self.status_table.setItem(3, 1, QTableWidgetItem("0.8"))

        except Exception as e:
            self.status_label.setText(f"Veri güncelleme hatası: {str(e)}")
            self.gps_status.emit("GPS veri hatası", False)

    def connect_rtk(self):
        server = self.server_input.text()
        port = self.port_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        mount = self.mount_select.currentText()

        if not all([server, port, username, password]):
            QMessageBox.warning(self, "Uyarı", "Tüm alanları doldurun!")
            return

        try:
            # TODO: RTK bağlantı işlemleri
            self.status_label.setText("RTK bağlantısı kuruluyor...")
            time.sleep(2)  # Simüle edilmiş bağlantı gecikmesi
            
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
            self.status_label.setText("RTK bağlantısı kuruldu")
            self.gps_status.emit("RTK bağlantısı başarılı", True)

        except Exception as e:
            self.status_label.setText(f"Bağlantı hatası: {str(e)}")
            self.gps_status.emit(f"RTK bağlantı hatası: {str(e)}", False)

    def disconnect_rtk(self):
        try:
            # TODO: RTK bağlantı kesme işlemleri
            self.status_label.setText("RTK bağlantısı kesiliyor...")
            time.sleep(1)  # Simüle edilmiş bağlantı kesme gecikmesi
            
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
            self.status_label.setText("RTK bağlantısı kesildi")
            self.gps_status.emit("RTK bağlantısı kesildi", True)

        except Exception as e:
            self.status_label.setText(f"Bağlantı kesme hatası: {str(e)}")
            self.gps_status.emit(f"RTK bağlantı kesme hatası: {str(e)}", False)

    def closeEvent(self, event):
        if hasattr(self, 'gps_timer'):
            self.gps_timer.stop()
        event.accept()