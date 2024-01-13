from Tournament import Tournament
from Round import  Round

'''
The performance class is utlized by the Student class and is the base of nearly all the data in the program.

'''
class Performance:
    def __init__(self, tournament, event):
        self.tournament = tournament
        self.event = event
        self.placement = "100"
        self.competitors = 6
        self.rounds = []
        self.partner = None

    def add_result(self, placement):
        self.placement = placement

    def add_competitors(self, comp):
        self.competitors = int(comp)

    def add_round(self, rank, qp):
        self.rounds.append(Round(rank, qp))

    def sweeps_points(self):
        total = 0
        for round in self.rounds:
            total += round.points
        return total

    def add_partner(self, partner):

        self.partner = partner



    def get_partner(self):
        return self.partner

    def duplicate(self):
        new_performance = Performance(self.tournament, self.event)
        new_performance.placement = self.placement
        new_performance.partner = self.partner
        print(self.partner)
        new_performance.competitors = self.competitors
        new_performance.rounds = self.rounds
        return new_performance

    @property
    def qualifier(self):
        if self.competitors is None:
            return False
        min = 2
        rank_num = int(self.placement.split(" ")[0])
        qual_mins = [25, 40, 60, 80]
        fest_mins =  [10, 15, 19]
        if self.competitors > qual_mins[0]:
            min = 3
        if self.competitors > qual_mins[1]:
            min = 4
        if self.competitors > qual_mins[2]:
            min = 5
        if self.competitors > qual_mins[3]:
            min = 6

        if rank_num <= min:
            return " *State Champs Qualified* "

        if self.competitors > fest_mins[0]:
            min = 4

        if self.competitors > fest_mins[1]:
            min = 5

        if self.competitors > fest_mins[2]:
            min = 6

        if rank_num <= min:
            return " *Festival Qualified* "
        else:
            return False

    @property
    def result(self):
        return self.placement

    def __eq__(self, other):
        if isinstance(other, Performance):

            return str(self) == str(other)
        print(f"{other} is not a Performance!")
        return False

    def __str__(self):
        output = ""
        output += self.event

        output += f" -- {self.tournament}"
        return output
