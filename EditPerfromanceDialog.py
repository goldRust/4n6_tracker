import sys
from Performance import Performance
from Student import Student
from Tournament import Tournament
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

class EditPerformanceDialog(QDialog):
    def __init__(self, perf, tournaments, perf_ind, parent=None):

        self.parent = parent
        self.perf_ind = perf_ind

        super().__init__(parent)
        loadUi("edit_performance_dialog.ui", self)
        host, date = perf[2].split(" -- ")

        self.student = parent.team.get_student(parent.selected_student.text())
        self.perf = self.student.get_performance(Performance(Tournament(host, date),perf[0]))

        self.edit_rank.setValue(int(self.perf.placement))
        self.edit_event.setText(self.perf.event)
        self.edit_competitors.setText(str(self.perf.competitors))
        for i in range(len(self.perf.rounds)):
            self.round_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(self.perf.rounds[i].rank)))
            self.round_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.perf.rounds[i].qp)))

        self.edit_tournament.addItems(tournaments)
        self.edit_tournament.setCurrentText(str(self.perf.tournament))




        self.edit_tournament.currentTextChanged.connect(self.enableSave)
        self.edit_rank.textChanged.connect(self.enableSave)
        self.edit_event.textChanged.connect(self.enableSave)
        self.edit_competitors.textChanged.connect(self.enableSave)
        self.round_table.itemChanged.connect(self.enableSave)
        self.delete_button.clicked.connect(self.delete)
        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.save)



    def enableSave(self):
        self.save_button.setEnabled(True)
    def save(self):
        tournament = self.edit_tournament.currentText().split(" -- ")
        tournament = Tournament(tournament[0], tournament[1])
        new_perf = Performance(tournament, self.edit_event.text())
        new_perf.placement = self.edit_rank.text()
        new_perf.competitors = int(self.edit_competitors.text())
        new_perf.add_round(self.round_table.item(0,0).text(), self.round_table.item(0,1).text())
        new_perf.add_round(self.round_table.item(1,0).text(), self.round_table.item(1,1).text())
        new_perf.add_round(self.round_table.item(2,0).text(), self.round_table.item(2,1).text())
        self.parent.team.get_student(self.parent.selected_student.text()).delete_performance(self.perf)
        self.parent.team.get_student(self.parent.selected_student.text()).add_performance(new_perf)

        #update table

        self.accept()

    def delete(self):
        self.student.delete_performance(self.perf)
        self.accept()







