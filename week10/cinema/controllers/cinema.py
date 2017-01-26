from database.main import session
from models.user import UserSchema


def log_user():
    """ Log in a user to the system"""
    print('Please log in:')
    username = input('>Username ')
    password = input('>Password ')

    # fetch from the DB
    user = session.query(UserSchema).filter_by(username=username, password=password).one_or_none()
    while user is None:
        print("Invalid username/password! Would you like to log in again?(y/n)")
        choice = input()
        if choice not in ['y', 'yes', 'Y', 'Yes']:
            return None  # user has given up on logging in

        username = input('>Username ')
        password = input('>Password ')
        user = session.query(UserSchema).filter_by(username=username, password=password).one_or_none()

    return user
