""" This module loads information from the database. """
from database.main import connection, cursor
from queries.queries import (GET_ALL_MOVIES_ORDERED_BY_DATE, GET_MOVIE_BY_ID,
                             GET_MOVIE_PROJECTIONS_ORDERED_BY_DATE, GET_MOVIE_PROJECTIONS_ORDERED_BY_DATE_IN_DATE,
                             GET_RESERVATIONS_BY_PROJECTION_ID, GET_USER_BY_USERNAME_AND_PASSWORD)


def get_all_movies_ordered_by_date():
    movies = cursor.execute(GET_ALL_MOVIES_ORDERED_BY_DATE).fetchall()
    return movies


def get_movie_by_id(id):
    return cursor.execute(GET_MOVIE_BY_ID, [id]).fetchone()


def get_movie_projections_ordered_by_date(movie_id, date):
    if not date:
        movie_projections = cursor.execute(GET_MOVIE_PROJECTIONS_ORDERED_BY_DATE, [movie_id]).fetchall()
    else:
        movie_projections = cursor.execute(GET_MOVIE_PROJECTIONS_ORDERED_BY_DATE_IN_DATE, [movie_id, date]).fetchall()
    return movie_projections


def get_reservations_by_projection_id(projection_id):
    return cursor.execute(GET_RESERVATIONS_BY_PROJECTION_ID, [projection_id]).fetchall()


def get_user_by_username_and_password(username, password):
    return cursor.execute(GET_USER_BY_USERNAME_AND_PASSWORD, [username, password]).fetchone()
