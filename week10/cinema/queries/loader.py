from database.main import connection, cursor
from queries.queries import GET_ALL_MOVIES_ORDERED_BY_DATE


def get_all_movies_ordered_by_date():
    movies = cursor.execute(GET_ALL_MOVIES_ORDERED_BY_DATE)
    return movies
