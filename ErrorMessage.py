import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi


class ErrorMessage(QDialog):
    def __init__(self, message, parent=None):
        print(message)
        super().__init__(parent)
        loadUi("error.ui", self)
        self.error_message.setText(message)
        self.show()
        self.ok_button.clicked.connect(self.close)
