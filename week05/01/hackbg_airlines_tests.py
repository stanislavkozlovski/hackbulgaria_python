from hackbg_airlines import *
import unittest


class AirlineTests(unittest.TestCase):

    def setUp(self):
        """ Some variables we'll be using in our tests"""
        # Terminals for flights
        self.terminal_1 = Terminal(1, 20)
        self.terminal_2 = Terminal(2, 30)


        # Sample flights
        self.f = Flight(start_time=Date(29, 11, 2016, hour='13:20'), end_time=Date(29, 11, 2016, hour='15:30'),
                   max_passengers=90, from_dest="Sofia", to_dest="London", terminal=self.terminal_2,
                   declined=False)

        self.f2 = Flight(start_time=Date(29, 10, 2016, hour='10:20'), end_time=Date(30, 11, 2016, hour='23:00'),
                   max_passengers=100, from_dest="London", to_dest="Sofia", terminal=self.terminal_2,
                   declined=False)

        self.f3 = Flight(start_time=Date(30, 11, 2016, hour='14:50'), end_time=Date(30, 11, 2016, hour='18:15'),
                   max_passengers=110, from_dest="Madrid", to_dest="Barcelona", terminal=self.terminal_2,
                   declined=False)

        self.f4 = Flight(start_time=Date(31, 11, 2016, hour='20:20'), end_time=Date(1, 12, 2016, hour='21:21'),
                   max_passengers=150, from_dest="Burgas", to_dest="Paris", terminal=self.terminal_2,
                   declined=False)

        ''' Passengers '''
        # LONDON
        self.london_passengers = [Passenger('Foo', 'Bar', self.f, 17), Passenger('Bar', 'Foo', self.f, 19)]
        self.london_reservations = [Reservation(self.f, self.london_passengers[0], True),
                               Reservation(self.f, self.london_passengers[1], True)]
        self.f.add_passengers(self.london_passengers)
        self.f.add_reservations(self.london_reservations)
        # SOFIA
        self.sofia_passengers = [Passenger('Foo', 'Bar', self.f2, 21), Passenger('Bar', 'Foo', self.f2, 19)]
        self.sofia_reservations = [Reservation(self.f2, self.sofia_passengers[0], True),
                              Reservation(self.f2, self.sofia_passengers[1], True)]
        self.f2.add_passengers(self.sofia_passengers)
        self.f2.add_reservations(self.sofia_reservations)
        # BARCELONA
        self.barcelona_passengers = [Passenger('Lo', 'Dash', flight=self.f3, age=34),
                                Passenger('Dash', 'Lo', flight=self.f3, age=40)]
        self.barcelona_reservations = [Reservation(self.f3, self.barcelona_passengers[0], True),
                                  Reservation(self.f3, self.barcelona_passengers[1], True)]
        self.f3.add_passengers(self.barcelona_passengers)
        self.f3.add_reservations(self.barcelona_reservations)

        # Our Airline class holding our flights
        self.airline_dummy = Airline(flights=[self.f, self.f2, self.f3, self.f4])


    """ TESTS """

    '''###################### PASSENGER CLASS TESTS #############################'''

    def test_passenger_class_constructor(self):
        f = Flight(start_time=Date(29, 11, 2016, hour='12:20'), end_time=Date(29, 11, 2016, hour='15:30'),
                   max_passengers=120, from_dest="Sofia", to_dest="London", terminal=Terminal(2, 30),
                   declined=False)
        p = Passenger(first_name="Rositsa", last_name="Zlateva", flight=f, age=22)

        self.assertTrue(isinstance(p, Passenger))
        self.assertTrue(isinstance(p.flight, Flight))

    '''###################### RESERVATION CLASS TESTS #############################'''

    def test_reservation_class_constructor(self):
        f = Flight(start_time=Date(29, 11, 2016, hour='12:20'), end_time=Date(29, 11, 2016, hour='15:30'),
                   max_passengers=120, from_dest="Sofia", to_dest="London", terminal=Terminal(2, 30),
                   declined=False)
        p = Passenger(first_name="Rositsa", last_name="Zlateva", flight=f, age=22)
        r = Reservation(flight=f, passenger=p, accepted=True)

        self.assertTrue(r, Reservation)
        self.assertTrue(r.flight, Flight)
        self.assertTrue(r.passenger, Passenger)

    '''###################### TERMINAL CLASS TESTS #############################'''

    def test_terminal_class_constructor(self):
        t = Terminal(number=1, max_flights=20)

        self.assertTrue(isinstance(t, Terminal))

    def test_terminal_comparison(self):
        ''' test the terminal comparison, which should work by it's number'''
        t_1 = Terminal(number=1, max_flights=20)
        t_2 = Terminal(number=1, max_flights=20)
        t_3 = Terminal(number=12, max_flights=20)

        self.assertEqual(t_1, t_2)
        self.assertNotEqual(t_1, t_3)
        self.assertNotEqual(t_2, t_3)

    '''###################### DATE CLASS TESTS #############################'''

    def test_date_class_constructor(self):
        d = Date(day=29, month=11, year=2016, hour='12:20')

        self.assertTrue(d, Date)

    def test_date_equals(self):
        ''' test if two dates are equal'''
        d_1 = Date(10, 10, 2016, '10:10')
        d_2 = Date(10, 10, 2016, '10:10')

        self.assertEqual(d_1, d_2)

    def test_date_comparison(self):
        ''' test expected values wheh comparing different dates'''
        d_1 = Date(10, 10, 2016, '10:10')
        d_2 = Date(10, 11, 2016, '10:10')
        self.assertEqual(d_1 > d_2, False)
        self.assertTrue(d_1 != d_2)

        d_1 = Date(10, 10, 2016, '10:10')
        d_2 = Date(10, 10, 2016, '10:10')
        self.assertEqual(d_1 > d_2, False)
        self.assertEqual(d_1 >= d_2, True)
        self.assertEqual(d_1 <= d_2, True)

        d_1 = Date(10, 10, 2016, '10:10')
        d_2 = Date(10, 10, 2018, '10:09')
        self.assertEqual(d_1 > d_2, False)
        self.assertEqual(d_1 < d_2, True)

    '''###################### FLIGHT CLASS TESTS #############################'''

    def test_flight_class_constructor(self):
        f = Flight(start_time=Date(29, 11, 2016, hour='12:20'), end_time=Date(29, 11, 2016, hour='15:30'),
                   max_passengers=120, from_dest="Sofia", to_dest="London", terminal=Terminal(2, 30),
                   declined=False)

        self.assertTrue(isinstance(f, Flight))

    def test_flight_get_passengers_under_18(self):
        """ Get all the passengers from a flight who are under 18 years old """
        self.assertEqual(len(self.f.get_passengers_under_18()), 1)
        self.assertEqual(len(self.f2.get_passengers_under_18()), 0)

    def test_flight_get_passengers_reservations(self):
        """ Get all the reservations on a given flight"""
        self.assertEqual(self.f.get_passenger_reservations(), self.london_reservations)
        self.assertEqual(self.f4.get_passenger_reservations(), [])

    def test_flight_has_empty_seats(self):
        """ Says if a flight has any empty seats """
        self.assertTrue(self.f.has_empty_seats())
        self.f4.add_passengers([Passenger('Dummy', 'Guy', self.f4, 50)] * self.f4.max_passengers)
        self.assertFalse(self.f4.has_empty_seats())

    '''###################### AIRLINE CLASS TESTS #############################'''

    def test_airline_class_constructor(self):
        self.assertTrue(isinstance(self.airline_dummy, Airline))
        self.assertEqual(len(self.airline_dummy.flights), 4)
        self.assertEqual(self.airline_dummy.flights[-1].to_dest, "Paris")

    def test_airline_get_flights_for(self):
        """test the function that gets the flights for a specific date"""
        self.assertEqual(self.airline_dummy.get_flights_for(Date(29, 11, 2016, '00:00')), [self.f])
        self.assertEqual(self.airline_dummy.get_flights_for(Date(29, 4314, 2016, '00:00')), [])

    def test_airline_get_flights_before(self):
        """test the function that gets the flights BEFORE a specific date"""
        self.assertEqual(self.airline_dummy.get_flights_before(Date(29, 11, 2016, '23:59')), [self.f, self.f2])
        self.assertEqual(self.airline_dummy.get_flights_before(Date(29, 11, 24141, '23:59')),
                         [self.f, self.f2, self.f3, self.f4])

    def test_airline_get_flights_from(self):
        """
        test the function that gets the flights from a specific city
        Adding a date as an argument will get all the flights from a specific city on that date
        """
        self.assertEqual(self.airline_dummy.get_flights_from('Burgas'), [self.f4])
        self.assertEqual(self.airline_dummy.get_flights_from('NowhereLand'), [])

        # with dates
        self.assertEqual(
            self.airline_dummy.get_flights_from(city_origin='Burgas', date=self.f4.start_time),
            [self.f4]
        )

        self.assertEqual(
            self.airline_dummy.get_flights_from(city_origin='Burgas', date=self.f3.start_time),
            []
        )

    def test_airline_get_flights_to(self):
        """
       test the function that gets the flights flying to a specific city
       Adding a date as an argument will get all the flights flying to a specific city on that date
       """
        self.assertEqual(self.airline_dummy.get_flights_to('Paris'), [self.f4])
        self.assertEqual(self.airline_dummy.get_flights_to('NowhereLand'), [])

    def test_airline_get_flights_to_with_date(self):
        # with dates
        self.assertEqual(
            self.airline_dummy.get_flights_to(destination='Paris', date=self.f4.start_time),
            [self.f4]
        )
        self.assertEqual(
            self.airline_dummy.get_flights_to(destination='Paris', date=self.f3.start_time),
            []
        )

    def test_airline_get_terminal_flights(self):
        """ Get all the flights that are flying from a specific terminal """
        terminal_3 = Terminal(number=3, max_flights=20)

        # all our dummy flights come from terminal 2
        self.assertEqual(
            self.airline_dummy.get_terminal_flights(terminal=self.terminal_2),
            [self.f, self.f2, self.f3, self.f4]
        )
        self.assertEqual(
            self.airline_dummy.get_terminal_flights(terminal=terminal_3),
            []
        )

    def test_airline_get_terminal_flights_on(self):
        """ Get all the flights that are flying from a specific terminal on a given date"""
        terminal_3 = Terminal(number=3, max_flights=20)
        self.assertEqual(
            self.airline_dummy.get_terminal_flights(terminal=self.terminal_2, date=self.f2.start_time),
            [self.f2]
        )
        self.assertEqual(
            self.airline_dummy.get_terminal_flights(terminal=terminal_3, date=Date(0, 0, 0000, '00:00')),
            []
        )

    def test_airline_terminal_flights_to_dest(self):
        """ Get all the flights that are flying from a specific terminal and headed to the given city"""
        test_destination = 'Barcelona'
        self.assertEqual(self.airline_dummy.get_terminal_flights(terminal=self.terminal_2, to_dest=test_destination),
                         [self.f3])

        self.assertEqual(self.airline_dummy.get_terminal_flights(terminal=self.terminal_1, to_dest=test_destination),
                         [])

    def test_airline_flight_duration(self):
        """ Get the flight duration for each flight"""
        year_duration_flight = Flight(start_time=Date(31, 11, 2016, hour='20:20'), end_time=Date(1, 1, 2018, hour='01:01'),
                         max_passengers=150, from_dest="Burgas", to_dest="Paris",
                         terminal=self.terminal_2,
                         declined=False)
        self.assertEqual(year_duration_flight.get_flight_duration(), Duration(years=1, months=1, days=0, hours=4, minutes=41))
        self.assertEqual(self.f.get_flight_duration(), Duration(years=0, months=0, days=0, hours=2, minutes=10))
        self.assertEqual(self.f2.get_flight_duration(), Duration(years=0, months=1, days=1, hours=12, minutes=40))
        self.assertEqual(self.f3.get_flight_duration(), Duration(years=0, months=0, days=0, hours=3, minutes=25))
        self.assertEqual(self.f4.get_flight_duration(), Duration(years=0, months=0, days=1, hours=1, minutes=1))

    def test_airline_flights_on_date_lt_hours(self):
        """ Get the flights on a specific date whose duration is less than the given hours """
        self.assertEqual(self.airline_dummy.get_flights_on_date_lt_hours('809414839418341413413413412'),
                         [self.f, self.f2, self.f3, self.f4])
        self.assertEqual(self.airline_dummy.get_flights_on_date_lt_hours('20'), [self.f, self.f3])
        self.assertEqual(self.airline_dummy.get_flights_on_date_lt_hours('1'), [])

    def test_airline_flights_within_duration(self):
        """ Get the flights whose durations are within the duration of another flight"""
        self.assertEqual(self.airline_dummy.get_flights_within_duration(self.f2),
                         [self.f, self.f2 ,self.f3, self.f4])
        self.assertEqual(self.airline_dummy.get_flights_within_duration(self.f),
                         [self.f])

    def test_airline_get_passengers_to_dest(self):
        """ Get all the passengers who are flying to a destination"""
        self.assertEqual(len(self.airline_dummy.get_passengers_to_dest('Barcelona')), 2)
        self.assertEqual(len(self.airline_dummy.get_passengers_to_dest('NOWHERE')), 0)

        paris_passengers = [Passenger('Mu', 'Ku', flight=self.f4, age=30),
                            Passenger('MuS', 'KuS', flight=self.f4, age=30)]
        paris_reservations = [Reservation(flight=self.f4, passenger=paris_passengers[0], accepted=True),
                              Reservation(flight=self.f4, passenger=paris_passengers[1], accepted=True)]
        self.f4.add_passengers(paris_passengers)
        self.f4.add_reservations(paris_reservations)

        self.assertEqual(self.airline_dummy.get_passengers_to_dest('Paris'), paris_passengers)

    def test_airline_get_passengers_from_terminal(self):
        """ Get all the passengers that are flying from a terminal"""
        self.assertEqual(len(self.airline_dummy.get_passengers_from_terminal(self.terminal_2)), 6)
        self.assertEqual(len(self.airline_dummy.get_passengers_from_terminal(self.terminal_1)), 0)

    def test_airline_get_flights_with_passengers(self):
        """ Get all the flights whose passengers are more than the given count """
        # add some dummy passengers to our pre-defined flights
        dp = Passenger("Dummy", "Passenger", flight=self.f3, age=30)
        self.f3.add_passengers([dp] * 42)
        self.f4.add_passengers([dp] * 42)
        self.assertEqual(self.airline_dummy.get_flights_with_passengers(41), [self.f3, self.f4])
        self.assertEqual(self.airline_dummy.get_flights_with_passengers(1), [self.f, self.f2, self.f3, self.f4])
        self.assertEqual(self.airline_dummy.get_flights_with_passengers(100000), [])

    def test_airline_get_passengers_to_dest(self):
        """ Get all the passengers who are flying to a destination"""
        self.assertEqual(len(self.airline_dummy.get_passengers_to_dest('Barcelona')), 2)
        self.assertEqual(len(self.airline_dummy.get_passengers_to_dest('NOWHERE')), 0)

        paris_passengers = [Passenger('Mu', 'Ku', flight=self.f4, age=30),
                            Passenger('MuS', 'KuS', flight=self.f4, age=30)]
        paris_reservations = [Reservation(flight=self.f4, passenger=paris_passengers[0], accepted=True),
                              Reservation(flight=self.f4, passenger=paris_passengers[1], accepted=True)]
        self.f4.add_passengers(paris_passengers)
        self.f4.add_reservations(paris_reservations)

        self.assertEqual(self.airline_dummy.get_passengers_to_dest('Paris'), paris_passengers)


    def test_airline_get_passengers_from_terminal(self):
        """ Get all the passengers that are flying from a terminal"""
        self.assertEqual(len(self.airline_dummy.get_passengers_from_terminal(self.terminal_2)), 6)
        self.assertEqual(len(self.airline_dummy.get_passengers_from_terminal(self.terminal_1)), 0)

    def test_airline_get_flights_with_passengers(self):
        """ Get all the flights whose passengers are more than the given count """
        # add some dummy passengers to our pre-defined flights
        dp = Passenger("Dummy", "Passenger", flight=self.f3, age=30)
        self.f3.add_passengers([dp]*42)
        self.f4.add_passengers([dp]*42)
        self.assertEqual(self.airline_dummy.get_flights_with_passengers(41), [self.f3, self.f4])
        self.assertEqual(self.airline_dummy.get_flights_with_passengers(1), [self.f, self.f2, self.f3, self.f4])
        self.assertEqual(self.airline_dummy.get_flights_with_passengers(100000), [])


    def test_airline_get_reservations_to_destination(self):
        """ Get all the reservations that are to a specific destination """
        self.assertEqual(self.airline_dummy.get_reservations_to_destination('London'), self.london_reservations)
        self.assertEqual(self.airline_dummy.get_reservations_to_destination('NOWHERE'), [])
    def test_airline_get_reservations_to_destination(self):
        """ Get all the reservations that are to a specific destination """
        self.assertEqual(self.airline_dummy.get_reservations_to_destination('London'), self.london_reservations)
        self.assertEqual(self.airline_dummy.get_reservations_to_destination('NOWHERE'), [])



if __name__ == '__main__':
    unittest.main()