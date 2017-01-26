from sqlalchemy import Column, Integer, String, REAL
from database.main import Base


class MovieSchema(Base):
    __tablename__ = 'movie'
    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(250))
    rating = Column(REAL)
