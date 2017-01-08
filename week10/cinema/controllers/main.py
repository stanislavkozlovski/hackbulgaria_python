import getpass
from settings.validator import is_valid_spell, is_valid_date, is_valid_ticket_count
from settings.constants import (DB_ID_KEY, DB_MOVIE_NAME_KEY, DB_MOVIE_RATING_KEY,
                                DB_PROJECTIONS_DATE_KEY, DB_PROJECTIONS_HOUR_KEY,
                                DB_PROJECTIONS_MOVIE_TYPE_KEY, MOVIE_HALL_CAPACITY, DB_USERS_USERNAME_KEY)
from settings.utils import get_free_spots_for_a_projection
from queries.loader import (get_all_movies_ordered_by_date, get_movie_by_id, get_movie_projections_ordered_by_date,
                            get_reservations_by_projection_id, get_user_by_username_and_password)


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
        free_spots_count = get_free_spots_for_a_projection(projection[DB_ID_KEY])
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
