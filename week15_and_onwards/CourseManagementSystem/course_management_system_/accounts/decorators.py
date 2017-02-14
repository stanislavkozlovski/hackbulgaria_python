from django.http import HttpRequest
from django.shortcuts import redirect


def anon_required(redirect_url):
    """ Requires a user to not be logged in."""

    def wrapper(func):
        def decorate(*args, **kwargs):
            request: HttpRequest = args[0]
            if 'user' in request.session:
                return redirect(redirect_url)

            return func(*args, **kwargs)

        return decorate

    return wrapper
