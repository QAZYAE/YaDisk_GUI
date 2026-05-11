"""Main window"""
import os
import subprocess

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer

from src.file_dialog import FileDialog
from src.YaDisk_backend import Disk
from src.utility import warn



class MainWindow(QMainWindow):
    """Main window"""
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(os.path.join(os.getcwd(), 'src', 'ui', 'MainWindow.ui'), self)
        # Disk backend
        try:
            self.disk = Disk()
        except Exception as e:
            warn(self, f'Exception occured:\n{type(e).__name__}: {e}')
            self.closeEvent(None)
        # Connecting buttons
        # Check status
        self.btn_check_status.clicked.connect(self.check_yadisk_status)
        self.timer = QTimer(self)
        self.timer.singleShot(0, self.check_yadisk_status)
        self.timer.timeout.connect(self.check_yadisk_status)
        self.timer.start(1000)  # 1 second
        # File dialog
        self.btn_path.clicked.connect(self.open_file_dialog)
        # Showing main window
        self.show()
        
        
    def check_yadisk_status(self):
        """Check current yandex disk status"""
        res = subprocess.run(['yandex-disk', 'status'], capture_output=True)
        self.label_yadisk_status.setText(res.stdout.decode())
        
        
    def open_file_dialog(self):
        self.chosen_file = None
        self.file_dialog = FileDialog(disk=self.disk, parent=self)