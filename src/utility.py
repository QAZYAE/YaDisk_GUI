from PyQt5.QtWidgets import QMessageBox



def warn(parent = None, message: str = None) -> None:
    """Warning messagebox"""
    QMessageBox.warning(parent, 'Warning', message, QMessageBox.Ok)