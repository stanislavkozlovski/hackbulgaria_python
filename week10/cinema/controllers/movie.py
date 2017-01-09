from settings.constants import DB_ID_KEY, DB_MOVIE_NAME_KEY, DB_MOVIE_RATING_KEY
from queries.loader import get_all_movies_ordered_by_date


def show_movies():
    movies = get_all_movies_ordered_by_date()
    # format the movies for output
    output_movies = ['[{id}] - {movie_name} ({rating})'.format(id=movie[DB_ID_KEY],
                                                               movie_name=movie[DB_MOVIE_NAME_KEY],
                                                               rating=movie[DB_MOVIE_RATING_KEY])
                     for movie in movies]
    print("Current movies:\n{}".format('\n'.join(output_movies)))
