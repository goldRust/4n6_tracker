from Student import Student
from Tournament import Tournament

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

    def get_tournament(self, host):
        for tournament in self.tournaments:
            if str(tournament) == str(host):
                return tournament

        return None

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

    def __str__(self):
        output = "*"*10
        output += f"{self.name}\n\n" + "*"*10
        for student in self.students:
            output += "#"*10
            output += "\n" + str(student)

        return output