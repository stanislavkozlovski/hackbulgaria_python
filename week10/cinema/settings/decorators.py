from settings.constants import DB_USERS_USERNAME_KEY


def authenticate(func):
    """
    A function used to authenticate (log in) the user into the system. Requires that a Cinema object is passed
    to the
    """
    def _authenticate(*args, **kwargs):
        cinema = args[0]
        if not cinema.has_logged_user():
            cinema.log_user_in()
            if not cinema.has_logged_user():
                # If the user has declined logging in
                print('You have to be logged in to make a reservation!')
                return
        func(*args, **kwargs)
    return _authenticate


def authenticate_user(func):
    """ A function used to authenticate (log in) the SPECIFIC user into the system. Requires that a Cinema object and
     a username is passed to the decorated function."""
    def _auth(*args, **kwargs):
        cinema = args[0]
        username = args[1]
        if (not cinema.has_logged_user()) or cinema.user.username != username:
            print('You have to be logged in as {u} to do that!'.format(u=username))
            cinema.log_user_in()
            if (not cinema.has_logged_user()) or cinema.user.username != username:
                print('You have to be logged in as {u} to do that!'.format(u=username))
                return
    return _auth
