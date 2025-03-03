from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                          QLabel, QTextEdit, QComboBox, QFileDialog,
                          QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
import os
import time

class ScriptingEngine(QWidget):
    script_status = pyqtSignal(str, bool)  # status_message, success

    def __init__(self):
        super().__init__()
        self.current_time_utc = "2025-03-02 19:44:38"
        self.current_user = "ErenKarakoc06"
        self.script_file = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Üst bilgi paneli
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel(f"Kullanıcı: {self.current_user}"))
        info_layout.addWidget(QLabel(f"UTC: {self.current_time_utc}"))
        layout.addLayout(info_layout)

        # Script seçimi
        file_layout = QHBoxLayout()
        self.file_label = QLabel("Script Dosyası: Seçilmedi")
        file_layout.addWidget(self.file_label)
        
        select_btn = QPushButton("Dosya Seç")
        select_btn.clicked.connect(self.select_script)
        file_layout.addWidget(select_btn)
        layout.addLayout(file_layout)

        # Script editörü
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Script kodunuzu buraya yazın...")
        layout.addWidget(self.editor)

        # Script tipi seçimi
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Script Tipi:"))
        self.script_type = QComboBox()
        self.script_type.addItems(["Python", "MAVLink", "Özel"])
        type_layout.addWidget(self.script_type)
        layout.addLayout(type_layout)

        # Kontrol butonları
        btn_layout = QHBoxLayout()
        
        run_btn = QPushButton("Çalıştır")
        run_btn.clicked.connect(self.run_script)
        btn_layout.addWidget(run_btn)
        
        save_btn = QPushButton("Kaydet")
        save_btn.clicked.connect(self.save_script)
        btn_layout.addWidget(save_btn)
        
        self.cancel_btn = QPushButton("İptal")
        self.cancel_btn.clicked.connect(self.cancel_script)
        self.cancel_btn.setEnabled(False)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)

        # Durum bildirimi
        self.status_label = QLabel("Hazır")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def select_script(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Script Dosyası Seç",
            "",
            "Python Files (*.py);;All Files (*.*)"
        )
        
        if file_name:
            self.script_file = file_name
            self.file_label.setText(f"Script Dosyası: {os.path.basename(file_name)}")
            
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    self.editor.setText(file.read())
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya okuma hatası: {str(e)}")

    def save_script(self):
        if not self.script_file:
            self.script_file, _ = QFileDialog.getSaveFileName(
                self,
                "Script Kaydet",
                "",
                "Python Files (*.py);;All Files (*.*)"
            )
        
        if self.script_file:
            try:
                with open(self.script_file, 'w', encoding='utf-8') as file:
                    file.write(self.editor.toPlainText())
                self.status_label.setText("Script kaydedildi")
                self.script_status.emit("Script kaydedildi", True)
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Kaydetme hatası: {str(e)}")
                self.script_status.emit(f"Kaydetme hatası: {str(e)}", False)

    def run_script(self):
        script_content = self.editor.toPlainText()
        if not script_content.strip():
            QMessageBox.warning(self, "Uyarı", "Script boş olamaz!")
            return

        try:
            self.status_label.setText("Script çalışıyor...")
            self.cancel_btn.setEnabled(True)
            
            # TODO: Script çalıştırma mantığı eklenecek
            # Örnek için basit bir simülasyon:
            time.sleep(2)
            
            self.status_label.setText("Script başarıyla tamamlandı")
            self.script_status.emit("Script başarıyla tamamlandı", True)
        except Exception as e:
            self.status_label.setText(f"Hata: {str(e)}")
            self.script_status.emit(f"Script hatası: {str(e)}", False)
        finally:
            self.cancel_btn.setEnabled(False)

    def cancel_script(self):
        # TODO: Script iptal mantığı eklenecek
        self.status_label.setText("Script iptal edildi")
        self.cancel_btn.setEnabled(False)
        self.script_status.emit("Script iptal edildi", False)