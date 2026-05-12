"""Main window"""
import os
import subprocess
import time

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5.QtCore import QTimer

from src.path_editor import PathEditor
from src.YaDisk_backend import Disk
from src.config_parser import ConfigParser
from src.utility import warn, choose



class MainWindow(QMainWindow):
    """Main window"""
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(os.path.join(os.getcwd(), 'src', 'ui', 'MainWindow.ui'), self)
        # Disk backend
        try:
            self.disk = Disk()
        except Exception as e:
            warn(self, f'Exception occurred while creating disk instance:\n{type(e).__name__}: {e}')
            self.closeEvent(None)
        # YaDisk config
        try:
            self.config = ConfigParser(path_to_config=os.path.join(os.getcwd(), 'test.txt'))
        except Exception as e:
            warn(self, f'Exception occurred while reading configuration file:\n{type(e).__name__}: {e}')
            self.closeEvent(None)
        # Connecting buttons
        # Check status timer
        self.btn_check_status.clicked.connect(self.check_yadisk_status)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_yadisk_status)
        self.start_timer()
        # Start/stop
        self.btn_start_stop.clicked.connect(self.start_stop_yadisk)
        # Exception files
        self.btn_add_exception.clicked.connect(self.add_sync_exception)
        self.sync_except_layout = QVBoxLayout()
        self.sync_except_scroll_widget.setLayout(self.sync_except_layout)
        self.fill_sync_exceptions()
        # Save button
        self.btn_save.clicked.connect(self.save_settings)
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
        
        
    def add_sync_exception(self):
        """Add a widget for inputting path of the new synchronization exception"""
        editor = PathEditor(disk=self.disk, parent=self.sync_except_scroll_widget, path=None)
        self.sync_except_layout.addWidget(editor)
        
        
    def fill_sync_exceptions(self):
        """Fill the sync exception widget with paths from config"""
        # Deleting existing widgets
        for child in self.sync_except_scroll_widget.children():
            if isinstance(child, PathEditor):
                child.deleteLater()
        # Creating widgets
        for path in self.config.get_exclude_paths():
            editor = PathEditor(disk=self.disk, parent=self.sync_except_scroll_widget, path=path)
            self.sync_except_layout.addWidget(editor)
            
            
    def update_config(self):
        """Update `self.config`"""
        exclude_paths = []
        for widget in self.sync_except_scroll_widget.children():
            if isinstance(widget, PathEditor):
                if widget.path is not None and not widget.bad_path:
                    exclude_paths.append(widget.path)
        self.config.set_exclude_paths(exclude_paths)
            
        
    def save_settings(self):
        """Save settings to the config file"""
        self.update_config()
        self.config.write()
        
        
    def closeEvent(self, e):
        """On app closing"""
        self.update_config()
        if not self.config.compare_with_file():
            if choose(parent=self, title='Unsaved settings', 
                      message='Some settings have been change. Do you want to save them before closing?'):
                self.config.write()
        self.close()