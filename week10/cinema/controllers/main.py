from models.cinema import Cinema
from settings.validator import is_valid_spell
from controllers.projections import get_movie_projections, show_movie_projections
from controllers.reservation import make_reservation
from controllers.movie import show_movies


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
        make_reservation(cinema)

