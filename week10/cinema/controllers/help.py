from settings.constants import VALID_SPELLS


def general_help():
    """ Prints out the available spells"""
    print('The available spells are: \n\t{}'.format('\n\t'.join(VALID_SPELLS)))
    print('For more information on each spell, enter "help <command name>".')


def command_help(command: str):
    """ Prints out the help for the specific command """
    command_to_help_func = {
        'help': help_help,
        'exit': exit_help,
        'show movies': show_movies_help,
        'show movie projections': show_movie_projections_help,
        'make reservation': make_reservation_help,
        'cancel reservation': cancel_reservation_help
    }
    if command not in command_to_help_func:
        print('Invalid command.')
    else:
        command_to_help_func[command]()


def show_movies_help():
    print('The "show movies" command displays all the movies ordered by their rating.')


def show_movie_projections_help():
    print('The "show movie projections <movie_id> [<date>] prints all the projections for a given movie.')
    print('\tThe date is optional and if given, will print out all the projections for that movie on that date only.')
    print('\tThe projections are ordered by date.')
    print('\tThe number of free spots for the projection is shown.')


def make_reservation_help():
    print('The "make reservation" command lets you reserve tickets for a given movie projection.')
    print('\tIt requires that you\'re logged in to the system.')
    print('\tLets you choose from all the movies, the projection for the movies and the free seats for the given projection.')
    print('\tYou are allowed to reserve multiple tickets.')
    print('\tDuring the proccess, entering the "give up" command will cancel the creation.')


def cancel_reservation_help():
    print('The "cancel reservation <username>" command lets you cancel all the reservations made on your name.')
    print('It is required that you are logged in as the user you are cancelling the reservations of.')


def exit_help():
    print('Exits the system.')


def help_help():
    print('Pretty self-explanatory. :|')
