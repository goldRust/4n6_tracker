
class Round:
    def __init__(self,rank,qp):
        self.rank = -1
        self.qp = -1
        if rank.isnumeric():
            self.rank = int(rank)
        if qp.isnumeric():
            self.qp = int(qp)
        self.ballot = None

    def add_ballot(self, ballot):
        self.ballot = ballot

    @property
    def points(self):
        if self.rank == -1:
            return 0
        points = 6 - self.rank
        if points < 1:
            points = 1
        return points
