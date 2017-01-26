from database.main import session
from models.movie import MovieSchema
from settings.constants import MOVIE_HALL_CAPACITY
from settings.validator import is_valid_date


def show_movie_projections(movie, projections, date=None):
    if projections is None:
        return
    output_lines = []
    date_annexation = '' if not date else ' on date {}'.format(date)
    # for each projection get the free spots by reading the reservations table
    for projection in sorted(projections, key=lambda proj: (proj.proj_date, proj.time)):
        free_spots_count = MOVIE_HALL_CAPACITY - len(projection.reservations)
        if date:
            output_lines.append("[{id}] - {hour} ({movie_type}) - {free_spots} Free Spots".format(
                id=projection.id_, hour=projection.time,
                movie_type=projection.type, free_spots=free_spots_count
            ))
        else:
            output_lines.append("[{id}] - {date} {hour} ({movie_type}) - {free_spots} Free Spots".format(
                id=projection.id_, date=projection.proj_date,
                hour=projection.time, movie_type=projection.type,
                free_spots=free_spots_count
            ))
    print("Projections for movie '{mv_name}'{annexation}:".format(mv_name=movie.name,
                                                                  annexation=date_annexation))
    print('\n'.join(output_lines))


def get_movie_projections(movie_id, date=None) -> tuple:
    """ Given a movie_id and an optional date, return the appropriate movie projections """
    movie = session.query(MovieSchema).get(movie_id)
    if not movie:
        print("Invalid movie id!")
        return None, None
    elif date and not is_valid_date(date):
        print('Invalid date! Date should be in the format of YYYY-MM-DD!')
        return None, None
    return movie, movie.projections
