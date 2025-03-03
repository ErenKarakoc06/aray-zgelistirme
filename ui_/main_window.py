from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QDockWidget, QTabWidget, QLabel, QPushButton,
                             QComboBox, QStatusBar, QToolBar, QMenuBar,
                             QGraphicsView, QGraphicsScene, QStackedWidget)
from PyQt6.QtCore import Qt, pyqtSignal, QRectF, QPointF, QTimer
from PyQt6.QtGui import QAction, QIcon, QPainter, QPen, QColor, QBrush
from datetime import datetime
import sys
import os

# Yerel modülleri import et
from ui.map_widget import MapWidget
from ui.instruments.flight_instruments import FlightInstrumentsWidget
from ui.instruments.telemetry import TelemetryManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_time_utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.current_user = "ErenKarakoc06"
        self.setWindowTitle("Drone Ground Control Station")

        # Telemetri yöneticisi
        self.telemetry_manager = TelemetryManager()

        # Timer kurulumu
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Her saniye güncelle

        self.init_ui()

    def update_time(self):
        self.current_time_utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.statusBar().showMessage(
            f'Bağlı Değil | {self.current_time_utc} | {self.current_user}'
        )

    def init_ui(self):
        # Ana widget ve layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Sol panel (Flight Instruments + Kontroller)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # Flight Instruments
        self.instruments = FlightInstrumentsWidget()
        left_layout.addWidget(self.instruments)

        # Kontrol paneli
        control_panel = self.create_control_panel()
        left_layout.addWidget(control_panel)

        # Telemetri göstergeleri
        telemetry_panel = self.create_telemetry_panel()
        left_layout.addWidget(telemetry_panel)

        left_panel.setFixedWidth(450)  # Sol panel genişliği
        main_layout.addWidget(left_panel)

        # Orta panel (Harita/Görev Planlama)
        center_panel = self.create_center_panel()
        main_layout.addWidget(center_panel)

        # Menü, toolbar ve status bar
        self.create_menu_bar()
        self.create_toolbar()
        self.create_status_bar()

        # Telemetri sinyallerini bağla
        self.telemetry_manager.attitude_data.connect(self.update_attitude)
        self.telemetry_manager.position_data.connect(self.update_position)
        self.telemetry_manager.system_status.connect(self.update_status)

        # Pencereyi maximize et
        self.showMaximized()

    def create_control_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()

        # Mod seçici
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Uçuş Modu:"))
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(['GUIDED', 'AUTO', 'LOITER', 'RTL', 'LAND'])
        mode_layout.addWidget(self.mode_selector)
        layout.addLayout(mode_layout)

        # ARM/DISARM butonu
        self.arm_btn = QPushButton("ARM")
        self.arm_btn.setCheckable(True)
        layout.addWidget(self.arm_btn)

        # Görev kontrol butonları
        mission_layout = QHBoxLayout()
        self.start_mission_btn = QPushButton("Başlat")
        self.pause_mission_btn = QPushButton("Duraklat")
        self.stop_mission_btn = QPushButton("Durdur")

        mission_layout.addWidget(self.start_mission_btn)
        mission_layout.addWidget(self.pause_mission_btn)
        mission_layout.addWidget(self.stop_mission_btn)
        layout.addLayout(mission_layout)

        panel.setLayout(layout)
        return panel

    def create_telemetry_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()

        # Telemetri etiketleri
        self.alt_label = QLabel("Yükseklik: 0 m")
        self.speed_label = QLabel("Hız: 0 m/s")
        self.heading_label = QLabel("Yön: 0°")
        self.gps_label = QLabel("GPS: 0 Uydu")
        self.battery_label = QLabel("Batarya: 0%")

        layout.addWidget(self.alt_label)
        layout.addWidget(self.speed_label)
        layout.addWidget(self.heading_label)
        layout.addWidget(self.gps_label)
        layout.addWidget(self.battery_label)

        panel.setLayout(layout)
        return panel

    def create_center_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Tab butonları
        tab_layout = QHBoxLayout()
        self.map_btn = QPushButton("Harita")
        self.mission_btn = QPushButton("Görev")
        self.map_btn.setCheckable(True)
        self.mission_btn.setCheckable(True)
        self.map_btn.setChecked(True)

        tab_layout.addWidget(self.map_btn)
        tab_layout.addWidget(self.mission_btn)
        tab_layout.addStretch()
        layout.addLayout(tab_layout)

        # Stacked widget for map and mission views
        self.stack = QStackedWidget()
        self.map_widget = MapWidget()
        self.mission_widget = QWidget()  # Bu sınıfı daha sonra implement edeceğiz

        self.stack.addWidget(self.map_widget)
        self.stack.addWidget(self.mission_widget)
        layout.addWidget(self.stack)

        # Tab buton bağlantıları
        self.map_btn.clicked.connect(lambda: self.change_tab(0))
        self.mission_btn.clicked.connect(lambda: self.change_tab(1))

        return panel

    def change_tab(self, index):
        self.stack.setCurrentIndex(index)
        self.map_btn.setChecked(index == 0)
        self.mission_btn.setChecked(index == 1)

    def create_menu_bar(self):
        menubar = self.menuBar()

        # Dosya menüsü
        file_menu = menubar.addMenu('Dosya')
        file_menu.addAction('Görev Yükle')
        file_menu.addAction('Görevi Kaydet')
        file_menu.addSeparator()
        file_menu.addAction('Parametreleri Yükle')
        file_menu.addAction('Parametreleri Kaydet')
        file_menu.addSeparator()
        file_menu.addAction('Çıkış')

        # Bağlantı menüsü
        conn_menu = menubar.addMenu('Bağlantı')
        conn_menu.addAction('Bağlan')
        conn_menu.addAction('Bağlantıyı Kes')
        conn_menu.addSeparator()
        conn_menu.addAction('Bağlantı Ayarları')

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Bağlantı ayarları
        self.conn_type = QComboBox()
        self.conn_type.addItems(['UDP', 'TCP', 'Serial'])
        toolbar.addWidget(self.conn_type)

        self.port = QComboBox()
        self.port.addItems(['14550', '14551', 'COM1', 'COM2'])
        toolbar.addWidget(self.port)

        self.connect_btn = QPushButton('Bağlan')
        toolbar.addWidget(self.connect_btn)

    def create_status_bar(self):
        self.statusBar().showMessage(
            f'Bağlı Değil | {self.current_time_utc} | {self.current_user}'
        )

    def update_attitude(self, data):
        self.instruments.update_instruments(data)

    def update_position(self, data):
        self.alt_label.setText(f"Yükseklik: {data['alt']:.1f} m")
        self.heading_label.setText(f"Yön: {data['heading']:.1f}°")
        self.map_widget.update_drone_position(data['lat'], data['lon'], data['heading'])

    def update_status(self, data):
        if 'battery' in data:
            self.battery_label.setText(f"Batarya: {data['battery']}%")
        if 'satellites' in data:
            self.gps_label.setText(f"GPS: {data['satellites']} Uydu")