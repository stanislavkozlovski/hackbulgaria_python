from db import Base
from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Team(Base):
    __tablename__ = 'team'

    name = Column(String(100), primary_key=True)
    room = Column(Integer)


class Tech(Base):
    __tablename__ = 'technologies'

    name = Column(String(200), primary_key=True)

    teams = relationship('TeamTechs')


class TeamTechs(Base):
    __tablename__ = 'team_technologies'

    team_id = Column(String(100), ForeignKey('team.name'), primary_key=True)
    tech_id = Column(String(100), ForeignKey('technologies.name'), primary_key=True)


class Mentor(Base):
    __tablename__ = 'mentors'

    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(60))
    teams = relationship('TeamMentors')


class TeamMentors(Base):
    __tablename__ = 'team_mentors'

    team_name = Column(String, ForeignKey('team.name'), primary_key=True)
    mentor_name = Column(String, ForeignKey('mentors.name'), primary_key=True)