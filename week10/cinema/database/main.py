from settings.constants import DB_NAME
from queries.queries import CREATE_TABLES
import sqlite3


connection = sqlite3.connect(DB_NAME)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.executescript(CREATE_TABLES)