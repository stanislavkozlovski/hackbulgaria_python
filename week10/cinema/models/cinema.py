from settings.constants import DB_USERS_USERNAME_KEY
from settings.utils import log_user


class Cinema:
    def __init__(self):
        self.user = None

    def has_logged_user(self):
        return self.user is not None

    def log_user_in(self):
        if self.user is not None:
            print('You are already logged in as {name}. Would you like to log out?(y/n)'.format(
                name=self.user[DB_USERS_USERNAME_KEY]))
            choice = input()
            if choice not in ['y', 'Yes', 'Y', 'YES', 'yes']:
                return
            self.user = None  # log out the current user

        user = log_user()

        if user is not None:
            print('You have been successfully logged in as {name}!'.format(name=user[DB_USERS_USERNAME_KEY]))
            self.user = user
