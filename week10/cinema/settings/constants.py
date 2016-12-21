import os
DB_NAME = os.path.join(os.path.join(os.path.dirname(os.getcwd()), 'database'), 'db.db')

VALID_SPELLS = [
    "show movies",
    "show movie projections",
    "make reservation",
    "cancel reservation",
    "exit",
    "help"
]

DB_ID_KEY = 'id'

DB_MOVIE_NAME_KEY = 'name'
DB_MOVIE_RATING_KEY = 'rating'