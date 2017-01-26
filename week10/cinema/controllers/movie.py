from database.main import session
from models.movie import MovieSchema


def get_all_movies_ordered_by_date():
    movies = session.query(MovieSchema).order_by(MovieSchema.rating.desc()).all()
    return movies


def show_movies():
    movies = get_all_movies_ordered_by_date()
    # format the movies for output
    output_movies = ['[{id}] - {movie_name} ({rating})'.format(id=movie.id_,
                                                               movie_name=movie.name,
                                                               rating=movie.rating)
                     for movie in movies]
    print("Current movies:\n{}".format('\n'.join(output_movies)))
