from settings.constants import (DB_ID_KEY, DB_MOVIE_NAME_KEY, DB_PROJECTIONS_DATE_KEY,
                                DB_PROJECTIONS_HOUR_KEY, DB_PROJECTIONS_MOVIE_TYPE_KEY)
from settings.utils import get_free_spot_count_for_a_projection
from settings.validator import is_valid_date
from queries.loader import get_movie_by_id, get_movie_projections_ordered_by_date


def show_movie_projections(movie, projections, date=None):
    if projections is None:
        return
    output_lines = []
    date_annexation = '' if not date else ' on date {}'.format(date)
    # for each projection get the free spots by reading the reservations table
    for projection in projections:
        free_spots_count = get_free_spot_count_for_a_projection(projection[DB_ID_KEY])
        if date:
            output_lines.append("[{id}] - {hour} ({movie_type}) - {free_spots} Free Spots".format(
                id=projection[DB_ID_KEY], hour=projection[DB_PROJECTIONS_HOUR_KEY],
                movie_type=projection[DB_PROJECTIONS_MOVIE_TYPE_KEY], free_spots=free_spots_count
            ))
        else:
            output_lines.append("[{id}] - {date} {hour} ({movie_type}) - {free_spots} Free Spots".format(
                id=projection[DB_ID_KEY], date=projection[DB_PROJECTIONS_DATE_KEY],
                hour=projection[DB_PROJECTIONS_HOUR_KEY], movie_type=projection[DB_PROJECTIONS_MOVIE_TYPE_KEY],
                free_spots=free_spots_count
            ))
    print("Projections for movie '{mv_name}'{annexation}:".format(mv_name=movie[DB_MOVIE_NAME_KEY],
                                                                  annexation=date_annexation))
    print('\n'.join(output_lines))


def get_movie_projections(movie_id, date=None) -> tuple:
    """ Given a movie_id and an optional date, return the appropriate movie projections """
    movie = get_movie_by_id(movie_id)
    if not movie:
        print("Invalid movie id!")
        return None, None
    elif date and not is_valid_date(date):
        print('Invalid date! Date should be in the format of YYYY-MM-DD!')
        return None, None
    return movie, get_movie_projections_ordered_by_date(movie[DB_ID_KEY], date)
