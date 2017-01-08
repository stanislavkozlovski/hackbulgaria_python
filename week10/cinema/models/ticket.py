class Ticket:
    def __init__(self, row: int, col: int, movie_name: int, date: str, hour: str):
        self.row = row
        self.col = col
        self.movie_name = movie_name
        self.date = date
        self.hour = hour

    def __str__(self):
        return "Ticket for {movie_name} on {date} at {time}. Seat position: {x}:{y}".format(
            movie_name=self.movie_name, date=self.date, time=self.hour, x=self.row, y=self.col
        )

    def __eq__(self, other):
        return self.movie_name == other.movie_name and self.date == other.date and self.hour == other.hour