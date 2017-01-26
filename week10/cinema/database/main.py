from settings.constants import DB_NAME
import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine('sqlite:////{DB_NAME}'.format(DB_NAME=DB_NAME))
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

