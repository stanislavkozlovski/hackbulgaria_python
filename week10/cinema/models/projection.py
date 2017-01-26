from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from database.main import Base


class ProjectionSchema(Base):
    __tablename__ = 'projections'
    id_ = Column('id', Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.id'))
    type = Column(String(20))
    proj_date = Column(String(50))
    time = Column(String(30))

    _ = relationship('MovieSchema', backref=backref('projections', uselist=True))
