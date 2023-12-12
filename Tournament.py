class Tournament:
    def __init__(self,school, date):
        self.school = school
        self.date = date
        self.photo = None

    def __eq__(self, other):
        print(f"Comparing: {self} : {other}")
        if isinstance(other, Tournament):
            return str(self) == str(other)
        return False

    def __str__(self):
        return  f"{self.school} -- {self.date}"