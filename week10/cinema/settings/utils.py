""" Utility/helper function """
from settings.constants import MOVIE_HALL_CAPACITY
from queries.loader import get_reservations_by_projection_id


def get_free_spots_for_a_projection(projection_id):
    """ Returns the number of free spots for a movie projection """
    reservations = get_reservations_by_projection_id(projection_id)
    return MOVIE_HALL_CAPACITY - len(reservations)
