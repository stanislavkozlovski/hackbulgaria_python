from settings.validator import is_valid_spell, is_valid_date
from settings.constants import (DB_ID_KEY, DB_MOVIE_NAME_KEY, DB_MOVIE_RATING_KEY,
                                DB_PROJECTIONS_DATE_KEY, DB_PROJECTIONS_HOUR_KEY,
                                DB_PROJECTIONS_MOVIE_TYPE_KEY, MOVIE_HALL_CAPACITY)
from queries.loader import get_all_movies_ordered_by_date, get_movie_by_id, get_movie_projections_ordered_by_date, get_reservations_by_projection_id


def read_spell():
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
        movie_id = None
        if len(command_args) == 5:
            # Date has been given
            date = command_args[-1]
            movie_id = command_args[-2]
        else:
            movie_id = command_args[-1]
        show_movie_projections(movie_id, date)


def show_movies():
    movies = get_all_movies_ordered_by_date()
    # format the movies for output
    output_movies = ['[{id}] - {movie_name} ({rating})'.format(id=movie[DB_ID_KEY],
                                                               movie_name=movie[DB_MOVIE_NAME_KEY],
                                                               rating=movie[DB_MOVIE_RATING_KEY])
                     for movie in movies]
    print("Current movies:\n{}".format('\n'.join(output_movies)))


def show_movie_projections(movie_id, date=None):
    movie = get_movie_by_id(movie_id)
    if not movie:
        print("Invalid movie id!")
        return
    elif date and not is_valid_date(date):
        print('Invalid date! Date should be in the format of YYYY-MM-DD!')
        return
    projections = get_movie_projections_ordered_by_date(movie[DB_ID_KEY], date)
    # for each projection
    # get the free spots by reading the reservations table
    output_lines = []
    for projection in projections:
        reservations = get_reservations_by_projection_id(projection[DB_ID_KEY])
        free_spots_count = MOVIE_HALL_CAPACITY - len(reservations)
        output_lines.append("[{id}] - {date} {hour} ({movie_type}) - {free_spots} Free Spots".format(
            id=projection[DB_ID_KEY], date=projection[DB_PROJECTIONS_DATE_KEY],
            hour=projection[DB_PROJECTIONS_HOUR_KEY], movie_type=projection[DB_PROJECTIONS_MOVIE_TYPE_KEY],
            free_spots=free_spots_count
        ))
    print('\n'.join(output_lines))
