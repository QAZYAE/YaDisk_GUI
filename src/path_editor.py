"""Custom widget for path editing line"""
import os

from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

from src.file_dialog import FileDialog
from src.YaDisk_backend import Disk
from src.utility import warn



class PathEditor(QWidget):
    """Custom widget for path editing line"""
    
    bad_path: bool = False  # True if the path doesn't  exist
    
    def __init__(self, disk, parent=None, path=None):
        super().__init__(parent)
        self.ui = uic.loadUi(os.path.join(os.getcwd(), 'src', 'ui', 'PathEditor.ui'), self)
        # Initial variables
        self.disk: Disk = disk
        self.path = path
        self.update_path_display()
        # Connecting events
        self.line_edit_path.editingFinished.connect(self.on_edit_finished)
        self.btn_browse.clicked.connect(self.open_file_dialog)
        self.btn_delete.clicked.connect(self.delete_editor)
        
        
    def update_path_display(self):
        """Update path line edit"""
        if self.path is None:
            self.line_edit_path.setText('Choose a path')
        else:
            self.line_edit_path.setText(self.path)
        if self.bad_path:
            self.label_bad_path.setText('Bad path!')
        else:
            self.label_bad_path.setText('')
            
            
    def on_edit_finished(self):
        # Fixing Qt bug where the method is called twice
        if not self.line_edit_path.isModified():
            return
        self.line_edit_path.setModified(False)
        # Checking if path is None
        self.path = self.line_edit_path.text()
        if self.path == 'Choose a path':
            self.path = None
            return
        # Checking if path exists
        self.line_edit_path.setText('Checking the path...')
        self.line_edit_path.repaint()
        exists = self.disk.check_path(self.path)
        if isinstance(exists, str):
            warn(self, exists)
            self.bad_path = True
        else:
            self.bad_path = not exists
        if self.bad_path:
            warn(self, 'The path does not exist!')
        self.update_path_display()
        
        
    def open_file_dialog(self):
        """Browse button pressed"""
        self.file_dialog = FileDialog(disk=self.disk, parent=self)
        
        
    def delete_editor(self):
        """Button delete pressed"""
        self.deleteLater()