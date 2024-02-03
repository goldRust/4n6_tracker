import sys
from Performance import Performance
from Student import Student
from Tournament import Tournament
from Partner_Dialog import  Partner_Dialog
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi


"""
This dialog allows users to update information about a particular performance.
"""
class EditPerformanceDialog(QDialog):
    def __init__(self, student, event, tournament, tournaments, perf_ind, parent=None):

        self.parent = parent
        self.perf_ind = perf_ind
        self.old_partner = None

        super().__init__(parent)
        loadUi("edit_performance_dialog.ui", self)

        self.student = student
        self.perf = self.student.get_performance(Performance(tournament, event))

        self.edit_rank.setValue(int(self.perf.placement))
        self.edit_event.setText(self.perf.event)
        self.edit_competitors.setText(str(self.perf.competitors))
        self.student_name.setText(self.student.full_name)
        for i in range(len(self.perf.rounds)):
            self.round_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(self.perf.rounds[i].rank)))
            self.round_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.perf.rounds[i].qp)))

        self.edit_tournament.addItems(tournaments)
        self.edit_tournament.setCurrentText(str(self.perf.tournament))
        if self.perf.partner is not None:
            self.student_name.setText(f"{self.student.full_name} & {self.perf.partner.full_name}" )
            self.change_partner.setEnabled(True)



        self.edit_tournament.currentTextChanged.connect(self.enableSave)
        self.edit_rank.textChanged.connect(self.enableSave)
        self.edit_event.textChanged.connect(self.enableSave)
        self.edit_competitors.textChanged.connect(self.enableSave)
        self.round_table.itemChanged.connect(self.enableSave)
        self.delete_button.clicked.connect(self.delete)
        self.cancel_button.clicked.connect(self.cancel)
        self.save_button.clicked.connect(self.save)
        self.change_partner.clicked.connect(self.edit_partner)



    def enableSave(self):
        self.save_button.setEnabled(True)
    def save(self):
        tournament = self.edit_tournament.currentText().split(" -- ")
        tournament = Tournament(tournament[0], tournament[1])
        new_perf = Performance(tournament, self.edit_event.text())
        new_perf.placement = self.edit_rank.text()
        new_perf.competitors = int(self.edit_competitors.text())
        new_perf.partner = self.perf.partner
        if self.round_table.item(0,0) is not None and self.round_table.item(0,1) is not None:
            r1, q1 = self.round_table.item(0,0).text(), self.round_table.item(0,1).text()
            if r1.isnumeric() and q1.isnumeric():
                new_perf.add_round(r1, q1)
        if self.round_table.item(1, 0) is not None and self.round_table.item(1, 1) is not None:
            r1, q1 = self.round_table.item(1, 0).text(), self.round_table.item(1, 1).text()
            if r1.isnumeric() and q1.isnumeric():
                new_perf.add_round(r1, q1)
        if self.round_table.item(2, 0) is not None and self.round_table.item(2, 1) is not None:
            r1, q1 = self.round_table.item(2, 0).text(), self.round_table.item(2, 1).text()
            if r1.isnumeric() and q1.isnumeric():
                new_perf.add_round(r1, q1)

        self.student.delete_performance(self.perf)
        self.student.add_performance(new_perf)
        if self.perf.partner is not None:
            self.perf.partner.delete_performance(self.perf)
            partner_perf = new_perf.duplicate()
            partner_perf.partner = self.student
            self.perf.partner.add_performance(partner_perf)

        if self.perf.competitors != new_perf.competitors:
            for other_student in self.parent.team.students:
                for other_performance in other_student.performances:
                    if other_performance.tournament == new_perf.tournament and other_performance.event == new_perf.event:
                        other_performance.competitors = new_perf.competitors


        #update table

        self.accept()

    def delete(self):
        self.student.delete_performance(self.perf)
        if self.perf.partner is not None:
            self.perf.partner.delete_performance(self.perf)
        self.accept()

    def edit_partner(self):
        try:
            students = [student.full_name for student in self.parent.team.students]
            self.old_partner = self.perf.partner
            self.perf.partner.delete_performance(self.perf)
            new_partner = Partner_Dialog((f"{self.student.full_name}'s partner for {self.perf.event}:", self.perf.event, self.perf.tournament, self.perf.placement), students,self.student, self.parent).exec_()
            self.student_name.setText(f"{self.student.full_name} & {self.perf.partner.full_name}" )
            self.enableSave()
        except Exception as e:
            print(e)

    def cancel(self):
        if self.old_partner is not None:
            self.perf.partner.delete_performance(self.perf)
            partner_performance = self.perf.duplicate()
            partner_performance.partner = self.student
            self.old_partner.add_performance(partner_performance)

            self.perf.partner = self.old_partner
        self.reject()






