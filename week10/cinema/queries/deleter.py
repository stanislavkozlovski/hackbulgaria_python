""" This module deletes information from the DB """
from database.main import connection, cursor
from queries.queries import DELETE_RESERVATIONS_FROM_USER


def delete_reservations_from_user(user_id):
    """ Given a user id, deletes all reservations that are registered to that name """
    cursor.execute(DELETE_RESERVATIONS_FROM_USER, user_id)
    connection.commit()
