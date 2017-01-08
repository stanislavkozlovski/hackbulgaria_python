""" Utility/helper function """
from settings.constants import MOVIE_HALL_CAPACITY, DB_RESERVATIONS_COL_KEY, DB_RESERVATIONS_ROW_KEY
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
    movie_hall = create_movie_hall_matrix_representation()
    reservations = get_reservations_by_projection_id(projection_id)
    # add a X for each taken spot
    for reservation in reservations:
        row, col = reservation[DB_RESERVATIONS_ROW_KEY], reservation[DB_RESERVATIONS_COL_KEY]
        movie_hall[row][col] = 'X'

    return movie_hall


def create_movie_hall_matrix_representation():
    """ Creates a movie hall representation using a 11x11 matrix.
    [[' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
     ['1', '', '', '', '', '', '', '', '', '', ''],
     ...etc
    """
    matrix = [[' '] + [str(row) for row in range(1, 11)]]  # create the top row
    # create the other rows
    for row in range(1, 11):
        matrix.append([str(row)] + (['-'] * 10))

    return matrix

