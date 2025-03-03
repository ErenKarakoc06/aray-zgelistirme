from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                          QLabel, QSpinBox, QComboBox, QTabWidget, QGroupBox,
                          QCheckBox, QColorDialog, QSlider, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPen
import json
import os

class HUDLayoutEditor(QWidget):
    layout_changed = pyqtSignal(dict)

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.dragging = False
        self.selected_element = None
        self.elements = {
            'artificial_horizon': {'x': 150, 'y': 150, 'size': 200},
            'altitude': {'x': 50, 'y': 100, 'size': 100},
            'speed': {'x': 250, 'y': 100, 'size': 100},
            'heading': {'x': 150, 'y': 50, 'size': 100},
            'battery': {'x': 50, 'y': 200, 'size': 80},
            'gps': {'x': 250, 'y': 200, 'size': 80}
        }
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(400, 300)
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Arka plan
        painter.fillRect(self.rect(), QColor(40, 40, 40))

        # Elementleri çiz
        for name, props in self.elements.items():
            color = QColor(255, 255, 255) if name != self.selected_element else QColor(0, 255, 0)
            pen = QPen(color)
            painter.setPen(pen)

            x, y = props['x'], props['y']
            size = props['size']
            
            # Element tipine göre çizim
            if name == 'artificial_horizon':
                painter.drawEllipse(x - size//2, y - size//2, size, size)
            elif name in ['altitude', 'speed']:
                painter.drawRect(x - size//4, y - size//2, size//2, size)
            elif name == 'heading':
                painter.drawRect(x - size//2, y - size//4, size, size//2)
            else:  # battery ve gps için
                painter.drawRect(x - size//2, y - size//2, size, size)

            # Element adını yaz
            painter.drawText(x - size//2, y + size//2 + 15, name)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            for name, props in self.elements.items():
                if self.is_point_in_element(event.pos().x(), event.pos().y(), props):
                    self.dragging = True
                    self.selected_element = name
                    self.update()
                    break

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.layout_changed.emit(self.elements)

    def mouseMoveEvent(self, event):
        if self.dragging and self.selected_element:
            self.elements[self.selected_element]['x'] = event.pos().x()
            self.elements[self.selected_element]['y'] = event.pos().y()
            self.update()

    def is_point_in_element(self, x, y, props):
        ex, ey = props['x'], props['y']
        size = props['size']
        return (x - ex) ** 2 + (y - ey) ** 2 <= (size/2) ** 2

class HUDCustomization(QWidget):
    settings_updated = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.current_time_utc = "2025-03-02 19:53:49"
        self.current_user = "ErenKarakoc06"
        
        # Varsayılan HUD ayarları
        self.hud_settings = {
            'colors': {
                'background': '#000000',
                'text': '#FFFFFF',
                'horizon': '#00FF00',
                'warning': '#FF0000'
            },
            'size': {
                'text': 12,
                'icons': 24,
                'horizon': 200
            },
            'elements': {
                'artificial_horizon': True,
                'altitude': True,
                'speed': True,
                'heading': True,
                'battery': True,
                'gps': True
            },
            'opacity': 0.8,
            'refresh_rate': 30
        }
        
        self.load_settings()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Üst bilgi paneli
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel(f"Kullanıcı: {self.current_user}"))
        info_layout.addWidget(QLabel(f"UTC: {self.current_time_utc}"))
        layout.addLayout(info_layout)

        # Sekmeler
        tabs = QTabWidget()
        tabs.addTab(self.create_colors_tab(), "Renkler")
        tabs.addTab(self.create_elements_tab(), "Elementler")
        tabs.addTab(self.create_layout_tab(), "Yerleşim")
        tabs.addTab(self.create_performance_tab(), "Performans")
        layout.addWidget(tabs)

        # Kaydet/İptal butonları
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("Kaydet")
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("Varsayılana Dön")
        reset_btn.clicked.connect(self.reset_settings)
        btn_layout.addWidget(reset_btn)
        
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def create_colors_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        colors_group = QGroupBox("Renk Ayarları")
        colors_layout = QVBoxLayout()

        for name, color in self.hud_settings['colors'].items():
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{name.capitalize()}:"))
            
            color_btn = QPushButton()
            color_btn.setStyleSheet(f"background-color: {color};")
            color_btn.setFixedSize(50, 25)
            color_btn.clicked.connect(lambda checked, n=name: self.choose_color(n))
            row.addWidget(color_btn)
            
            colors_layout.addLayout(row)

        colors_group.setLayout(colors_layout)
        layout.addWidget(colors_group)
        widget.setLayout(layout)
        return widget

    def create_elements_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        elements_group = QGroupBox("Görünür Elementler")
        elements_layout = QVBoxLayout()

        for element, visible in self.hud_settings['elements'].items():
            checkbox = QCheckBox(element.replace('_', ' ').title())
            checkbox.setChecked(visible)
            checkbox.stateChanged.connect(lambda state, e=element: self.toggle_element(e, state))
            elements_layout.addWidget(checkbox)

        elements_group.setLayout(elements_layout)
        layout.addWidget(elements_group)

        # Boyut ayarları
        size_group = QGroupBox("Boyut Ayarları")
        size_layout = QVBoxLayout()

        for item, size in self.hud_settings['size'].items():
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{item.replace('_', ' ').title()} Boyutu:"))
            
            spin = QSpinBox()
            spin.setRange(8, 48)
            spin.setValue(size)
            spin.valueChanged.connect(lambda value, i=item: self.update_size(i, value))
            row.addWidget(spin)
            
            size_layout.addLayout(row)

        size_group.setLayout(size_layout)
        layout.addWidget(size_group)

        widget.setLayout(layout)
        return widget

    def create_layout_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Layout editörü
        self.layout_editor = HUDLayoutEditor(self.hud_settings)
        self.layout_editor.layout_changed.connect(self.update_layout)
        layout.addWidget(self.layout_editor)

        widget.setLayout(layout)
        return widget

    def create_performance_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Opaklık ayarı
        opacity_group = QGroupBox("Opaklık")
        opacity_layout = QHBoxLayout()
        
        opacity_slider = QSlider(Qt.Orientation.Horizontal)
        opacity_slider.setRange(0, 100)
        opacity_slider.setValue(int(self.hud_settings['opacity'] * 100))
        opacity_slider.valueChanged.connect(self.update_opacity)
        
        opacity_layout.addWidget(QLabel("0%"))
        opacity_layout.addWidget(opacity_slider)
        opacity_layout.addWidget(QLabel("100%"))
        
        opacity_group.setLayout(opacity_layout)
        layout.addWidget(opacity_group)

        # Yenileme hızı
        refresh_group = QGroupBox("Yenileme Hızı")
        refresh_layout = QHBoxLayout()
        
        refresh_combo = QComboBox()
        refresh_combo.addItems(["15 Hz", "30 Hz", "60 Hz"])
        refresh_combo.setCurrentText(f"{self.hud_settings['refresh_rate']} Hz")
        refresh_combo.currentTextChanged.connect(self.update_refresh_rate)
        
        refresh_layout.addWidget(QLabel("Yenileme Hızı:"))
        refresh_layout.addWidget(refresh_combo)
        
        refresh_group.setLayout(refresh_layout)
        layout.addWidget(refresh_group)

        widget.setLayout(layout)
        return widget

    def choose_color(self, name):
        color = QColorDialog.getColor(QColor(self.hud_settings['colors'][name]))
        if color.isValid():
            self.hud_settings['colors'][name] = color.name()
            self.sender().setStyleSheet(f"background-color: {color.name()};")
            self.settings_updated.emit(self.hud_settings)

    def toggle_element(self, element, state):
        self.hud_settings['elements'][element] = bool(state)
        self.settings_updated.emit(self.hud_settings)

    def update_size(self, item, value):
        self.hud_settings['size'][item] = value
        self.settings_updated.emit(self.hud_settings)

    def update_layout(self, new_layout):
        # Layout değişikliklerini kaydet
        self.settings_updated.emit(self.hud_settings)

    def update_opacity(self, value):
        self.hud_settings['opacity'] = value / 100.0
        self.settings_updated.emit(self.hud_settings)

    def update_refresh_rate(self, rate_text):
        rate = int(rate_text.split()[0])
        self.hud_settings['refresh_rate'] = rate
        self.settings_updated.emit(self.hud_settings)

    def load_settings(self):
        try:
            if os.path.exists('hud_settings.json'):
                with open('hud_settings.json', 'r') as f:
                    saved_settings = json.load(f)
                    self.hud_settings.update(saved_settings)
        except Exception as e:
            QMessageBox.warning(self, "Uyarı", f"Ayarlar yüklenemedi: {str(e)}")

    def save_settings(self):
        try:
            with open('hud_settings.json', 'w') as f:
                json.dump(self.hud_settings, f)
            QMessageBox.information(self, "Başarılı", "Ayarlar kaydedildi!")
            self.settings_updated.emit(self.hud_settings)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Ayarlar kaydedilemedi: {str(e)}")

    def reset_settings(self):
        reply = QMessageBox.question(self, 'Onay', 
                                   'Tüm ayarları varsayılana döndürmek istediğinize emin misiniz?',
                                   QMessageBox.StandardButton.Yes | 
                                   QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            if os.path.exists('hud_settings.json'):
                os.remove('hud_settings.json')
            self.__init__()
            self.settings_updated.emit(self.hud_settings)
            QMessageBox.information(self, "Başarılı", "Ayarlar varsayılana döndürüldü!")