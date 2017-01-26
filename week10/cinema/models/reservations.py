from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import backref, relationship

from database.main import Base


class ReservationSchema(Base):
    __tablename__ = 'reservations'

    id_ = Column('id', Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    projection_id = Column(Integer, ForeignKey('projections.id'))
    row = Column(Integer)
    col = Column(Integer)
    _ = relationship('ProjectionSchema', backref=backref('reservations', uselist=True))
