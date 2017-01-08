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
