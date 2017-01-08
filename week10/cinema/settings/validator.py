from datetime import datetime
import settings.constants as constants


def is_valid_spell(spell: str):
    if not isinstance(spell, str):
        return False
    for valid_spell in constants.VALID_SPELLS:
        if spell.startswith(valid_spell):
            return True

    return False


def is_valid_date(date):
    """
    A valid date is in the format of yyyy-mm-dd
    """
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False


def is_valid_ticket_count(ticket_count: str):
    """ A valid ticket count is between 1-10 """
    try:
        tickets = int(ticket_count)
        if 1 <= tickets <= 10:
            return True
        return False
    except (ValueError, TypeError):
        return False
