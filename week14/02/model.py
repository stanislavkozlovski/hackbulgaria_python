import os
import sqlalchemy
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DB_PATH = os.path.join(DIR_PATH, "servers.db")
engine = sqlalchemy.create_engine(f'sqlite:////{DB_PATH}')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Server(Base):
    __tablename__ = 'server'
    server_name = Column(String(200), primary_key=True)
    occurences = Column(Integer)

Base.metadata.create_all(engine)