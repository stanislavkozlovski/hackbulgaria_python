class Airline:
    def __init__(self, flights: ['Flight']):
        self.flights = [flight for flight in flights if not flight.declined]  # add only the flights that are not declined

    def decline_flight(self, flight: 'Flight'):
        flight.decline_flight()
        self.flights.remove(flight)

    # TODO: Look over the possibility of higher-order functions
    # def get_flights(self, term):
    #     return [flight for flight in self.flights if term]

    def get_flights_for(self, date):
        """ Get all the flights that are on the given date """
        return [flight for flight in self.flights if flight.start_time == date]

    def get_flights_before(self, date):
        """ Get all the flights that are before the given date """
        return [flight for flight in self.flights if flight.start_time < date]

    def get_flights_from(self, city_origin: str, date: 'Date'=None):
        """ Get all the flights flying from a given place, with the added possibility to have said
                    flights be on a specific date"""
        if date:
            return [flight for flight in self.flights if flight.from_dest == city_origin and flight.start_time == date]

        return [flight for flight in self.flights if flight.from_dest == city_origin]

    def get_flights_to(self, destination: str, date: 'Date'=None):
        """ Get all the flights to a given destination, with the added possibility to have said
            flights be on a specific date"""
        if date:
            return [flight for flight in self.flights if flight.to_dest == destination and flight.start_time == date]

        return [flight for flight in self.flights if flight.to_dest == destination]

    def get_terminal_flights(self, terminal: 'Terminal', date: 'Date'=None, to_dest: str=None):
        """
        Get all the flights from a given terminal, with the added possibility to
        have those flights be on a specific date or to a specific destination, depending if the associated
        parametersa are filled.
        """
        if date:
            return [flight for flight in self.flights if flight.terminal == terminal and flight.start_time == date]
        elif to_dest:
            return [flight for flight in self.flights if flight.terminal == terminal and flight.to_dest == to_dest]

        return [flight for flight in self.flights if flight.terminal == terminal]

    def get_flights_within_duration(self, flight: 'Flight'):
        """ Get all flights whose durations are within the given flight's duration"""
        maximum_duration = flight.get_flight_duration()
        return [flight for flight in self.flights if flight.get_flight_duration() <= maximum_duration]

    def get_flights_on_date_lt_hours(self, hours: str):
        """ Get all the flights whose duration is less than the given duration, IN HOURS"""
        hours = int(hours)  # convert to int
        return [flight for flight in self.flights if self.get_flight_hours_duration(flight) < hours]

    def get_passengers_to_dest(self, destination: str):
        """ Get all the passengers that are flying to the given destination """
        return [passenger for flight in self.flights if flight.to_dest == destination for passenger in flight.passengers]
    
    def get_passengers_from_terminal(self, terminal: 'Terminal'):
        """ Get all passengers that are flying from the given terminal. """
        return [passenger for flight in self.flights if flight.terminal == terminal for passenger in flight.passengers]

    def get_flights_with_passengers(self, size: int):
        """ Get all the flights whose passenger count is greater than the given size """
        return [flight for flight in self.flights if flight.passengers_count > size]

    def get_reservations_to_destination(self, destination: str):
        """ Get all the reservations that go to the given destination """
        return [reservation for flight in self.flights
                if flight.to_dest == destination for reservation in flight.reservations]

    def get_flight_hours_duration(self, flight: 'Flight'):
        """ Return the duration of a flight in hours """
        flight_duration = flight.get_flight_duration()

        hours = (flight_duration.years * Date.HOURS_IN_A_YEAR
                  + flight_duration.months * Date.HOURS_IN_A_MONTH
                  + flight_duration.days * Date.HOURS_IN_A_DAY
                  + flight_duration.hours
                  + flight_duration.minutes / 60)

        return hours


