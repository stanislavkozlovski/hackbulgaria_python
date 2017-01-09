from settings.constants import VALID_SPELLS


def general_help():
    """ Prints out the available spells"""
    print('The available spells are: \n\t{}'.format('\n\t'.join(VALID_SPELLS)))
    print('For more information on each spell, enter "help <command name>".')


def command_help(command: str):
    """ Prints out the help for the specific command """
    pass