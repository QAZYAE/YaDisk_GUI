from PyQt5.QtWidgets import QMessageBox



def warn(parent = None, message: str = None) -> None:
    """Warning messagebox"""
    QMessageBox.warning(parent, 'Warning', message, QMessageBox.Ok)
    
    
def choose(parent = None, title: str = None, message: str = None) -> bool:
    """Choose messagebox"""
    answer = False
    reply = QMessageBox.question(parent, title, message,
                                 QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)
    if reply == QMessageBox.Yes:
        answer = True
    return answer