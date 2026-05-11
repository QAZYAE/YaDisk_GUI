# Pulled from MemriBoard

import sys
import PyQt5
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from src.main_window import MainWindow

def main() -> None:
    
    # DPI fixing (pulled from MemriBoard https://github.com/neurocomputer/MemriBoard)
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()