from datetime import datetime
import settings.constants as constants


def is_valid_spell(spell: str):
    if not isinstance(spell, str):
        return False
    for valid_spell in constants.VALID_SPELLS:
        if spell in valid_spell:
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
