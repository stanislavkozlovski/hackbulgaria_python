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

MOVIE_HALL_CAPACITY = 100


DB_ID_KEY = 'id'

DB_MOVIE_NAME_KEY = 'name'
DB_MOVIE_RATING_KEY = 'rating'

DB_PROJECTIONS_DATE_KEY = 'proj_date'
DB_PROJECTIONS_HOUR_KEY = 'time'
DB_PROJECTIONS_MOVIE_TYPE_KEY = 'type'

DB_RESERVATIONS_ROW_KEY = 'row'
DB_RESERVATIONS_COL_KEY = 'col'

DB_USERS_USERNAME_KEY = 'username'
DB_USERS_PASSWORD_KEY = 'password'
