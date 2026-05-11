"""File dialog with TreeView"""
import os
import posixpath

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QModelIndex

from src.YaDisk_backend import Disk
from src.utility import warn



class FileDialog(QDialog):
    """Choose a file/dir dialog"""
    
    folder_icon = QIcon(os.path.join(os.getcwd(), 'src', 'icons', 'folder.svg'))
    file_icon = QIcon(os.path.join(os.getcwd(), 'src', 'icons', 'file.svg'))
    
    def __init__(self, disk, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.ui = uic.loadUi(os.path.join(os.getcwd(), 'src', 'ui', 'file_dialog.ui'), self)
        self.setModal(True)
        # Widgets
        self.label_status.setText('')
        self.btn_choose.clicked.connect(self.choose_path)
        # TreeView
        self.disk: Disk = disk
        self.tree: QTreeWidget
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Name', 'Modified'])
        self.tree.clicked.connect(self.on_tree_click)
        self.tree.itemActivated.connect(lambda: self.choose_path(return_pressed=True))
        self.fill_dir('/', self.tree)
        # Showing
        self.show()
        
        
    def fill_dir(self, path, parent_item):
        """Fill tree dir with items based on YaDisk files"""
        self.label_status.setText('Fetching data...')
        self.label_status.repaint()
        ls = self.disk.listdir(path)
        if isinstance(ls, str):
            warn(self, ls)
            return
        for name, date, filetype in ls:
            if filetype == 'dir':
                item = QTreeWidgetItem(parent_item, [name, date.strftime("%d.%m.%Y %H:%M:%S"), 'dir'])
                item.setIcon(0, self.folder_icon)
            else:
                item = QTreeWidgetItem(parent_item, [name, date.strftime("%d.%m.%Y %H:%M:%S"), 'file'])
                item.setIcon(0, self.file_icon)
        self.tree.resizeColumnToContents(0)
        self.label_status.setText('')
        self.label_status.repaint()
        
    
    def on_tree_click(self, index: QModelIndex):
        """One of the items clicked"""
        # Checking type
        parent_item = self.tree.itemFromIndex(index)
        if parent_item.text(2) == 'dir':
            # Checking if children are filled
            item = self.tree.itemFromIndex(index.child(0, 0))
            if item is None:
                # Getting full path
                path = self._get_full_path(parent_item)
                self.fill_dir(path, parent_item)
        parent_item.setExpanded(True)
        
        
    def _get_full_path(self, item: QTreeWidgetItem) -> str:
        """Get full path for the item"""
        path = item.text(0)
        parent = item.parent()
        while parent is not None:
            path = posixpath.join(parent.text(0), path)
            parent = parent.parent()
        path = posixpath.sep + path
        return path
        
        
    def choose_path(self, return_pressed=False):
        """Button choose is pressed"""
        item = self.tree.currentItem()
        if item.text(2) == 'dir' and return_pressed:  # Double click on a folder just opens it
            self.on_tree_click(self.tree.currentIndex())
            return
        path = self._get_full_path(item)
        self.parent.chosen_file = path
        self.close()
