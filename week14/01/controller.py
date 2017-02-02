from db import session
from models import Team, TeamTechs, Tech, TeamMentors, Mentor
from constants import InvalidMentor

def fetch_number_of_teams_in_room(room):
    number_of_teams_in_room = session.query(Team).filter_by(room=room).count()
    return number_of_teams_in_room


def fetch_teams_using_technology(tech):
    teams = [team.team_id for team in session.query(TeamTechs).filter_by(tech_id=tech).all()]
    return teams


def fetch_available_technologies():
    technologies = [tech.name for tech in session.query(Tech).all()]
    return technologies


def fetch_team_by_name(team_name):
    team = session.query(Team).filter_by(name=team_name).one_or_none()
    return team


def add_skill_to_team(team_name, tech_name):
    session.add(TeamTechs(team_id=team_name, tech_id=tech_name))
    session.commit()
    session.flush()


def fetch_teams_by_mentor(mentor_name) -> [Team]:
    mentor = session.query(Mentor).filter_by(name=mentor_name).one_or_none()
    if mentor is None:
        raise InvalidMentor(f'No mentor named {mentor_name}!')

    return mentor.teams


def fetch_teams_ordered_by_room() -> [Team]:
    return session.query(Team).order_by(Team.room).all()


def get_mentor_rooms(mentor: Mentor, descending=False):
    rooms = sorted([team.room for team in mentor.teams])

    if descending:
        return reversed(rooms)

    return rooms
