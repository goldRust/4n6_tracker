import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi


class Welcome(QDialog):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__(parent)
        loadUi("welcome_screen.ui", self)
        self.load_team.clicked.connect(self.loadTeam)
        self.new_team.clicked.connect(self.newTeam)

    def newTeam(self):
        self.parent.gui_new_team()
        self.close()

    def loadTeam(self):
        self.parent.load()
        self.close()
