import sys
import os
from pathlib import Path

# Proje kök dizinini PYTHONPATH'e ekle
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # QWebEngine için gerekli
    app.setApplicationName("Drone Ground Control Station")
    app.setOrganizationName("ErenKarakoc06")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()