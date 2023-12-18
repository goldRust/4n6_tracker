from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
class InfoMessage(QDialog):
    def __init__(self, message, parent=None):
        print(message)
        super().__init__(parent)
        loadUi("info_box.ui", self)
        self.info_label.setText(message)
        self.show()
        self.ok_button.clicked.connect(self.close)
