from settings.validator import is_valid_spell
from settings.constants import DB_ID_KEY, DB_MOVIE_NAME_KEY, DB_MOVIE_RATING_KEY
from queries.loader import get_all_movies_ordered_by_date


def read_spell():
    """ Expect a command from the user and do the appropriate action """
    user_input = input()
    while not is_valid_spell(user_input):
        print('Invalid spell!')
        user_input = input()

    if user_input == 'show movies':
        show_movies()


def show_movies():
    movies = get_all_movies_ordered_by_date()
    # format the movies for output
    output_movies = ['[{id}] - {movie_name} ({rating})'.format(id=movie[DB_ID_KEY],
                                                               movie_name=movie[DB_MOVIE_NAME_KEY],
                                                               rating=movie[DB_MOVIE_RATING_KEY])
                     for movie in movies]
    print("Current movies:\n{}".format('\n'.join(output_movies)))
