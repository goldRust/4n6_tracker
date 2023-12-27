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
        return performance

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

    def delete_performance(self, performance):
        if performance in self.performances:
            self.performances.remove(performance)
        else:
            print("Performance not found.")

    def get_performance(self, performance):
        if performance in self.performances:
            return self.performances[self.performances.index(performance)]

    def sort_performances(self):
        self.performances = Student.perf_sort(self.performances)

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.full_name == other.full_name
        return False

    def __lt__(self, other):
        if self.last_name == other.last_name:
            return self.first_name < other.first_name
        return self.last_name < other.last_name

    def __gt__(self, other):
        if self.last_name == other.last_name:
            return self.first_name > other.first_name
        return self.last_name > other.last_name

    def __le__(self, other):
        if self.last_name == other.last_name:
            return self.first_name <= other.first_name
        return self.last_name <= other.last_name

    def __ge__(self, other):
        if self.last_name == other.last_name:
            return self.first_name >= other.first_name
        return self.last_name >= other.last_name

    def __str__(self):
        output = ""
        output += self.full_name + "\n"

        for perf in self.performances:
            output += "\t" + str(perf) + "\n"

        return output

    @staticmethod
    def perf_sort(perf_list):

        front = []
        mid = []
        back = []
        if len(perf_list) <2:
            return perf_list
        key = perf_list.pop()
        mid.append(key)
        for perf in perf_list:
            if int(perf.placement) > int(key.placement):
                back.append(perf)
            elif int(perf.placement) < int(key.placement):
                front.append(perf)
            else:
                mid.append(perf)
        if len(front)>1:
            front = Student.perf_sort(front)
        if len(back)>1:
            back = Student.perf_sort(back)

        complete = front + mid + back
        return complete

