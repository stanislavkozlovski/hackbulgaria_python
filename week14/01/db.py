import os
import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DB_PATH = os.path.join(DIR_PATH, "hackathon.db")
engine = sqlalchemy.create_engine(f'sqlite:////{DB_PATH}')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


def load_and_create_db():
    import models
    Base.metadata.create_all(engine)


def delete_test_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

