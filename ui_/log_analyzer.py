from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                          QLabel, QTextEdit, QFileDialog, QComboBox,
                          QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
import os
import time
from datetime import datetime

class LogAnalyzer(QWidget):
    analysis_completed = pyqtSignal(str, bool)  # result_message, success

    def __init__(self):
        super().__init__()
        self.current_time_utc = "2025-03-02 19:46:01"
        self.current_user = "ErenKarakoc06"
        self.log_file = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Üst bilgi paneli
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel(f"Kullanıcı: {self.current_user}"))
        info_layout.addWidget(QLabel(f"UTC: {self.current_time_utc}"))
        layout.addLayout(info_layout)

        # Log dosyası seçimi
        file_layout = QHBoxLayout()
        self.file_label = QLabel("Log Dosyası: Seçilmedi")
        file_layout.addWidget(self.file_label)
        
        select_btn = QPushButton("Dosya Seç")
        select_btn.clicked.connect(self.select_log)
        file_layout.addWidget(select_btn)
        layout.addLayout(file_layout)

        # Analiz tipi seçimi
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Analiz Tipi:"))
        self.analysis_type = QComboBox()
        self.analysis_type.addItems([
            "Genel Analiz",
            "Hata Analizi",
            "Performans Analizi",
            "Sensör Verileri",
            "Motor/ESC Logs",
            "GPS Tracks"
        ])
        type_layout.addWidget(self.analysis_type)
        layout.addLayout(type_layout)

        # Log görüntüleyici
        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setPlaceholderText("Log içeriği burada görüntülenecek...")
        layout.addWidget(self.log_viewer)

        # İlerleme çubuğu
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Kontrol butonları
        btn_layout = QHBoxLayout()
        
        analyze_btn = QPushButton("Analiz Et")
        analyze_btn.clicked.connect(self.analyze_log)
        btn_layout.addWidget(analyze_btn)
        
        export_btn = QPushButton("Dışa Aktar")
        export_btn.clicked.connect(self.export_results)
        btn_layout.addWidget(export_btn)
        
        clear_btn = QPushButton("Temizle")
        clear_btn.clicked.connect(self.clear_analysis)
        btn_layout.addWidget(clear_btn)
        
        layout.addLayout(btn_layout)

        # Durum bildirimi
        self.status_label = QLabel("Hazır")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def select_log(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Log Dosyası Seç",
            "",
            "Log Files (*.log *.txt);;All Files (*.*)"
        )
        
        if file_name:
            self.log_file = file_name
            self.file_label.setText(f"Log Dosyası: {os.path.basename(file_name)}")
            
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.log_viewer.setText(content)
                    self.status_label.setText("Log dosyası yüklendi")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya okuma hatası: {str(e)}")

    def analyze_log(self):
        if not self.log_file:
            QMessageBox.warning(self, "Uyarı", "Önce bir log dosyası seçin!")
            return

        try:
            self.progress_bar.show()
            self.progress_bar.setValue(0)
            self.status_label.setText("Analiz başlatılıyor...")

            # Analiz tipine göre işlem
            analysis_type = self.analysis_type.currentText()
            
            # Simüle edilmiş analiz süreci
            for i in range(101):
                time.sleep(0.05)  # Simüle edilmiş işlem
                self.progress_bar.setValue(i)
                if i % 20 == 0:
                    self.status_label.setText(f"Analiz devam ediyor... {i}%")

            # Örnek analiz sonuçları
            results = f"""
            Analiz Tipi: {analysis_type}
            Dosya: {os.path.basename(self.log_file)}
            Tarih: {self.current_time_utc}
            
            Özet:
            - Toplam log süresi: 1 saat 23 dakika
            - Hata sayısı: 0
            - Uyarı sayısı: 2
            - Maksimum yükseklik: 120m
            - Ortalama hız: 15 m/s
            
            Detaylı analiz raporu için dışa aktarma yapabilirsiniz.
            """
            
            self.log_viewer.setText(results)
            self.status_label.setText("Analiz tamamlandı")
            self.analysis_completed.emit("Analiz başarıyla tamamlandı", True)

        except Exception as e:
            self.status_label.setText(f"Hata: {str(e)}")
            self.analysis_completed.emit(f"Analiz hatası: {str(e)}", False)
        finally:
            self.progress_bar.hide()

    def export_results(self):
        if not self.log_viewer.toPlainText():
            QMessageBox.warning(self, "Uyarı", "Dışa aktarılacak analiz sonucu yok!")
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Analiz Sonuçlarını Kaydet",
            "",
            "Text Files (*.txt);;All Files (*.*)"
        )
        
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(self.log_viewer.toPlainText())
                self.status_label.setText("Sonuçlar dışa aktarıldı")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dışa aktarma hatası: {str(e)}")

    def clear_analysis(self):
        self.log_viewer.clear()
        self.status_label.setText("Hazır")
        self.progress_bar.hide()
        self.file_label.setText("Log Dosyası: Seçilmedi")
        self.log_file = None