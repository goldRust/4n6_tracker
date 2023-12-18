import time

from Team import Team
from Performance import Performance
from Tournament import Tournament
from ErrorMessage import ErrorMessage
from Partner_Dialog import Partner_Dialog
from EditPerfromanceDialog import EditPerformanceDialog
from Awards import Award
from PDF_Gen import PDF_Gen
import sys, os
import pickle
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap


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
        if self.team is None:
            ErrorMessage("Load a file or create a new team first.", self)
            return
        self.team_name.setText(self.team.name)
        self.team_name.resize(len(self.team.name)*24,24)
        # self.patch_tournaments()
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
        if self.team is None:
            ErrorMessage("Load a file or create a new team first.", self)
            return

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
            # print(row)
            for col in row:
                self.team_report.setItem(row_ind, col_ind, QtWidgets.QTableWidgetItem(col))
                col_ind += 1

    def update_student_report(self, student):
        if self.team is None:
            ErrorMessage("Load a file or create a new team first.", self)
            return
        if len(student) < 1:
            return
        self.selected_student.setText(student)
        self.stud_report.setRowCount(len(self.team.get_student(student).performances))
        perf_ind = 0
        for perf in self.team.get_student(student).performances:
            rank = perf.placement
            if rank == -1 or rank == "":
                rank = "Unranked"
            state_qualifier = ""
            if str(rank) == "1" or str(rank) == "2":
                state_qualifier = " *State Qualified*"
            rank = str(rank) + state_qualifier
            self.stud_report.setItem(perf_ind, 0, QtWidgets.QTableWidgetItem(perf.event))
            self.stud_report.setItem(perf_ind, 1, QtWidgets.QTableWidgetItem(rank))
            self.stud_report.setItem(perf_ind, 2, QtWidgets.QTableWidgetItem(str(perf.tournament)))

            perf_ind += 1

        self.add_performance_frame.setEnabled(True)
        self.np_tourney.setEnabled(True)

        self.delete_student.setEnabled(True)

    def update_event_report(self, event):
        if self.team is None:
            ErrorMessage("Load a file or create a new team first.", self)
            return
        if len(event) < 1:
            return
        self.event_label.setText(event)
        table = []
        for student in self.team.students:
            for perf in student.performances:
                if perf.event == event:
                    rank = perf.placement
                    if rank == -1 or rank == "":
                        rank = "Unranked"
                    state_qualifier = ""
                    if str(rank) == "1" or str(rank) == "2":
                        state_qualifier = " *State Qualified*"
                    rank = str(rank) + state_qualifier
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

    # Used to update old files in which the tournament class didn't have the photo attribute.
    def patch_tournaments(self):
        for i in range(len(self.team.tournaments)):
            tournament = Tournament(self.team.tournaments[i].school, self.team.tournaments[i].date)
            self.team.tournaments[i] = tournament

    def update_tournament_report(self, host):
        if self.team is None:
            ErrorMessage("Load a file or create a new team first.", self)
            return

        if len(host) < 1:
            return

        tournament = self.team.get_tournament(host)
        table = []
        for student in self.team.students:
            for perf in student.performances:
                state_qualifier = ""
                if str(perf.tournament) == host:
                    rank = perf.placement
                    if rank == -1:
                        rank = "Unranked"
                    if str(rank) == "1" or str(rank) == "2":
                        state_qualifier = " *State Qualified*"
                    rank = str(rank) + state_qualifier
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
        if tournament.photo is not None:
            if os.path.isfile(tournament.photo):
                try:
                    file = QPixmap(tournament.photo).scaledToWidth(408)
                    self.team_picture.setPixmap(file)
                    self.photo_button.setText("Change Photo")
                except Exception as e:
                    ErrorMessage(e, self)
            else:
                ErrorMessage(
                    f"{tournament.photo} is not a valid file path. Perhaps it was loaded on a different computer?",
                    self)
        else:
            print("loading default picture.")
            pixmap = QPixmap("./images/no_team.jpg").scaledToWidth(408)
            self.team_picture.setPixmap(pixmap)
        self.awards_button.setEnabled(True)

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
        # Exit
        self.actionExit.triggered.connect(self.close)
        # Add Student
        self.add_perf_button.clicked.connect(self.gui_add_performance)
        # New Team
        self.actionNew.triggered.connect(self.gui_new_team)
        # New Tournament
        self.nt_button.clicked.connect(self.gui_add_tournament)
        # Student report click to edit
        self.stud_report.cellClicked.connect(self.edit_performance)
        # Team Report click to view student
        self.team_report.cellClicked.connect(self.view_student)
        # Awards maker button
        self.awards_button.clicked.connect(self.make_awards)
        # Team PDF menu item
        self.actionTeam_Report_2.triggered.connect(self.pdf_team_report)
        # Student PDF menu item
        self.actionStudent_Report_2.triggered.connect(self.pdf_student_report)
        # Tournament PDF menu item
        self.actionTournament_Report_2.triggered.connect(self.pdf_tournament_report)
        # Event PDF menu item
        self.actionEvent_Report_2.triggered.connect(self.pdf_event_report)
        # State PDF menu item
        self.actionState_Qualifier_Report.triggered.connect(self.pdf_state_report)
        # Switch tabs.
        self.tabWidget.tabBarClicked.connect(self.click_tab)
        # Student removal button
        self.delete_student.clicked.connect(self.gui_remove_student)
        self.delete_student.setStyleSheet("background-color: tomato")

        # Team Picture clickable
        self.photo_button.clicked.connect(self.get_team_picture)

    def click_tab(self, tab):
        if tab == 0:
            self.load_team_info()
        if tab == 1:
            self.update_student_report(self.stud_selector.currentText())
        if tab == 2:
            self.update_tournament_report(self.tourney_selector.currentText())
        if tab == 3:
            self.update_event_report(self.event_label.text())

    def view_student(self, row, column):

        if column != 0:
            return
        name = self.team_report.item(row, column).text()

        self.update_student_report(name)
        self.stud_selector.setCurrentText(name)
        self.tabWidget.setCurrentIndex(1)

    def gui_new_team(self):
        new_team = ""
        while len(new_team) < 1:
            new_team, done = QtWidgets.QInputDialog.getText(
                self, "New Team", "Team Name"
            )
            if not done:
                return

        if done:
            print(new_team)
            self.team = Team(new_team)
            self.load_team_info()
        else:
            print("nope")
            return

    def gui_add_student(self):
        if self.team is None:
            ErrorMessage("No team!\nLoad a team file or make a new one by clicking File in the top left.", self)
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

    def gui_remove_student(self):
        confirm = QtWidgets.QMessageBox.question(self, "DELETE STUDENT!",
                                                 f"This will completely remove all records of this student.\nThis cannot be undone!\nAre you certain you wish to remove {self.team.get_student(self.selected_student.text()).full_name}?",
                                                 QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
        if confirm == QtWidgets.QMessageBox.Yes:
            try:
                student = self.team.get_student(self.selected_student.text())
                self.team.delete_student(student)
                self.update_student_list()
                self.update_student_report(self.stud_selector.curentText())
            except Exception as e:
                print(e)

    def gui_add_tournament(self):
        if self.team is None:
            ErrorMessage("No team!\nLoad a team file or make a new one by clicking File in the top left.", self)
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
            ErrorMessage("No team!\nLoad a team file or make a new one by clicking File in the top left.", self)
        student = self.team.get_student(self.selected_student.text())
        print(student)
        if student is None:
            ErrorMessage("Student not found!", self)
            return
        try:
            tourney = self.team.get_tournament(self.np_tourney.currentText())
        except Exception as e:
            print(e)
        # tourney = self.np_tourney.currentText().split(" -- ")
        if tourney is None:
            ErrorMessage("No Tournament Selected. \nSelect a tournament from the list or make a new one in the Tournament tab.", self)
            return

        if len(self.np_event.text()) < 1:
            ErrorMessage("Event Required", self)
            return
        performance = Performance(tourney, self.np_event.text())
        performance = student.add_performance(performance)
        performance.placement = self.np_rank.text()
        if performance.event == "IDA" or performance.event == "DA" or performance.event == "DI":
            students = [stud.full_name for stud in self.team.students]
            partner = self.team.get_student(Partner_Dialog((f"{student.full_name}'s partner for {performance.event}:",
                                                            performance.event, performance.tournament,
                                                            performance.placement), students, self).exec_())
        self.np_rank.clear()
        self.np_event.clear()
        self.update_student_report(student.full_name)
        self.update_tournament_report(str(performance.tournament))
        self.update_event_report(performance.event)
        self.update_event_list()
        self.update_team_report()

    def edit_performance(self, row, col):
        print(f"{row} {col} Clicked")
        tournaments = [str(tournament) for tournament in self.team.tournaments]
        perf = (self.stud_report.item(row, 0).text(), self.stud_report.item(row, 1).text(),
                self.stud_report.item(row, 2).text())

        rebuild = EditPerformanceDialog(perf, tournaments, row, self).exec_()
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
        if self.team is None:
            ErrorMessage("No team found! Create a new team or load an existing team file.", self)
            return
        directory = self.openFolderNameDialog()
        file = directory +"/"+ self.team.name + ".4n6"
        with open(file, 'wb') as f:
            pickle.dump(self.team, f, protocol=pickle.HIGHEST_PROTOCOL)
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setText(f"{file} has been saved.")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg_box.exec_()

    def new_team(self, team_name):
        self.team = Team(team_name)

    def openFileNameDialog(self, type):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open .4N6 File", "",
                                                  type, options=options)
        return fileName

    def openFolderNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folderName = QFileDialog.getExistingDirectory(self, "Select Directory", "", options=options)
        # print(folderName)
        return folderName

    def closeEvent(self, event):
        save_first = QtWidgets.QMessageBox.question(self, "QUIT", "Do you wish to save before you exit?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if save_first == QtWidgets.QMessageBox.Yes:
            self.save()
            if not type(event) == bool:
                event.accept()
                sys.exit()
        else:
            if not type(event) == bool:
                sys.exit()

    def make_awards(self):
        tournament = self.team.get_tournament(self.tourney_selector.currentText())
        awards = []
        for student in self.team.students:
            for perf in student.performances:
                if perf.tournament == tournament:
                    rank = perf.placement
                    if rank.isnumeric() and int(rank) < 10:
                        award = Award(student.first, student.last, perf.event, rank)
                        awards.append(award)
        folder = self.openFolderNameDialog()
        if len(folder) < 1:
            return
        print(folder)
        pdf = PDF_Gen()
        pdf.create_awards(awards, folder, str(tournament), team_pic=tournament.photo)

        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setText(f"{tournament} awards file has been saved.")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg_box.exec_()

    def pdf_team_report(self):
        if self.team is None:
            ErrorMessage("Load a team file or create new team.", self)
            return
        folder = self.openFolderNameDialog()
        if len(folder) < 1:
            return
        pdf = PDF_Gen()
        pdf.team_report(self.team, folder)
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setText(f"{self.team.name} team report has been saved.")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg_box.exec_()

    def pdf_student_report(self):
        if self.team is None:
            ErrorMessage("Load a team file or create new team.", self)
            return
        folder = self.openFolderNameDialog()
        if len(folder) < 1:
            return
        student = self.team.get_student(self.selected_student.text())
        if student is None:
            ErrorMessage("Student not found!", self)
            return
        pdf = PDF_Gen()
        pdf.student_report(student, folder)

        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setText(f"{student.full_name} report has been saved.")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg_box.exec_()

    def pdf_tournament_report(self):
        if self.team is None:
            ErrorMessage("Load a team file or create new team.", self)
            return
        folder = self.openFolderNameDialog()
        if len(folder) < 1:
            return

        tournament = self.team.get_tournament( self.tourney_selector.currentText())
        if tournament is None:
            ErrorMessage("Tournament not found!",self)
            return

        pdf = PDF_Gen()
        pdf.tournament_report(self.team, tournament, folder)

        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setText(f"{tournament} report has been saved.")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg_box.exec_()

    def pdf_event_report(self):
        if self.team is None:
            ErrorMessage("Load a team file or create new team.", self)
            return
        folder = self.openFolderNameDialog()
        if len(folder) < 1:
            return
        pdf = PDF_Gen()
        pdf.event_report(self.team, self.event_label.text(), folder)

        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setText(f"{self.event_label.text()} event report has been saved.")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg_box.exec_()

    def pdf_state_report(self):
        if self.team is None:
            ErrorMessage("Load a team file or create new team.", self)
            return
        folder = self.openFolderNameDialog()
        pdf = PDF_Gen()
        pdf.state_qualifier_report(self.team, folder)
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setText(f"{self.team.name} state qualifier report has been saved.")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg_box.exec_()

    def get_team_picture(self):

        file = self.openFileNameDialog("Image File(*.jpg)")
        if not file:
            return

        try:
            tournament = self.team.get_tournament(self.tourney_selector.currentText())
            tournament.photo = file
            pixmap = QPixmap(file).scaledToWidth(408)

            self.team_picture.setPixmap(pixmap)
        except Exception as e:
            ErrorMessage(e, self)

    @staticmethod
    def main(args):
        app = QApplication(args)
        mainwindow = Controller()
        mainwindow.setFixedHeight(900)
        mainwindow.setFixedWidth(1070)
        mainwindow.show()
        app.exec_()


# Main Guard
if __name__ == "__main__":
    Controller.main(sys.argv)
