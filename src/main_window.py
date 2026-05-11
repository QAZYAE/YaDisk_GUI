"""Main window"""
import os
import subprocess
import time

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
        self.timer.timeout.connect(self.check_yadisk_status)
        self.start_timer()
        # Start/stop
        self.btn_start_stop.clicked.connect(self.start_stop_yadisk)
        # File dialog
        self.btn_path.clicked.connect(self.open_file_dialog)
        # Showing main window
        self.show()
        
        
    def check_yadisk_status(self):
        """Check current yandex disk status"""
        try:
            res = subprocess.run(['yandex-disk', 'status'], capture_output=True)
            self.label_yadisk_status_full.setText(res.stdout.decode())
            if res.stdout.decode().startswith('Error: daemon not started'):
                self.yadisk_status = False
            else:
                self.yadisk_status = True
        except Exception as e:
            self.label_yadisk_status_full.setText(f'{type(e).__name__}: {e}')
            self.yadisk_status = False
        if self.yadisk_status:
            self.label_yadisk_status.setText('Daemon running')
            self.btn_start_stop.setText('Stop')
        else:
            self.label_yadisk_status.setText('Daemon stopped')
            self.btn_start_stop.setText('Start')
            
            
    def start_timer(self):
        """Start the updating timer"""
        self.check_yadisk_status()
        self.timer.start(1000)  # 1 second
        
        
    def stop_timer(self):
        """Stop the timer"""
        self.timer.stop()
        
            
    def start_stop_yadisk(self):
        """Start or stop the daemon"""
        if self.yadisk_status:  # Stopping
            self.label_yadisk_status.setText('Stopping...')
            self.label_yadisk_status.repaint()
            try:
                res = subprocess.run(['yandex-disk', 'stop'], capture_output=True)
                if res.stdout.decode().startswith('Daemon stopped.'):
                    self.yadisk_status = False
                    self.stop_timer()
                    time.sleep(1)
                    self.check_yadisk_status()
                else:
                    raise RuntimeError(f'Could not stop the daemon. Std error: {res.stderr.decode()}')
            except Exception as e:
                self.yadisk_status = True
                self.label_yadisk_status_full.setText(f'Error occured:\n{type(e).__name__}:\n{e}')
                self.start_timer()
        else:  # Starting
            self.label_yadisk_status.setText('Starting...')
            self.label_yadisk_status.repaint()
            try:
                res = subprocess.run(['yandex-disk', 'start'], capture_output=True)
                if res.stdout.decode().startswith('Starting daemon process...Done'):
                    self.yadisk_status = True
                    self.start_timer()
                else:
                    raise RuntimeError(f'Could not start the daemon. Std error: {res.stderr.decode()}')
            except Exception as e:
                self.yadisk_status = False
                self.label_yadisk_status_full.setText(f'Error occured:\n{type(e).__name__}:\n{e}')
                self.stop_timer()
        
        
        
    def open_file_dialog(self):
        self.chosen_file = None
        self.file_dialog = FileDialog(disk=self.disk, parent=self)