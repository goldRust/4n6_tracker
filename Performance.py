from Tournament import Tournament

class Performance:
    def __init__(self, tournament, event):
        self.tournament = tournament
        self.event = event
        self.placement = -1

    def add_result(self, placement):
        self.placement = placement

    @property
    def result(self):
        return self.placement

    def __eq__(self, other):
        if isinstance(other, Performance):
            return str(self) == str(other)
        return False

    def __str__(self):
        output = ""
        output += self.event

        output += f"-- {self.tournament}"
        return output
