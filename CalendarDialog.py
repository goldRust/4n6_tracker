import sys

from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        self.parent = parent
        print("Loading window")
        super().__init__(parent)
        loadUi("calendar.ui", self)

        self.ok_button.clicked.connect(self.getValues)
        self.cancel_button.clicked.connect(self.close)

    def getValues(self):
        print(self.calendar.selectedDate())
        date = self.calendar.selectedDate()
        day = date.day()
        month = date.month()
        year = date.year()
        display_text = f"Date: {month}-{day}-{year}"
        self.parent.date_label.setText(display_text)
        self.accept()
        return self.calendar.selectedDate()







