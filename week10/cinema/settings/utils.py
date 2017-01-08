""" Utility/helper function """
from settings.constants import MOVIE_HALL_CAPACITY
from queries.loader import get_reservations_by_projection_id


def get_free_spot_count_for_a_projection(projection_id):
    """ Returns the number of free spots for a movie projection """
    reservations = get_reservations_by_projection_id(projection_id)
    return MOVIE_HALL_CAPACITY - len(reservations)


def get_free_spots_for_a_projection(projection_id):
    """
    Given a projection ID, returns a matrix representing the free and taken seats
    ex:
      1 2 3 4 5 6 7 8 9 10
    1 - - - - - X - - - -
    2 - - - - - - - - - -
    3 - - - - - - - - - - 
    4 - - - - - - - - - -
    5 - - - - - - - - - -
    6 - - - - - - - - - -
    7 - - - - - - - - - -
    8 - - - - - - - - - -
    9 - - - - - - - - - -
    10- - - - - - - - - -
    """
    pass


def create_movie_hall_matrix_representation():
    """ Creates a movie hall representation using a 11x11 matrix.
    [[' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
     ['1', '', '', '', '', '', '', '', '', '', ''],
     ...etc
    """
    matrix = [[' '] + [str(row) for row in range(1, 11)]]  # create the top row
    # create the other rows
    for row in range(1, 11):
        matrix.append([str(row)] + ([' '] * 10))

    return matrix
