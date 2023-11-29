from Student import Student
from Team import Team
from Performance import Performance
from Tournament import Tournament
import sys
import pickle
class Controller:
    def __int__(self):
        pass



    def load(self, file):
        with open(file,'rb') as f:
            self.team = pickle.load(f)

    def save(self):
        file = self.team.name + ".4n6"
        with open(file, 'wb') as f:
            pickle.dump(self.team, f, protocol=pickle.HIGHEST_PROTOCOL)

    def new_team(self, team_name):
        self.team = Team(team_name)


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
                print(f"{ctrl.team.name}.4n6 saved.")

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






# Main Guard
if __name__ == "__main__":
    Controller.main(sys.argv)
