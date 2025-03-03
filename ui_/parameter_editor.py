from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QTableWidget, QTableWidgetItem, QLabel, QLineEdit)
from PyQt6.QtCore import pyqtSignal

class ParameterEditor(QWidget):
    parameter_changed = pyqtSignal(str, float)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Arama kutusu
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Ara:"))
        self.search_box = QLineEdit()
        self.search_box.textChanged.connect(self.filter_parameters)
        search_layout.addWidget(self.search_box)
        layout.addLayout(search_layout)
        
        # Parametre tablosu
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Parametre", "Değer", "Birim", "Açıklama"])
        layout.addWidget(self.table)
        
        # Butonlar
        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("Yenile")
        refresh_btn.clicked.connect(self.refresh_parameters)
        save_btn = QPushButton("Kaydet")
        save_btn.clicked.connect(self.save_parameters)
        load_btn = QPushButton("Yükle")
        load_btn.clicked.connect(self.load_parameters)
        
        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(load_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
    def filter_parameters(self, text):
        for row in range(self.table.rowCount()):
            show = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and text.lower() in item.text().lower():
                    show = True
                    break
            self.table.setRowHidden(row, not show)
    
    def refresh_parameters(self):
        # MAVLink'ten parametreleri al
        pass
    
    def save_parameters(self):
        # Parametreleri dosyaya kaydet
        pass
    
    def load_parameters(self):
        # Parametreleri dosyadan yükle
        pass