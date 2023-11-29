from Student import Student

class Team:

    def __init__(self, name):
        self.name = name
        self.students = []

    def new_student(self, fname, lname):
        stud = Student(fname,lname)
        if stud in self.students:
            print(f"{stud.full_name} is already on the team!")
            stud = self.get_student(fname, lname)
        else:
            self.students.append(stud)
            print(f"{stud.full_name} has been added to the team!")
        return stud

    def get_student(self, fname, lname):
        for student in self.students:
            if student.first_name == fname and student.last_name == lname:
                return student

        return "Student not found."

    def tournament_report(self, school):
        # Returns a list of tuples (student name, [performances])
        report = []
        output = ""
        for student in self.students:
            perfs = student.get_perfs_by_tournament(school)
            report.append((student.full_name, perfs))
            for perf in perfs:
                output += f"{student.full_name}: {perf}\n"


        print(output)
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
        print(output)
        return report

    def __str__(self):
        output = "*"*10
        output += f"{self.name}\n\n" + "*"*10
        for student in self.students:
            output += "#"*10
            output += "\n" + str(student)

        return output