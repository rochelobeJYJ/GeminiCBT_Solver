
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QIcon

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from src.gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Set app icon
    icon_path = os.path.join(current_dir, "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Fonts: Malgun Gothic 9pt (approx 12px)
    font = QFont("Malgun Gothic", 9)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
