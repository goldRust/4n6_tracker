import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

class ErrorMessage(QDialog):
    def __init__(self, message, parent=None):
        print(message)
        super().__init__(parent)
        loadUi("error.ui", self)
        print("here")
        self.error_message.setText(message)
        print("text set")
        self.show()
        self.ok_button.clicked.connect(self.close)





