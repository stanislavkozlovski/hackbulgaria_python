class Ticket:
    def __init__(self, row: int, col: int, movie_name: str, movie_id: int, proj_type:str, date: str, hour: str, owner_id: int):
        self.row = row
        self.col = col
        self.movie_name = movie_name
        self.proj_type = proj_type
        self.owner_id = owner_id
        self.date = date
        self.hour = hour

    def __str__(self):
        return "Ticket for {movie_name}({proj_type}) on {date} at {time}. Seat position: {x}:{y}".format(
            movie_name=self.movie_name, proj_type=self.proj_type, date=self.date, time=self.hour, x=self.row, y=self.col
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.movie_name == other.movie_name and self.date == other.date and self.hour == other.hour
