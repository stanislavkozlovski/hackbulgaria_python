import sqlite3
import sqlalchemy
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DB_PATH = os.path.join(DIR_PATH, "db.db")

engine = sqlalchemy.create_engine('sqlite:////{DB_PATH}'.format(DB_PATH=DB_PATH))
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
