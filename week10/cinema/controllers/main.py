import getpass
from models.ticket import Ticket
from settings.validator import is_valid_spell, is_valid_date, is_valid_ticket_count, is_valid_row_or_col
from settings.constants import (DB_ID_KEY, DB_MOVIE_NAME_KEY, DB_MOVIE_RATING_KEY,
                                DB_PROJECTIONS_DATE_KEY, DB_PROJECTIONS_HOUR_KEY,
                                DB_PROJECTIONS_MOVIE_TYPE_KEY, MOVIE_HALL_CAPACITY, DB_USERS_USERNAME_KEY)
from settings.utils import get_free_spot_count_for_a_projection, get_free_spots_for_a_projection, print_movie_hall
from queries.loader import (get_all_movies_ordered_by_date, get_movie_by_id, get_movie_projections_ordered_by_date,
                            get_reservations_by_projection_id, get_user_by_username_and_password)
from queries.inserter import create_reservations

class Cinema:
    def __init__(self):
        self.user = None

    def has_logged_user(self):
        return self.user is not None

    def log_user_in(self):
        if self.user is not None:
            print('You are already logged in as {name}. Would you like to log out?(y/n)'.format(
                name=self.user[DB_USERS_USERNAME_KEY]))
            choice = input()
            if choice not in ['y', 'Yes', 'Y', 'YES', 'yes']:
                return
            self.user = None  # log out the current user

        user = log_user()

        if user is not None:
            print('You have been successfully logged in as {name}!'.format(name=user[DB_USERS_USERNAME_KEY]))
            self.user = user


def read_spell(cinema: Cinema):
    """ Expect a command from the user and do the appropriate action """
    user_input = input()
    while not is_valid_spell(user_input):
        print('Invalid spell!')
        user_input = input()

    # TODO: Move to a dictionary/something else
    if user_input == 'show movies':
        show_movies()
    elif 'show movie projections' in user_input:
        command_args = user_input.split()
        date = None
        if len(command_args) == 5:
            # Date has been given
            date = command_args[-1]
            movie_id = command_args[-2]
        else:
            movie_id = command_args[-1]
        movie, projections = get_movie_projections(movie_id, date)
        show_movie_projections(movie, projections, date)
    elif 'make reservation' in user_input:
        if not cinema.has_logged_user():
            cinema.log_user_in()
            if not cinema.has_logged_user():
                # If the user has declined logging in
                print('You have to be logged in to make a reservation!')
                return
        print('Choose the amount of tickets you want:')
        ticket_count = input(">Ticket count: ")
        while not is_valid_ticket_count(ticket_count):
            print('Invalid ticket count! The ticket count should be between 1-10 inclusive.')
            ticket_count = input(">Ticket count: ")
        ticket_count = int(ticket_count)
        # show the movies and let the user choose one
        show_movies()
        movie_id = input(">Choose a movie: ")
        movie = get_movie_by_id(movie_id)
        while not movie:
            print("Invalid movie id!")
            movie_id = input(">Choose a movie: ")
            movie = get_movie_by_id(movie_id)

        # show the projections for the movie
        movie, projections = get_movie_projections(movie_id)
        if len(projections) == 0:
            print('There are no projections for that movie, we apologize for the inconvenience.')
            return
        projections_by_id = {str(projection[DB_ID_KEY]): projection for projection in projections}
        while True:
            show_movie_projections(movie, projections)
            projection_id = input(">Choose a projection: ")
            if projection_id in projections_by_id:
                # see if there are enough free spots
                free_spots_count = get_free_spot_count_for_a_projection(projection_id)

                if free_spots_count < ticket_count:
                    print('There are not enough free spots for {} tickets!'.format(ticket_count))
                    print('Please choose another projection')
                    continue

                break
            print('Invalid projection id!')
        projection = projections_by_id[projection_id]
        movie_hall = get_free_spots_for_a_projection(projection_id)
        tickets = {}  # type: {int:Ticket}
        for i in range(ticket_count):
            # loop until the user chooses a valid ticket
            while True:
                print("Please pick a spot for ticket #{}".format(i+1))
                print_movie_hall(movie_hall)
                row = input("Choose a row: (1-10): ")
                while not is_valid_row_or_col(row):
                    print('The row you entered is invalid.')
                    row = input("Choose a row: (1-10): ")
                row = int(row)
                col = input("Choose a cow: (1-10): ")
                while not is_valid_row_or_col(col):
                    print('The col you entered is invalid.')
                    col = input("Choose a col: (1-10): ")
                col = int(col)
                if movie_hall[row][col] == 'X':
                    print('The spot you choose is taken!')
                else:
                    # take the seat and add the ticket
                    movie_hall[row][col] = 'X'
                    ticket = Ticket(row, col, movie_name=movie[DB_MOVIE_NAME_KEY], projection_id=projection[DB_ID_KEY],
                                    proj_type=projection[DB_PROJECTIONS_MOVIE_TYPE_KEY],
                                    date=projection[DB_PROJECTIONS_DATE_KEY], hour=projection[DB_PROJECTIONS_HOUR_KEY],
                                    owner_id=cinema.user[DB_ID_KEY])
                    tickets[i+1] = ticket
                    break
        # finalize order
        print('You have chosen to create {reservation_count} reservations for the movie {movie_name} on {date}{time}'.format(
            reservation_count=ticket_count, movie_name=movie[DB_MOVIE_NAME_KEY],
            date=projection[DB_PROJECTIONS_DATE_KEY], time=projection[DB_PROJECTIONS_HOUR_KEY]
        ))
        for idx, ticket in tickets.items():
            print("#{} {}".format(str(idx), ticket))

        choice = input('Do you confirm your order? (y/n): ')
        if choice in ['y', 'Y', 'yes', 'YES', 'Yes']:
            create_reservations(tickets.values())



