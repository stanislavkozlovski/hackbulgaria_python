import requests
import db
from models import Team, Tech, TeamTechs, Mentor, TeamMentors
from constants import MENTORS_URL, TECHNOLOGIES_URL, PUBLIC_TEAMS_URL


def load_mentors(raw_mentors_json):
    loaded_mentors: [Mentor] = []
    loaded_team_mentors: [TeamMentors] = []
    for mentor in raw_mentors_json:
        mntr = Mentor(name=mentor["name"])
        loaded_mentors.append(mntr)
        for mentored_team in mentor['teams']:
            tm_name = mentored_team['name']
            loaded_team_mentors.append(TeamMentors(team_name=tm_name, mentor_name=mntr.name))

    return loaded_mentors, loaded_team_mentors


def load_technologies(technologies):
    loaded_technologies: [Tech] = []
    for tech in technologies:
        loaded_technologies.append(Tech(name=tech['name']))

    return loaded_technologies


def load_teams_and_team_tech(raw_teams_json):
    loaded_teams: [Team] = []
    loaded_team_techs: [TeamTechs] = []
    for team in raw_teams_json:
        tm = Team(name=team['name'], room=team['room'])
        loaded_teams.append(tm)

        for tech in team["technologies_full"]:
            tech_name = tech['name']
            team_tech = TeamTechs(team_name=tm.name, tech_name=tech_name)
            loaded_team_techs.append(team_tech)

    return loaded_teams, loaded_team_techs


def save_seq(seq):
    db.session.add_all(seq)
    db.session.commit()
    db.session.flush()


def load_all_models():
    db.delete_test_db()
    db.load_and_create_db()

    raw_tech_info = requests.get(TECHNOLOGIES_URL).json()
    technologies = load_technologies(raw_tech_info)
    save_seq(technologies)

    raw_team_info = requests.get(PUBLIC_TEAMS_URL).json()
    teams, team_techs = load_teams_and_team_tech(raw_team_info)
    save_seq(teams)
    save_seq(team_techs)

    raw_mentors_info = requests.get(MENTORS_URL).json()
    mentors, team_mentors = load_mentors(raw_mentors_info)
    save_seq(mentors)
    save_seq(team_mentors)
