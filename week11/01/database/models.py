from sqlalchemy import Column, String, Integer, REAL, ForeignKey
from sqlalchemy.orm import relationship, backref
from database.main import Base, session


class Client(Base):

    __tablename__ = 'clients'

    id_ = Column('id', Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    salt = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    balance = Column(REAL, nullable=False, default=0.00)
    message = Column(String(400))
    reset_code = Column(String(400))
    last_blocked = Column(String(100))


# TODO: not nullable balance
class InvalidLogin(Base):

    __tablename__ = 'invalid_logins'

    id_ = Column('id', Integer, ForeignKey('clients.id'), primary_key=True)
    login_count = Column(Integer)
    _ = relationship('Client', backref=backref('invalid_logins', uselist=False))


class TanCode(Base):

    __tablename__ = 'tan_codes'

    id_ = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('clients.id'))
    tan_code = Column(String(250), nullable=False)

    _ = relationship('Client', backref='tan_codes')
