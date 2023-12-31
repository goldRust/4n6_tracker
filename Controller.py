import time

from Team import Team
from Performance import Performance
from Tournament import Tournament
from ErrorMessage import ErrorMessage
from Partner_Dialog import Partner_Dialog
from EditPerformanceDialog import EditPerformanceDialog
from Awards import Award
from PDF_Gen import PDF_Gen
from InfoMessage import InfoMessage
from CalendarDialog import CalendarDialog
from Welcome import Welcome
import sys, os
import pickle
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Controller(QMainWindow):
    def __init__(self):
        self.team = None

        super(Controller, self).__init__()
        loadUi("Forensics_Organizer.ui", self)

        self.setWindowIcon(QtGui.QIcon("4n6_icon.png"))
        self.setWindowTitle("4N6 Season Organizer")
        self.set_columns()
        self.set_interactive()

        Welcome(self).exec_()

    # Working on resize... very buggy right now.
    def resizeEvent(self, event):
        try:
            original_w = 1070
            original_h = 900
            percent_w = self.width() / original_w
            percent_h = self.height() / original_h
            x_center = int(self.width() /2)
            y_center = int(self.height()/2)
            self.tabWidget.resize(self.width() - 1, self.height() - 1)
            tables = [self.team_report, self.stud_report, self.tourney_report, self.event_report]
            for table in tables:
                table.resize(self.width() - 20, table.height())

            # self.add_performance_frame.setGeometry(0, self.height() + 100, self.width(), 200)
            # movable_items = [self.label_12, self.label_11, self.label_10, self.label_13, self.np_tourney, self.np_event, self.np_rank, self.add_perf_button]
            movable_items = []
            window_center_h = self.height() // 2
            window_center_w = self.width() // 2

            for item in movable_items:
                h_center = item.x() + item.width() // 2
                v_center = item.y() + item.height() // 2
                new_x = window_center_w - h_center
                new_y = window_center_h - v_center
                new_width = item.width()
                new_height = item.height()

                item.setGeometry(new_x, new_y, new_width, new_height)
                print(new_x)
        except Exception as e:
            print(e)

    def load_team_info(self):
        if self.team is None:
            ErrorMessage("Load a file or create a new team first.", self)
            return
        self.team_name.setText(self.team.name)
        self.team_name.resize(len(self.team.name)*24,24)
        # self.patch_tournaments()
        # self.patch_performances()
        self.update_team_report()
        self.team.students.sort()
        self.update_student_list()

        self.update_event_list()

        self.update_tourney_list()
        self.np_rank.clear()

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
            best = None
            best_rank = 101
            events = ""
            tournaments = ""
            tournament_count = 0
            for perf in student.performances:
                rank_int = int(perf.placement)
                if rank_int < best_rank:
                    best_rank = rank_int
                    best = perf
                if perf.event not in events:
                    events += f"{perf.event}, "
                if perf.tournament.school not in tournaments:
                    tournaments += f"{str(perf.tournament)} | "
                    tournament_count += 1
            if best is not None:
                best_str = f"{best.event} -- Rank: {best.placement} -- Competitors: {best.competitors} at {str(best.tournament)}"
            else:
                best_str = ""

            table.append([student.full_name, str(tournament_count), events, best_str])
        row_ind = 0
        col_ind = 0

        self.team_report.setRowCount(len(table))

        for row in table:
            # print(row)
            for col in row:
                self.team_report.setItem(row_ind, col_ind, QtWidgets.QTableWidgetItem(col))
                col_ind += 1

        for i in range(self.team_report.columnCount()):
            if self.team_report.item(i, 0):
                width = 120
                if len(self.team_report.item(0,i).text()) * 10 > width:
                    width = len(self.team_report.item(0,i).text()) * 10
                self.team_report.setColumnWidth(i, width)

    def update_student_report(self, student):
        if self.team is None:
            ErrorMessage("Load a file or create a new team first.", self)
            return
        if len(student) < 1:
            return
        self.selected_student.setText(student)
        self.stud_report.setRowCount(len(self.team.get_student(student).performances))
        perf_ind = 0
        self.team.get_student(student).sort_performances()
        for perf in self.team.get_student(student).performances:
            rank = perf.placement
            if rank == -1 or rank == "" or rank == "100":
                rank = "Unranked"
            state_qualifier = ""
            print("Checking Qualified")
            if perf.qualifier:
                state_qualifier = perf.qualifier
                print("Qualified")

            rank = str(rank) + state_qualifier
            self.stud_report.setItem(perf_ind, 0, QtWidgets.QTableWidgetItem(perf.event))
            self.stud_report.setItem(perf_ind, 1, QtWidgets.QTableWidgetItem(rank))
            self.stud_report.setItem(perf_ind, 2, QtWidgets.QTableWidgetItem(str(perf.tournament)))

            perf_ind += 1

        self.add_performance_frame.setEnabled(True)
        self.np_tourney.setEnabled(True)

        self.delete_student.setEnabled(True)


        for i in range(self.stud_report.columnCount()):
            if self.stud_report.item(i, 0):
                width = 160
                if len(self.stud_report.item(0,i).text()) * 10 > width:
                    width = len(self.stud_report.item(0,i).text()) * 10
                self.stud_report.setColumnWidth(i, width)

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
                    if rank == -1 or rank == "100":
                        rank = "Unranked"
                    state_qualifier = ""
                    if perf.qualifier:
                        state_qualifier = perf.qualifier
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

    # Used to update old files in which the performance class didn't have the competitors attribute.
    def patch_performances(self):
        print("Patching performances")
        for stud in self.team.students:
            for i in range(len(stud.performances)):
                new_perf = Performance(stud.performances[i].tournament, stud.performances[i].event)
                new_perf.placement = stud.performances[i].placement
                if stud.performances[i].competitors:
                    new_perf.competitors = stud.performances[i].competitors
                stud.performances[i] = new_perf
                print(stud.performances[i].placement)
                if len(stud.performances[i].placement) < 1:
                    stud.performances[i].placement = "100"
                if not stud.performances[i].placement.isnumeric():
                    num = stud.performances[i].placement.split(" ")[0]
                    print(num)
                    stud.performances[i].placement = num


        print("Patch complete.")

    def update_tournament_report(self, host):
        if self.team is None:
            ErrorMessage("Load a file or create a new team first.", self)
            return

        if len(host) < 1:
            return

        tournament = self.team.get_tournament(host)
        table = []
        longest_name = 0
        longest_event = 0
        longest_rank = 0
        sweeps_total = 0
        for student in self.team.students:
            if longest_name < len(student.full_name) * 10:
                longest_name = len(student.full_name) * 10
            for perf in student.performances:
                state_qualifier = ""
                if str(perf.tournament) == host:
                    if longest_event < len(perf.event) * 10:
                        longest_event = len(perf.event) *10

                    rank = perf.placement

                    if rank == -1 or rank == "100":
                        rank = "Unranked"
                    if perf.qualifier:
                        state_qualifier = perf.qualifier
                    rank = str(rank) + state_qualifier
                    if longest_rank < len(rank) * 10:
                        longest_rank = len(rank) * 10

                    sweeps_total += perf.sweeps_points()
                    table.append([student.full_name, perf.event, rank, str(perf.sweeps_points())])
        table.append(["", "", "TOTAL SWEEPS:", str(sweeps_total)])
        self.tourney_report.setRowCount(len(table))
        row_ind = 0
        col_ind = 0

        for row in table:
            for col in row:
                self.tourney_report.setItem(row_ind, col_ind, QtWidgets.QTableWidgetItem(col))
                col_ind += 1

            col_ind = 0
            row_ind += 1
        self.tourney_report.setColumnWidth(0, longest_name)
        self.tourney_report.setColumnWidth(1, longest_event)
        self.tourney_report.setColumnWidth(2, longest_rank)
        self.tourney_report.setColumnWidth(3, 5 * 12)
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
        # Tournament report click to edit
        self.tourney_report.cellClicked.connect(self.edit_performance_tr)
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

        # Change tournament date
        self.change_date.clicked.connect(self.change_tourney_date)

        # Remove Photo
        self.remove_photo_button.clicked.connect(self.remove_photo)



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
            self.stud_selector.setCurrentText(student.full_name)
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
        if self.date_label.text() == "Date" or self.date_label.text() == "Date:":
            ErrorMessage("Select the date of the tournament.\nClick 'Select Date'",self)
            return
        date = self.date_label.text().split(": ")[1]
        if len(host) < 1:
            ErrorMessage("Host school name required.", self)
            return
        new_tourney = Tournament(host, date)
        self.team.tournaments.append(new_tourney)
        self.tourney_selector.addItem(str(new_tourney))
        self.np_tourney.addItem(str(new_tourney))
        self.nt_host.clear()
        self.date_label.setText("Date:")

    def change_tourney_date(self):
        date = CalendarDialog(self).exec_()

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
        placement = self.np_rank.text()
        if not placement.isnumeric():
            placement = "100"
        performance.placement = placement
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
        tournaments = [str(tournament) for tournament in self.team.tournaments]
        event = self.stud_report.item(row, 0).text()
        tournament = self.stud_report.item(row, 2).text()
        perf = (self.stud_report.item(row, 0).text(), self.stud_report.item(row, 1).text(),
                self.stud_report.item(row, 2).text())
        student = self.team.get_student(self.stud_selector.currentText())

        rebuild = EditPerformanceDialog(student, event, tournament, tournaments, row, self).exec_()
        if rebuild:
            print("Clearing old")
            self.stud_report.clearContents()
            print("Entering new")
            self.update_student_report(self.selected_student.text())
            print("Updated")

    def edit_performance_tr(self, row, col):
        tournaments = [str(tournament) for tournament in self.team.tournaments]
        student = self.team.get_student(self.tourney_report.item(row, 0).text())
        event = self.tourney_report.item(row,1).text()
        tournament = self.tourney_selector.currentText()
        perf = (self.tourney_report.item(row, 0).text(), self.tourney_report.item(row, 1).text(),
                self.tourney_report.item(row, 2).text())


        rebuild = EditPerformanceDialog(student, event, tournament, tournaments, row, self).exec_()
        if rebuild:
            print("Clearing old")
            self.tourney_report.clearContents()
            print("Entering new")
            self.update_tournament_report(self.tourney_selector.currentText())
            print("Updated")

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
        InfoMessage(f"{file} has been saved.", self)

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
        if self.team is None:
            sys.exit()
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
        retval = InfoMessage(f"{tournament} awards file has been saved.",self).exec_()

    def pdf_team_report(self):
        if self.team is None:
            ErrorMessage("Load a team file or create new team.", self)
            return
        folder = self.openFolderNameDialog()
        if len(folder) < 1:
            return
        pdf = PDF_Gen()
        pdf.team_report(self.team, folder)
        retval = InfoMessage(f"{self.team.name} team report has been saved.", self)

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
        retval = InfoMessage(f"{student.full_name} report has been saved.",self)

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
        retval = InfoMessage(f"{tournament} report has been saved.",self)

    def pdf_event_report(self):
        if self.team is None:
            ErrorMessage("Load a team file or create new team.", self)
            return
        folder = self.openFolderNameDialog()
        if len(folder) < 1:
            return
        pdf = PDF_Gen()
        pdf.event_report(self.team, self.event_label.text(), folder)
        retval = InfoMessage(f"{self.event_label.text()} event report has been saved.",self)

    def pdf_state_report(self):
        if self.team is None:
            ErrorMessage("Load a team file or create new team.", self)
            return
        folder = self.openFolderNameDialog()
        pdf = PDF_Gen()
        pdf.state_qualifier_report(self.team, folder)
        retval = InfoMessage(f"{self.team.name} state qualifier report has been saved.", self)

    def get_team_picture(self):

        file = self.openFileNameDialog("Image Files (*.png *.jpg *.bmp)")
        if not file:
            return

        try:
            tournament = self.team.get_tournament(self.tourney_selector.currentText())
            tournament.photo = file
            pixmap = QPixmap(file).scaledToWidth(408)

            self.team_picture.setPixmap(pixmap)
        except Exception as e:
            ErrorMessage(e, self)

    def remove_photo(self):
        tournament = self.team.get_tournament(self.tourney_selector.currentText())
        tournament.photo = None
        print("Updating Tournament")
        self.update_tournament_report(self.tourney_selector.currentText())

    @staticmethod
    def main(args):
        app = QApplication(args)
        mainwindow = Controller()
        mainwindow.setFixedHeight(884)
        mainwindow.setFixedWidth(1067)
        mainwindow.show()
        app.exec_()


# Main Guard
if __name__ == "__main__":
    Controller.main(sys.argv)
