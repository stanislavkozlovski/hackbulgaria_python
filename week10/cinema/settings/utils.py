""" Utility/helper functions """


def get_free_spots_for_a_projection(projection):
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
    reservations = projection.reservations
    # add a X for each taken spot
    for reservation in reservations:
        row, col = reservation.row, reservation.col
        movie_hall[row][col] = 'X'

    return movie_hall


def print_movie_hall(movie_hall: list):
    """
    Given a matrix representing a movie hall, prints in out for the user to view it
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
    for row in movie_hall:
        print(' '.join(row).rjust(25, ' '))


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


