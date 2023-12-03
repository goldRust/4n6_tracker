import sys
from Performance import Performance
from Student import Student
from Tournament import Tournament
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

class EditPerformanceDialog(QDialog):
    def __init__(self, perf, tournaments, parent=None):

        self.parent = parent

        super().__init__(parent)
        loadUi("edit_performance_dialog.ui", self)
        date, host = perf[2].split(" -- ")

        self.perf = Performance(Tournament(host, date),perf[0])

        self.perf.placement = perf[1]
        self.edit_rank.setText(self.perf.placement)
        self.edit_event.setText(self.perf.event)

        self.edit_tournament.addItems(tournaments)
        self.edit_tournament.setCurrentText(str(self.perf.tournament))
        self.student = parent.team.get_student(parent.selected_student.text())



        self.edit_tournament.currentTextChanged.connect(self.enableSave)
        self.edit_rank.textChanged.connect(self.enableSave)
        self.edit_event.textChanged.connect(self.enableSave)
        self.delete_button.clicked.connect(self.delete)
        self.cancel_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self.save)

    def enableSave(self):
        self.save_button.setEnabled(True)
    def save(self):
        tournament = self.edit_tournament.currentText().split(" -- ")
        tournament = Tournament(tournament[1], tournament[0])
        new_perf = Performance(tournament, self.edit_event.text())
        new_perf.placement = self.edit_rank.text()

        self.parent.team.get_student(self.parent.selected_student.text()).delete_performance(self.perf)
        self.parent.team.get_student(self.parent.selected_student.text()).add_performance(new_perf)
        self.close()

    def delete(self):
        self.student.delete_performance(self.perf)
        self.close()







