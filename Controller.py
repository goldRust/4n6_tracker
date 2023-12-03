import time

from Team import Team
from Performance import Performance
from Tournament import Tournament
from ErrorMessage import ErrorMessage
from Partner_Dialog import Partner_Dialog
from EditPerfromanceDialog import EditPerformanceDialog
import sys
import pickle
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog



class Controller(QMainWindow):
    def __init__(self):
        self.team = None

        super(Controller, self).__init__()
        loadUi("Forensics_Organizer.ui", self)

        self.setWindowIcon(QtGui.QIcon("4n6_icon.png"))
        self.setWindowTitle("4N6 Season Organizer")

        self.set_columns()

        self.set_interactive()

    def load_team_info(self):
        self.team_name.setText(self.team.name)

        self.update_team_report()
        self.team.students.sort()
        self.update_student_list()

        self.update_event_list()

        self.update_tourney_list()

    def clear_team_info(self):

        self.stud_selector.clear()
        print("Stud Cleared")
        self.np_tourney.clear()
        print("Tourney Cleared")
        self.tourney_selector.clear()
        print("Tourney Cleared")
        self.event_selector.clear()
        print("Event Cleared")

    def update_student_list(self):
        students = []
        self.stud_selector.clear()
        for student in self.team.students:
            students.append(student.full_name)

        self.stud_selector.addItems(students)

    def update_event_list(self):
        events = []
        self.event_selector.clear()
        for student in self.team.students:
            for perf in student.performances:
                if perf.event not in events:
                    events.append(perf.event)
        self.event_selector.addItems(events)

    def update_tourney_list(self):
        tourneys = []
        self.np_tourney.clear()
        self.tourney_selector.clear()
        for tourney in self.team.tournaments:
            tourneys.append(str(tourney))
        self.tourney_selector.addItems(tourneys)
        self.np_tourney.addItems(tourneys)

    def update_team_report(self):

        table = []

        for student in self.team.students:
            events = ""
            tournaments = ""
            for perf in student.performances:
                if perf.event not in events:
                    events += f"{perf.event}, "
                if perf.tournament.school not in tournaments:
                    tournaments += f"{str(perf.tournament)} | "
            table.append([student.full_name, tournaments, events])
        row_ind = 0
        col_ind = 0

        self.team_report.setRowCount(len(table))

        for row in table:
            print(row)
            for col in row:
                self.team_report.setItem(row_ind, col_ind, QtWidgets.QTableWidgetItem(col))
                col_ind += 1

    def update_student_report(self, student):
        if len(student) < 1:
            return
        self.selected_student.setText(student)
        self.stud_report.setRowCount(len(self.team.get_student(student).performances))
        perf_ind = 0
        for perf in self.team.get_student(student).performances:
            rank = perf.placement
            if rank == -1:
                rank = "Unranked"
            self.stud_report.setItem(perf_ind, 0, QtWidgets.QTableWidgetItem(perf.event))
            self.stud_report.setItem(perf_ind, 1, QtWidgets.QTableWidgetItem(rank))
            self.stud_report.setItem(perf_ind, 2, QtWidgets.QTableWidgetItem(str(perf.tournament)))

            perf_ind += 1

        self.add_performance_frame.enabled = True
        self.np_tourney.enabled = True



    def update_event_report(self, event):
        if len(event) < 1:
            return
        self.event_label.setText(event)
        table = []
        for student in self.team.students:
            for perf in student.performances:
                if perf.event == event:
                    rank = perf.placement
                    if rank == -1:
                        rank = "Unranked"
                    rank = str(rank)
                    table.append([student.full_name, rank, str(perf.tournament)])
        if len(table) < 1:
            ErrorMessage("No Performances to show.", self)
        self.event_report.setRowCount(len(table))
        row_ind = 0
        col_ind = 0
        for row in table:
            for col in row:
                self.event_report.setItem(row_ind, col_ind, QtWidgets.QTableWidgetItem(col))
                col_ind += 1
            col_ind = 0
            row_ind += 1

    def update_tournament_report(self, host):
        if len(host) < 1:
            return
        table = []
        for student in self.team.students:
            for perf in student.performances:
                if str(perf.tournament) == host:
                    rank = perf.placement
                    if rank == -1:
                        rank = "Unranked"
                    rank = str(rank)
                    table.append([student.full_name, perf.event, rank])

        self.tourney_report.setRowCount(len(table))
        row_ind = 0
        col_ind = 0
        for row in table:
            for col in row:
                self.tourney_report.setItem(row_ind, col_ind, QtWidgets.QTableWidgetItem(col))
                col_ind += 1
            col_ind = 0
            row_ind += 1
        self.tourney_report.cellClicked.connect(self.clicked)

    def set_columns(self):
        for i in range(self.stud_report.columnCount()):
            self.stud_report.setColumnWidth(i, 200)
        for i in range(self.team_report.columnCount()):
            self.team_report.setColumnWidth(i, 200)
        for i in range(self.tourney_report.columnCount()):
            self.tourney_report.setColumnWidth(i, 200)
        for i in range(self.event_report.columnCount()):
            self.event_report.setColumnWidth(i, 200)

    def set_interactive(self):
        # Change the selected student.
        self.stud_selector.currentTextChanged.connect(self.update_student_report)

        # Change the selected event.
        self.event_selector.currentTextChanged.connect(self.update_event_report)

        # Change the selected tournament
        self.tourney_selector.currentTextChanged.connect(self.update_tournament_report)

        # Add Student with button
        self.add_stud_button.clicked.connect(self.gui_add_student)

        # Save
        self.actionSave.triggered.connect(self.save)

        # Load
        self.actionLoad.triggered.connect(self.load)

        # Add Student
        self.add_perf_button.clicked.connect(self.gui_add_performance)

        # New Team
        self.actionNew.triggered.connect(self.gui_new_team)

        # New Tournament
        self.nt_button.clicked.connect(self.gui_add_tournament)

        # Student report click to edit
        self.stud_report.cellClicked.connect(self.edit_performance)

    def gui_new_team(self):
        new_team = ""
        while len(new_team)<1:
            new_team, done = QtWidgets.QInputDialog.getText(
                self, "New Team", "Team Name"
            )
        if done:
            print("Done")
            print(new_team)
            self.team = Team(new_team)
            self.load_team_info()
        else:
            print("nope")
            return

    def gui_add_student(self):
        if self.team is None:
            ErrorMessage("No team!\nLoad a team file or make a new one by clicking File in the top left.",self)
            return
        first = self.ns_first.text()
        last = self.ns_last.text()
        if len(first) < 1 or len(last) < 1:
            ErrorMessage("First and last name required.", self)
            return
        student = self.team.new_student(first, last)
        if student is not None:
            self.stud_selector.addItem(student.full_name)
        self.update_student_report(f"{first} {last}")
        self.ns_first.clear()
        self.ns_last.clear()

    def gui_add_tournament(self):
        if self.team is None:
            ErrorMessage("No team!\nLoad a team file or make a new one by clicking File in the top left.",self)
            return

        host = self.nt_host.text()
        date = self.nt_date.text()
        if len(host) < 1:
            ErrorMessage("Host school name required.", self)
            return
        new_tourney = Tournament(host, date)
        self.team.tournaments.append(new_tourney)
        self.tourney_selector.addItem(str(new_tourney))
        self.np_tourney.addItem(str(new_tourney))
        self.nt_host.clear()
        self.nt_date.clear()

    def gui_add_performance(self):
        if self.team is None:
            ErrorMessage("No team!\nLoad a team file or make a new one by clicking File in the top left.",self)
        student = self.team.get_student(self.selected_student.text())

        if student is None:
            ErrorMessage("Student not found!", self)
            return

        tourney = self.np_tourney.currentText().split(" -- ")
        if len(tourney) < 1:
            ErrorMessage("No Tournament Selected", self)
            return

        tourney = Tournament(tourney[1], tourney[0])

        if len(self.np_event.text()) < 1:
            ErrorMessage("Event Required", self)
            return

        performance = Performance(tourney, self.np_event.text())
        performance = student.add_performance(performance)
        performance.placement = self.np_rank.text()
        if performance.event == "IDA" or performance.event == "DA" or performance.event == "DI":
            students =  [stud.full_name for stud in self.team.students]
            partner = self.team.get_student(Partner_Dialog((f"{student.full_name}'s partner for {performance.event}:",performance.event,performance.tournament,performance.placement), students, self).exec_())


        self.np_rank.clear()
        self.np_event.clear()
        self.update_student_report(student.full_name)
        self.update_tournament_report(performance.tournament.school)
        self.update_event_report(performance.event)
        self.update_event_list()
        self.update_team_report()

    def edit_performance(self,row,col):
        print(f"{row} {col} Clicked")
        tournaments = [str(tournament) for tournament in self.team.tournaments]
        perf = (self.stud_report.item(row,0).text(), self.stud_report.item(row,1).text() , self.stud_report.item(row,2).text())

        rebuild = EditPerformanceDialog(perf,tournaments, row, self).exec_()
        if rebuild:
            self.stud_report.clearContents()
            
            self.update_student_report(self.selected_student.text())




    def clicked(self, row, col):
        print(f"{row} {col} Clicked")

    def load(self):
        file = self.openFileNameDialog("4n6 Files (*.4n6)")
        if not file:
            return
        if file:
            if ".4n6" not in file:
                ErrorMessage("Only able to load .4n6 files!", self)
                return

        try:
            with open(file, 'rb') as f:
                self.team = pickle.load(f)

                # For some reason this causes an error. It seems to run completely, then causes the program to close.
                # self.clear_team_info()
                self.load_team_info()
        except Exception as e:
            ErrorMessage(e, self)

    def save(self):
        file = self.team.name + ".4n6"
        with open(file, 'wb') as f:
            pickle.dump(self.team, f, protocol=pickle.HIGHEST_PROTOCOL)
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setText(f"{file} has been saved.")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg_box.exec_()


    def new_team(self, team_name):
        self.team = Team(team_name)

    '''
    @staticmethod
    def main(args):
        ctrl = Controller()
        if len(args) == 2:
            ctrl.load(args[1])
        else:
            team = input("Enter your team name: ")
            ctrl.new_team(team)

        # Show menu:
        while True:
            print("To add or edit a student, enter 'new_student'")
            print("To show a report, enter 'report'")
            print("To exit, enter 'exit'")
            response = input(">>")
            if response == "new_student":
                first = input("First name: ")
                last = input("Last name: ")
                student = ctrl.team.new_student(first, last)
                add_performance = input(f"Would you like to add a performance to {student.full_name}?")
                while add_performance == "y" or add_performance == "yes":
                    tourney = input("Tournament: ")
                    date = input("Date: ")
                    event = input("Event: ")
                    student.add_performance(Performance(Tournament(tourney,date),event))

                    add_performance = input(f"Would you like to add a performance to {student.full_name}?")
                ctrl.save()

            if response == "report":
                print(ctrl.team)

            if response == "save":
                ctrl.save()

            if response == "load":
                file = input("Enter the file name: ")
                ctrl.load(file)

            if response == "tr":
                ctrl.team.tournament_report(input("Host School: "))

            if response == "er":
                report = ctrl.team.event_report(input("Event: "))

            if response == 'sr':
                print(ctrl.team.get_student(input("First Name: "),input("Last Name: ")))

            if response == "exit":
                return
    '''

    def openFileNameDialog(self, type):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  type, options=options)
        return fileName

    @staticmethod
    def main(args):
        app = QApplication(args)
        mainwindow = Controller()
        widget = QtWidgets.QStackedWidget()
        widget.addWidget(mainwindow)
        widget.setFixedHeight(850)
        widget.setFixedWidth(1120)
        widget.setWindowIcon(QtGui.QIcon("4n6_icon.png"))
        widget.setWindowTitle("4N6 Season Tracker")
        widget.show()

        try:
            app.exec_()
        except Exception as e:
            print(e)
            ErrorMessage(e, mainwindow)


# Main Guard
if __name__ == "__main__":
    Controller.main(sys.argv)
