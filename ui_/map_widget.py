from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, pyqtSignal, Qt
from datetime import datetime
import json

class MapWidget(QWidget):
    waypoint_added = pyqtSignal(float, float, float)  # lat, lon, alt
    waypoint_removed = pyqtSignal(int)  # waypoint index
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.web_view = QWebEngineView()
        
        # HTML içeriği
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Drone Map</title>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"/>
            <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
            <style>
                #map { height: 100vh; width: 100%; }
                .info-box {
                    padding: 6px 8px;
                    font: 14px/16px Arial, Helvetica, sans-serif;
                    background: white;
                    background: rgba(255,255,255,0.8);
                    box-shadow: 0 0 15px rgba(0,0,0,0.2);
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                // Harita başlatma
                var map = L.map('map').setView([39.925533, 32.866287], 13);
                
                // OpenStreetMap katmanı
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors'
                }).addTo(map);
                
                // Drone marker'ı
                var droneIcon = L.divIcon({
                    className: 'drone-icon',
                    html: '🛩️',
                    iconSize: [25, 25],
                    iconAnchor: [12, 12]
                });
                
                var droneMarker = L.marker([39.925533, 32.866287], {
                    icon: droneIcon,
                    rotationAngle: 0
                }).addTo(map);
                
                // Waypoint yönetimi
                var waypoints = [];
                var waypointLayer = L.layerGroup().addTo(map);
                var missionPath = L.polyline([], {color: 'blue', weight: 2}).addTo(map);
                
                // Bilgi kutusu
                var info = L.control();
                info.onAdd = function(map) {
                    this._div = L.DomUtil.create('div', 'info-box');
                    this.update();
                    return this._div;
                };
                
                info.update = function(data) {
                    data = data || {};
                    this._div.innerHTML = `
                        <h4>Drone Bilgileri</h4>
                        <p>Yükseklik: ${data.altitude || 0} m</p>
                        <p>Hız: ${data.speed || 0} m/s</p>
                        <p>Heading: ${data.heading || 0}°</p>
                    `;
                };
                info.addTo(map);
                
                // JavaScript fonksiyonları
                function updateDronePosition(lat, lon, heading) {
                    droneMarker.setLatLng([lat, lon]);
                    droneMarker.setRotationAngle(heading);
                    map.panTo([lat, lon]);
                }
                
                function addWaypoint(lat, lon, alt) {
                    var marker = L.marker([lat, lon], {
                        draggable: true
                    });
                    
                    marker.altitude = alt;
                    marker.bindPopup(`Waypoint ${waypoints.length + 1}<br>Alt: ${alt}m`);
                    
                    marker.on('dragend', function(e) {
                        updateMissionPath();
                    });
                    
                    waypoints.push(marker);
                    waypointLayer.addLayer(marker);
                    updateMissionPath();
                }
                
                function removeWaypoint(index) {
                    if (index >= 0 && index < waypoints.length) {
                        waypointLayer.removeLayer(waypoints[index]);
                        waypoints.splice(index, 1);
                        updateMissionPath();
                    }
                }
                
                function updateMissionPath() {
                    var points = waypoints.map(w => w.getLatLng());
                    missionPath.setLatLngs(points);
                }
                
                function clearWaypoints() {
                    waypoints.forEach(w => waypointLayer.removeLayer(w));
                    waypoints = [];
                    missionPath.setLatLngs([]);
                }
                
                function updateTelemetry(data) {
                    info.update(data);
                }
                
                // Harita tıklama olayı
                var planningMode = false;
                map.on('click', function(e) {
                    if (planningMode) {
                        addWaypoint(e.latlng.lat, e.latlng.lng, 50);
                    }
                });
                
                function setPlanningMode(enabled) {
                    planningMode = enabled;
                }
            </script>
        </body>
        </html>
        """
        
        self.web_view.setHtml(html_content)
        layout.addWidget(self.web_view)
        self.setLayout(layout)
        
    def update_drone_position(self, lat, lon, heading=0):
        js = f"updateDronePosition({lat}, {lon}, {heading});"
        self.web_view.page().runJavaScript(js)
        
    def add_waypoint(self, lat, lon, alt=50):
        js = f"addWaypoint({lat}, {lon}, {alt});"
        self.web_view.page().runJavaScript(js)
        
    def remove_waypoint(self, index):
        js = f"removeWaypoint({index});"
        self.web_view.page().runJavaScript(js)
        
    def clear_waypoints(self):
        self.web_view.page().runJavaScript("clearWaypoints();")
        
    def update_telemetry(self, data):
        js = f"updateTelemetry({json.dumps(data)});"
        self.web_view.page().runJavaScript(js)
        
    def set_planning_mode(self, enabled):
        js = f"setPlanningMode({str(enabled).lower()});"
        self.web_view.page().runJavaScript(js)