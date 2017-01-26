from sqlalchemy import Column, Integer, String

from database.main import Base


class UserSchema(Base):
    __tablename__ = 'users'

    id_ = Column('id', Integer, primary_key=True)
    username = Column(String(200))
    password = Column(String(200))
