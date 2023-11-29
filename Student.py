from Performance import Performance
class Student:
    def __init__(self, fname, lname):
        self.first_name = fname
        self.last_name = lname
        self.performances = []

    @property
    def first(self):
        return self.first_name

    @property
    def last(self):
        return self.last_name

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def add_performance(self, performance):
        self.performances.append(performance)

    def get_perfs_by_event(self,event):
        perfs = []
        for perf in self.performances:
            if perf.event == event:
                perfs.append(perf)
        return perfs

    def get_perfs_by_tournament(self, school):
        perfs = []
        for perf in self.performances:
            if perf.tournament.school == school:
                perfs.append(perf)
        return perfs

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.full_name == other.full_name
        return False

    def __str__(self):
        output = ""
        output += self.full_name + "\n"

        for perf in self.performances:
            output += "\t" + str(perf) + "\n"

        return output


