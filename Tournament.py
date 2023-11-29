class Tournament:
    def __init__(self,school, date):
        self.school = school
        self.date = date

    def __str__(self):
        return  f"{self.date} -- {self.school}"