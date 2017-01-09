""" This module inserts information into the DB """
from database.main import connection, cursor
from queries.queries import CREATE_RESERVATION
from models.ticket import Ticket


def create_reservations(reservations: [Ticket]):
    """ Given a list of Tickets, insert a reservation for each ticket into the DB. """
    seq_of_parameters = [(rsv.owner_id, rsv.projection_id, rsv.row, rsv.col) for rsv in reservations]
    cursor.executemany(CREATE_RESERVATION, seq_of_parameters)
    connection.commit()
