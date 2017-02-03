from controller import (fetch_number_of_teams_in_room, fetch_teams_using_technology, fetch_team_by_name, add_skill_to_team,
                        fetch_teams_by_mentor, get_mentor_rooms, fetch_mentor_by_name, get_teams_and_schedule)
from constants import InvalidMentor
from datetime import timedelta
from load_models import load_all_models
import prettytable
from prettytable import PrettyTable


def display_help():
    print('Available commands:')
    print('\tTeams in room {room number}')
    print('\t\tPrints the number of teams in the given room.')
    print('\tTeams using {technology}')
    print('\t\tPrints all the teams that use the given technology in their stack.')
    print('\tAdd technology {technology name} to team {team name}')
    print('\t\tAdds the given technology to the technology stack of the given team.')
    print('\tShow teams mentored by {mentor name}')
    print('\t\tShows the teams that are mentored by the given mentor.')
    print('\tShow rooms visited by {mentor name} {DESC or ASC}')
    print('\t\tShows the rooms that will be visited by the given mentor, in ascending or descending order')
    print('\tShow schedule')
    print('\t\tShows the schedule for each team.')


def eval_command(command: str):
    if command.startswith('Teams in room ') and not command.endswith(' '):
        wanted_room = command.split()[3]
        teams_in_room = fetch_number_of_teams_in_room(wanted_room)
        print(f'There are a total of {teams_in_room} teams in {wanted_room}.')
    elif command.startswith('Teams using ') and not command.endswith(' '):
        wanted_tech = ' '.join(command.split()[2:])
        team_names = fetch_teams_using_technology(wanted_tech)

        if len(team_names) == 0:
            print(f'There are no teams using {wanted_tech}.')
            return

        teams_annexation: str = '\n\t'.join([tn for tn in team_names])
        print(f'The teams that use {wanted_tech} are \n\t{teams_annexation}')
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
    elif command.startswith('Show rooms visited by ') and (command.endswith('ASC') or command.endswith('DESC')):
        command_args = command.split()
        mentor_name = ' '.join(command_args[4:-1])
        order = command_args[-1]
        is_descending = True if order == 'DESC' else False

        mentor = fetch_mentor_by_name(mentor_name)
        if mentor is None:
            print(f'There is no mentor called {mentor_name}!')

        rooms = list(get_mentor_rooms(mentor, descending=is_descending))
        if len(rooms) < 1:
            print(f"{mentor_name} does not have any rooms to visit.")
            return

        rooms_annexation = '\n\t'.join(rooms)
        print(f'Rooms visited by {mentor_name}:\n\t{rooms_annexation}')
    elif command == 'Show schedule':
        teams = get_teams_and_schedule()
        table = prettytable.PrettyTable(['Time', 'Name', 'Room'], border=True, hrules=prettytable.ALL)
        for team in teams:
            table.add_row([team.time, team.name, team.room])

        print(table)
    elif command == 'help':
        display_help()
    else:
        print('Invalid command!')
        print('Type "help" to see the available commands.')


def main():
    load_all_models()
    command = input()
    while command != 'exit':
        eval_command(command)
        command = input()


if __name__ == '__main__':
    main()
