from controller import fetch_number_of_teams_in_room, fetch_teams_using_technology, fetch_team_by_name, add_skill_to_team, fetch_teams_by_mentor
from constants import InvalidMentor


def help():
    print('Available commands:')
    print('\tTeams in room {room number}')
    print('\t\tPrints the number of teams in the given room.')
    print('\tTeams using {technology}')
    print('\t\tPrints all the teams that use the given technology in their stack.')
    print('\tAdd technology {technology name} to team {team name}')
    print('\t\tAdds the given technology to the technology stack of the given team.')
    print('\tShow teams mentored by {mentor name}')
    print('\t\tShows the teams that are mentored by the given mentor.')


def eval_command(command: str):
    if command.startswith('Teams in room ') and not command.endswith(' '):
        wanted_room = command.split()[3]
        teams_in_room = fetch_number_of_teams_in_room(wanted_room)
        print(f'There are a total of {teams_in_room} teams in {wanted_room}.')
    elif command.startswith('Teams using ') and not command.endswith(' '):
        wanted_tech = command.split()[2:]
        teams = fetch_teams_using_technology(wanted_tech)

        if len(teams) == 0:
            print(f'There are no teams using {wanted_tech}.')
            return

        print(f'The teams that use {wanted_tech} are {" ".join([team.name for team in teams])}')
    elif command.startswith('Add technology ') and ' to team ' in command and not command.endswith(' '):
        command_args = command.split()
        tech = command_args[2]
        team_name = ' '.join(command_args[5:])

        team = fetch_team_by_name(team_name)
        if team is None:
            print(f'There is no team called {team_name}!')
            return

        add_skill_to_team(team.name, tech)
    elif command.startswith('Show teams mentored by ') and not command.endswith(' '):
        mentor = command[23:]
        try:
            teams = fetch_teams_by_mentor(mentor)
            if len(teams) == 0:
                print(f'There are no teams mentored by {mentor}')
                return
            teams_annexation = "\n\t".join([team.team_name for team in teams])
            print(f'Teams mentored by {mentor}:\n\t{teams_annexation}')
        except InvalidMentor as e:
            print(str(e))
            return


def main():
    command = input()
    while command != 'exit':
        eval_command(command)
        command = input()


if __name__ == '__main__':
    main()
