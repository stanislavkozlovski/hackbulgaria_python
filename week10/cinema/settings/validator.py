import settings.constants as constants


def is_valid_spell(spell: str):
    if not isinstance(spell, str):
        return False
    for valid_spell in constants.VALID_SPELLS:
        if spell in valid_spell:
            return True

    return False