class Flight:
    def __init__(self, start_time: 'Date', end_time: 'Date', max_passengers: int,
                 from_dest: str, to_dest: str, terminal: 'Terminal', declined: bool):
        self.start_time = start_time
        self.end_time = end_time
        self.max_passengers = max_passengers
        self.from_dest = from_dest
        self.to_dest = to_dest
        self.terminal = terminal
        self.declined = declined
        self.passengers = []  # type: ['Passenger']
        self.passengers_count = len(self.passengers)
        self.reservations = []  # type: ['Reservation']

    def decline_flight(self):
        self.declined = True

    def has_empty_seats(self):
        return self.max_passengers > self.passengers_count

    def get_passenger_reservations(self):
        return self.reservations

    def get_flight_duration(self):
        return self.end_time - self.start_time

    def add_reservations(self, reservations: ['Reservation']):
        self.reservations.extend(reservations)

    def add_passengers(self, passengers: ['Passenger']):
        self.passengers.extend(passengers)
        self.passengers_count = len(self.passengers)  # update passengers count

    def get_passengers_under_18(self):
        return [passenger for passenger in self.passengers if passenger.age < 18]


class Terminal:
    def __init__(self, number: int, max_flights: int):
        self.max_flights = max_flights
        self.number = number

    def __eq__(self, other):
        return self.number == other.number


class Passenger:
    def __init__(self, first_name: str, last_name: str, flight: Flight, age: int):
        self.first_name = first_name
        self.last_name = last_name
        self.flight = flight
        self.age = age


class Reservation:
    def __init__(self, flight: Flight, passenger: Passenger, accepted: bool):
        self.flight = flight
        self.passenger = passenger
        self.accepted = accepted

class Date:

    HOURS_IN_A_YEAR = 8765.81277
    HOURS_IN_A_MONTH = 730.484398
    HOURS_IN_A_DAY = 24

    def __init__(self, day: int, month: int, year: int, hour: str):
        self.day = day
        self.month = month
        self.year = year
        self.hour = hour

    def __gt__(self, other):
        """
         Compare the dates, first by their year, then by month, then by day, then by hour. Where if any one of them
         is bigger in that order and it's previous are equal, return True. (the date is greater, newer)
        """
        if self.year > other.year:
            return True
        elif self.year == other.year:
            if self.month > other.month:
                return True
            elif self.month == other.month:
                if self.day > other.day:
                    return True
                elif self.day == other.day:
                    if self.hour > other.hour:
                        return True
            # will go downwards to return false
        return False
        # TODO: Ask which one is better
        # return ((self.year > other.year)
        #        or (self.year == other.year and self.month > other.month)
        #         or (self.year == other.year and self.month == other.month and self.day > other.day)
        #         or (self.year == other.day and self.month == other.month and self.day == other.day and self.hour > other.hour))

    def __lt__(self, other):
        return not self.__gt__(other)

    def __ge__(self, other):
        return (self.year > other.year) or (self.month > other.month) or (self.day > other.day) or (self.hour >= self.hour)

    def __le__(self, other):
        return (self.year < other.year) or (self.month < other.month) or (self.day < other.day) or (self.hour <= self.hour)

    def __eq__(self, other):
        return [self.day, self.month, self.year] == [other.day, other.month, other.year]

    def __sub__(self, other):
        hours, minutes = tuple([int(x) for x in self.hour.split(':')])
        other_hours, other_minutes = tuple([int(x) for x in other.hour.split(':')])

        minute_difference = minutes-other_minutes
        if minute_difference < 0:
            # 1:20 - 0:30
            # 4:40 - 3:59 = 40-59 = -19 == 60-19 == 41 == 0:41
            hours -= 1
            minute_difference = 60 - abs(minute_difference)

        hour_difference = hours-other_hours
        day = self.day
        if hour_difference < 0:
            day -= 1
            hour_difference = 24 - abs(hour_difference)

        day_difference = day - other.day
        month = self.month
        if day_difference < 0:
            month -= 1
            day_difference = 31 - abs(day_difference)

        month_difference = month - other.month
        year = self.year
        if month_difference < 0:
            year -= 1
            month_difference = 12 - abs(month_difference)

        year_difference = year - other.year

        return Duration(years=year_difference, months=month_difference,
                        days=day_difference, hours=hour_difference, minutes=minute_difference)


class Duration:
    def __init__(self, years: int, months: int, days: int, hours: int, minutes: int):
        self.years = years
        self.months = months
        self.days = days
        self.hours = hours
        self.minutes = minutes

    def __eq__(self, other):
        return (self.years == other.years and self.months == other.months
                and self.days == other.days and self.hours == other.hours
                and self.minutes == other.minutes)

    def __gt__(self, other):
        return (self.years > other.years or self.months > other.months
                or self.days > other.days or self.hours > other.hours
                or self.minutes > other.minutes)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __lt__(self, other):
        return not self.__gt__(other)


