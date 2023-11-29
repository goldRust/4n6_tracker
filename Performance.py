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

    def __str__(self):
        output = ""
        output += self.event
        if self.placement != -1:
            output += f" -- #{self.placement} "
        else:
            output += " -- Unranked "
        output += f"-- {self.tournament}"
        return output
