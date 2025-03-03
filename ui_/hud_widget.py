from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
import math

class HUDWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        
        # HUD verileri
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.altitude = 0
        self.airspeed = 0
        self.groundspeed = 0
        self.vertical_speed = 0
        self.heading = 0
        
        # Görsel ayarlar
        self.setBackgroundRole(QPalette.ColorRole.Base)
        self.setAutoFillBackground(True)

    def update_data(self, roll, pitch, yaw, alt, airspeed, groundspeed, vspeed, heading):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        self.altitude = alt
        self.airspeed = airspeed
        self.groundspeed = groundspeed
        self.vertical_speed = vspeed
        self.heading = heading
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Ekran merkezi
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Ufuk çizgisi
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(-self.roll)
        
        pen = QPen(QColor(0, 255, 0))
        painter.setPen(pen)
        
        # Pitch ladder
        for i in range(-90, 91, 10):
            y = (i - self.pitch) * 2
            if abs(y) < self.height():
                if i == 0:  # Ufuk çizgisi
                    painter.drawLine(-50, y, 50, y)
                else:
                    painter.drawLine(-25, y, 25, y)
                    painter.drawText(-45, y + 5, f"{i}")
        
        painter.restore()
        
        # Heading indicator
        painter.setPen(QPen(QColor(0, 255, 0)))
        painter.drawText(10, 20, f"HDG: {int(self.heading)}°")
        
        # Altitude indicator
        painter.drawText(self.width() - 70, 20, f"ALT: {int(self.altitude)}m")
        
        # Airspeed indicator
        painter.drawText(10, self.height() - 10, f"AS: {int(self.airspeed)}m/s")
        
        # Ground speed
        painter.drawText(self.width() - 100, self.height() - 10, 
                        f"GS: {int(self.groundspeed)}m/s")
        
        # Vertical speed indicator
        vs_height = 100
        vs_width = 20
        vs_x = self.width() - 30
        vs_y = (self.height() - vs_height) / 2
        
        painter.drawRect(vs_x, vs_y, vs_width, vs_height)
        vs_indicator = max(min((-self.vertical_speed * 5) + vs_height/2, vs_height), 0)
        painter.fillRect(vs_x, vs_y + vs_height - vs_indicator, vs_width, 2, QColor(0, 255, 0))