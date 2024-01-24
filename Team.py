from Student import Student
from Tournament import Tournament

"""
The team class is the core of all the data contained in the program.
Team objects are what is saved in the save file.
They must  be initialized with a String representing the team name.

All other data is built as the user enters it. 

"""
class Team:

    def __init__(self, name):
        self.name = name
        self.students = []
        self.tournaments = []


    def new_student(self, fname, lname):
        stud = Student(fname,lname)
        if stud in self.students:

            return None
        else:
            self.students.append(stud)

        return stud

    def get_student(self, full_name):
        for student in self.students:
            if student.full_name == full_name:
                return student
        return None

    def add_tournament(self,tournament):
        self.tournaments.append[tournament]
        self.sort_tournaments()

    def get_tournament(self, host):
        for tournament in self.tournaments:
            if str(tournament) == str(host):
                return tournament

        return None

    def sort_tournaments(self):
        self.tournaments = Team.sort_tourney(self.tournaments)
    def tournament_report(self, school):
        # Returns a list of tuples (student name, [performances])
        report = []
        output = ""
        for student in self.students:
            perfs = student.get_perfs_by_tournament(school)
            report.append((student.full_name, perfs))
            for perf in perfs:
                output += f"{student.full_name}: {perf}\n"

        return report

    def event_report(self, event):
        # Returns a list of tuples (student name, [performances])
        report = []
        output = ""
        for student in self.students:
            perfs = student.get_perfs_by_event(event)
            report.append((student.full_name, perfs))
            for perf in perfs:
                output += f"{student.full_name}: {perf}\n"

        return report

    def delete_student(self, student):
        self.students.remove(student)

    def delete_tournament(self, tournament):
        self.tournaments.remove(tournament)
        for student in self.students:
            for performance in student.performances:
                if performance.tournament == tournament:
                    student.delete_performance(performance)
    def __str__(self):
        output = "*"*10
        output += f"{self.name}\n\n" + "*"*10
        for student in self.students:
            output += "#"*10
            output += "\n" + str(student)

        return output

    @staticmethod
    def sort_tourney(tournaments):
        front = []
        mid = []
        back = []

        if len(tournaments) < 2:
            return tournaments
        key = tournaments.pop()
        mid.append(key)
        for tournament in tournaments:
            if tournament.date < key.date:
                front.append(tournament)
            elif tournament.date > key.date:
                back.append(tournament)
            else:
                mid.append(tournament)
        if len(front) > 1:
            front = Team.sort_tourney(front)
        if len(back) > 1:
            back = Team.sort_tourney(back)

        complete = front + mid + back

        return complete
