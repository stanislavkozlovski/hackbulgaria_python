def validate_password(password: str) -> bool:
    """
    Password constraints:
        At least one uppercase letter
        At least one lowercase letter
        One digit
        Length greater than 7
    :return: a boolean indicating if the given password is valid.
    """
    if len(password) <= 7:
        return False
    contains_uppercase, contains_lowercase, contains_digit = False, False, False
    for character in password:
        if character.isupper():
            contains_uppercase = True
        elif character.islower():
            contains_lowercase = True
        elif character.isdigit():
            contains_digit = True

    return contains_lowercase and contains_uppercase and contains_digit
