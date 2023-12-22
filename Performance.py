from Tournament import Tournament

class Performance:
    def __init__(self, tournament, event):
        self.tournament = tournament
        self.event = event
        self.placement = "100"
        self.competitors = 6

    def add_result(self, placement):
        self.placement = placement

    def add_competitors(self, comp):
        self.competitors = int(comp)

    @property
    def qualifier(self):
        if self.competitors is None:
            return False
        min = 2
        rank_num = int(self.placement.split(" ")[0])
        qual_mins = [25, 40, 60, 80]
        if self.competitors > qual_mins[0]:
            min = 3
        if self.competitors > qual_mins[1]:
            min = 4
        if self.competitors > qual_mins[2]:
            min = 5
        if self.competitors > qual_mins[3]:
            min = 6

        if rank_num <= min:
            return True
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
