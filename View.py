from PySide6 import QtCore, QtWidgets, QtGui


class View(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.home_view()

    def home_view(self):
        self.button = QtWidgets.QPushButton("Load")
        self.text = QtWidgets.QLabel("Welcome to 4n6 Season Tracker",
                                     alignment=QtCore.Qt.AlignCenter)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect()