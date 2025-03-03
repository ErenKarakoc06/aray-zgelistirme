from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                          QLabel, QComboBox, QGroupBox, QLineEdit, QSpinBox,
                          QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QUrl
import folium
import io
import sys
import os
from datetime import datetime

class MapView(QWidget):
    waypoint_updated = pyqtSignal(dict)
    mission_updated = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.current_time_utc = "2025-03-02 20:09:36"
        self.current_user = "ErenKarakoc06"
        self.waypoints = []
        self.home_position = {"lat": 39.925018, "lon": 32.836956, "alt": 0}
        self.map_file = "temp_map.html"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Üst bilgi paneli
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel(f"Kullanıcı: {self.current_user}"))
        info_layout.addWidget(QLabel(f"UTC: {self.current_time_utc}"))
        layout.addLayout(info_layout)

        # Ana düzen
        main_layout = QHBoxLayout()

        # Harita Kontrolleri - Sol Panel
        left_panel = QGroupBox("Harita Kontrolleri")
        left_layout = QVBoxLayout()

        # Harita tipi seçimi
        map_type_layout = QHBoxLayout()
        map_type_layout.addWidget(QLabel("Harita Tipi:"))
        self.map_type_combo = QComboBox()
        self.map_type_combo.addItems(["OpenStreetMap", "Satellite", "Terrain"])
        self.map_type_combo.currentTextChanged.connect(self.change_map_type)
        map_type_layout.addWidget(self.map_type_combo)
        left_layout.addLayout(map_type_layout)

        # Koordinat girişi
        coord_group = QGroupBox("Koordinat Ekle")
        coord_layout = QVBoxLayout()
        
        lat_layout = QHBoxLayout()
        lat_layout.addWidget(QLabel("Enlem:"))
        self.lat_input = QLineEdit()
        lat_layout.addWidget(self.lat_input)
        coord_layout.addLayout(lat_layout)
        
        lon_layout = QHBoxLayout()
        lon_layout.addWidget(QLabel("Boylam:"))
        self.lon_input = QLineEdit()
        lon_layout.addWidget(self.lon_input)
        coord_layout.addLayout(lon_layout)
        
        alt_layout = QHBoxLayout()
        alt_layout.addWidget(QLabel("Yükseklik (m):"))
        self.alt_input = QSpinBox()
        self.alt_input.setRange(0, 10000)
        alt_layout.addWidget(self.alt_input)
        coord_layout.addLayout(alt_layout)
        
        coord_group.setLayout(coord_layout)
        left_layout.addWidget(coord_group)

        # Waypoint kontrolleri
        wp_btn_layout = QHBoxLayout()
        add_wp_btn = QPushButton("Waypoint Ekle")
        add_wp_btn.clicked.connect(self.add_waypoint)
        clear_wp_btn = QPushButton("Temizle")
        clear_wp_btn.clicked.connect(self.clear_waypoints)
        wp_btn_layout.addWidget(add_wp_btn)
        wp_btn_layout.addWidget(clear_wp_btn)
        left_layout.addLayout(wp_btn_layout)

        left_panel.setLayout(left_layout)
        main_layout.addWidget(left_panel)

        # Harita Görünümü - Orta Panel
        map_group = QGroupBox("Harita")
        map_layout = QVBoxLayout()
        self.create_map()
        map_group.setLayout(map_layout)
        main_layout.addWidget(map_group, stretch=2)

        # Görev Kontrolleri - Sağ Panel
        right_panel = QGroupBox("Görev Kontrolleri")
        right_layout = QVBoxLayout()

        # Araç durumu
        status_group = QGroupBox("Araç Durumu")
        status_layout = QVBoxLayout()
        self.vehicle_status = QLabel("Bağlı Değil")
        self.vehicle_position = QLabel("Konum: --")
        self.vehicle_altitude = QLabel("Yükseklik: --")
        self.vehicle_heading = QLabel("Yön: --")
        status_layout.addWidget(self.vehicle_status)
        status_layout.addWidget(self.vehicle_position)
        status_layout.addWidget(self.vehicle_altitude)
        status_layout.addWidget(self.vehicle_heading)
        status_group.setLayout(status_layout)
        right_layout.addWidget(status_group)

        # Görev butonları
        mission_btn_layout = QVBoxLayout()
        upload_btn = QPushButton("Görevi Yükle")
        upload_btn.clicked.connect(self.upload_mission)
        download_btn = QPushButton("Görevi İndir")
        download_btn.clicked.connect(self.download_mission)
        start_mission_btn = QPushButton("Görevi Başlat")
        start_mission_btn.clicked.connect(self.start_mission)
        rtl_btn = QPushButton("RTL")
        rtl_btn.clicked.connect(self.return_to_launch)
        
        mission_btn_layout.addWidget(upload_btn)
        mission_btn_layout.addWidget(download_btn)
        mission_btn_layout.addWidget(start_mission_btn)
        mission_btn_layout.addWidget(rtl_btn)
        right_layout.addLayout(mission_btn_layout)

        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel)

        layout.addLayout(main_layout)
        self.setLayout(layout)

    def create_map(self):
        """Folium haritası oluştur"""
        m = folium.Map(
            location=[self.home_position["lat"], self.home_position["lon"]],
            zoom_start=13
        )

        # Home pozisyonunu ekle
        folium.Marker(
            [self.home_position["lat"], self.home_position["lon"]],
            popup="Home Position",
            icon=folium.Icon(color='red', icon='home')
        ).add_to(m)

        # Waypointleri ekle
        for i, wp in enumerate(self.waypoints):
            folium.Marker(
                [wp["lat"], wp["lon"]],
                popup=f'WP {i+1} (Alt: {wp["alt"]}m)',
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)

        # Waypoint rotasını çiz
        if len(self.waypoints) > 0:
            points = [[wp["lat"], wp["lon"]] for wp in self.waypoints]
            folium.PolyLine(points, weight=2, color='red').add_to(m)

        # Haritayı HTML olarak kaydet
        m.save(self.map_file)

    def change_map_type(self, map_type):
        """Harita tipini değiştir"""
        if map_type == "Satellite":
            tiles = "Stamen Terrain"
        elif map_type == "Terrain":
            tiles = "Stamen Terrain"
        else:
            tiles = "OpenStreetMap"
            
        self.create_map()  # Haritayı yeniden oluştur

    def add_waypoint(self):
        """Yeni waypoint ekle"""
        try:
            lat = float(self.lat_input.text())
            lon = float(self.lon_input.text())
            alt = self.alt_input.value()
            
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                waypoint = {
                    "lat": lat,
                    "lon": lon,
                    "alt": alt
                }
                self.waypoints.append(waypoint)
                self.create_map()  # Haritayı güncelle
                self.waypoint_updated.emit(waypoint)
            else:
                print("Geçersiz koordinat değerleri!")
                
        except ValueError:
            print("Geçersiz koordinat formatı!")

    def clear_waypoints(self):
        """Tüm waypointleri temizle"""
        self.waypoints = []
        self.create_map()
        self.mission_updated.emit([])

    def upload_mission(self):
        """Görevi araca yükle"""
        print("Görev yükleniyor...")
        # TODO: MAVLink ile görevi araca yükle

    def download_mission(self):
        """Aracın mevcut görevini indir"""
        print("Görev indiriliyor...")
        # TODO: MAVLink ile aracın görevini al

    def start_mission(self):
        """Görevi başlat"""
        print("Görev başlatılıyor...")
        # TODO: MAVLink ile görevi başlat

    def return_to_launch(self):
        """RTL modunu aktifleştir"""
        print("RTL modu aktifleştiriliyor...")
        # TODO: MAVLink ile RTL komutunu gönder