def show_movies():
    movies = get_all_movies_ordered_by_date()
    # format the movies for output
    output_movies = ['[{id}] - {movie_name} ({rating})'.format(id=movie[DB_ID_KEY],
                                                               movie_name=movie[DB_MOVIE_NAME_KEY],
                                                               rating=movie[DB_MOVIE_RATING_KEY])
                     for movie in movies]
    print("Current movies:\n{}".format('\n'.join(output_movies)))


def show_movie_projections(movie, projections, date=None):
    if projections is None:
        return
    output_lines = []
    date_annexation = '' if not date else ' on date {}'.format(date)
    # for each projection get the free spots by reading the reservations table
    for projection in projections:
        free_spots_count = get_free_spot_count_for_a_projection(projection[DB_ID_KEY])
        if date:
            output_lines.append("[{id}] - {hour} ({movie_type}) - {free_spots} Free Spots".format(
                id=projection[DB_ID_KEY], hour=projection[DB_PROJECTIONS_HOUR_KEY],
                movie_type=projection[DB_PROJECTIONS_MOVIE_TYPE_KEY], free_spots=free_spots_count
            ))
        else:
            output_lines.append("[{id}] - {date} {hour} ({movie_type}) - {free_spots} Free Spots".format(
                id=projection[DB_ID_KEY], date=projection[DB_PROJECTIONS_DATE_KEY],
                hour=projection[DB_PROJECTIONS_HOUR_KEY], movie_type=projection[DB_PROJECTIONS_MOVIE_TYPE_KEY],
                free_spots=free_spots_count
            ))
    print("Projections for movie '{mv_name}'{annexation}:".format(mv_name=movie[DB_MOVIE_NAME_KEY],
                                                                  annexation=date_annexation))
    print('\n'.join(output_lines))


def get_movie_projections(movie_id, date=None) -> tuple:
    """ Given a movie_id and an optional date, return the appropriate movie projections """
    movie = get_movie_by_id(movie_id)
    if not movie:
        print("Invalid movie id!")
        return None, None
    elif date and not is_valid_date(date):
        print('Invalid date! Date should be in the format of YYYY-MM-DD!')
        return None, None
    return movie, get_movie_projections_ordered_by_date(movie[DB_ID_KEY], date)


def log_user():
    """ Log in a user to the system"""
    print('Please log in:')
    username = input('>Username ')
    password = getpass.getpass()

    # fetch from the DB
    user = get_user_by_username_and_password(username, password)
    while user is None:
        print("Invalid username/password! Would you like to log in again?(y/n)")
        choice = input()
        if choice not in ['y', 'yes', 'Y', 'Yes']:
            return None  # user has given up on logging in

        username = input('>Username ')
        password = getpass.getpass()
        user = get_user_by_username_and_password(username, password)

    return user
