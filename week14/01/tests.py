import unittest
from models import Team, Tech, TeamTechs, Mentor, TeamMentors
from load_models import load_mentors, load_technologies, load_teams_and_team_tech


class TestLoaders(unittest.TestCase):
    def test_load_mentors(self):
        """ The method should load Mentor and TeamMentors objects """
        raw_mentors = [
            {"name": "Анна-Мария Ангелова",
             "teams": [{"id": 268,"name": "Линейно Сортиране","room": "321"},]},
        ]
        loaded_mentors, loaded_team_mentors = load_mentors(raw_mentors)

        self.assertEqual(len(loaded_mentors), 1)
        self.assertEqual(len(loaded_team_mentors), 1)

        loaded_mentor = loaded_mentors[0]
        self.assertTrue(isinstance(loaded_mentor, Mentor))
        self.assertEqual(loaded_mentor.name, "Анна-Мария Ангелова")

        loaded_team_mentor = loaded_team_mentors[0]
        self.assertTrue(isinstance(loaded_team_mentor, TeamMentors))
        self.assertEqual(loaded_team_mentor.team_name, "Линейно Сортиране")
        self.assertEqual(loaded_team_mentor.mentor_name, "Анна-Мария Ангелова")

    def test_load_technologies(self):
        """ The function should return a list of Tech objects """
        tech_one = {"id": 2, "name": "C# / .NET" }
        tech_two = {"id": 3, "name": "HTML / CSS / JavaScript "}
        raw_techs = [tech_one, tech_two]

        loaded_techs = load_technologies(raw_techs)

        self.assertEqual(len(loaded_techs), 2)
        first_tech = loaded_techs[0]
        second_tech = loaded_techs[1]
        self.assertTrue(isinstance(first_tech, Tech))
        self.assertTrue(isinstance(second_tech, Tech))
        self.assertEqual(first_tech.name, tech_one['name'])
        self.assertEqual(second_tech.name, tech_two['name'])

    def test_load_teams_and_team_tech(self):
        """ The function should return a list of Team and TeamTechs objects """
        team_one = {
                    "id": 281, "name": "Pestering Petabytes",
                    "technologies_full": [{"id": 9, "name": "Java"}, {"id": 8, "name": "GO"}],
                    "room": "304"}
        team_two = {"id": 279, "name": "HackFMI Dream Team",
                    "technologies_full": [{"id": 7, "name": "C/C++"}],
                    "room": "305"}
        raw_teams = [team_one, team_two]
        teams, team_techs = load_teams_and_team_tech(raw_teams)

        self.assertEqual(len(teams), 2)
        self.assertEqual(len(team_techs), 3)

        first_team = teams[0]
        self.assertTrue(isinstance(first_team, Team))
        self.assertEqual(first_team.name, team_one['name'])
        self.assertEqual(first_team.room, team_one['room'])

        second_team = teams[1]
        self.assertTrue(isinstance(second_team, Team))
        self.assertEqual(second_team.name, team_two['name'])
        self.assertEqual(second_team.room, team_two['room'])

        tech_one = team_techs[0]
        self.assertTrue(isinstance(tech_one, TeamTechs))
        self.assertEqual(tech_one.team_id, team_one['name'])
        self.assertEqual(tech_one.tech_id, team_one['technologies_full'][0]['name'])

        tech_two = team_techs[1]
        self.assertTrue(isinstance(tech_two, TeamTechs))
        self.assertEqual(tech_two.team_id, team_one['name'])
        self.assertEqual(tech_two.tech_id, team_one['technologies_full'][1]['name'])

        tech_three = team_techs[2]
        self.assertTrue(isinstance(tech_three, TeamTechs))
        self.assertEqual(tech_three.team_id, team_two['name'])
        self.assertEqual(tech_three.tech_id, team_two['technologies_full'][0]['name'])

if __name__ == '__main__':
    unittest.main()
