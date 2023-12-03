class Tournament:
    def __init__(self,school, date):
        self.school = school
        self.date = date

    def __eq__(self, other):
        if isinstance(other, Tournament):
            return self.school == other.school and self.date == other.date
        return False

    def __str__(self):
        return  f"{self.date} -- {self.school}"