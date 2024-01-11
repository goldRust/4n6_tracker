import sys
from Performance import Performance
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

'''This dailog allows users to add the performance details to both participants in 2 person events.'''

class Partner_Dialog(QDialog):
    def __init__(self, perf, students, student, parent=None):
        self.parent = parent

        super().__init__(parent)
        loadUi("partner_dialog.ui", self)
        self.student = student
        self.perf = perf
        self.perf_description.setText(perf[0])
        self.partner_select.addItems(students)
        self.okay_button.clicked.connect(self.getValues)
        self.cancel_button.clicked.connect(self.close)



    def getValues(self):
        partner = self.parent.team.get_student(self.partner_select.currentText())
        partner_performance = partner.add_performance(Performance(self.perf[2], self.perf[1]))
        partner_performance.placement = self.perf[3]
        try:
            partner_performance.add_partner(self.student)
            self.student.get_performance(partner_performance).add_partner(partner)
        except Exception as e:
            print(e)
        self.accept()
