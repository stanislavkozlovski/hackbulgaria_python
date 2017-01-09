from settings.constants import SPECIAL_SYMBOLS


def is_valid_password(username, password):
    """
    Given a password, return a boolean indicating if it's valid
    A valid password is:
        More then 8 symbols
        Must have capital letters, and numbers and a special symbol
        Username is not in the password (as a substring)
    """
    has_capital_letter, has_number, has_special_symbol = False, False, False
    for letter in password:
        if letter.isupper():
            has_capital_letter = True
        elif letter in SPECIAL_SYMBOLS:
            has_special_symbol = True
        elif letter.isdigit():
            has_number = True

    return len(password) > 8 and (has_capital_letter and has_special_symbol and has_number) and username not in password
