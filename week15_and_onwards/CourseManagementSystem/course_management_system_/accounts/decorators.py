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


def login_required(redirect_url):
    """ Requires a user to be logged in"""
    def wrapper(view_func):
        def decorate(*args, **kwargs):
            request: HttpRequest = args[0]
            if 'user' not in request.session:
                return redirect(redirect_url)

            return view_func(*args, **kwargs)
        return decorate
    return wrapper


def teacher_required(redirect_url):
    """ Requires a user to be logged in and for him to be a teacher"""
    def wrapper(view_func):
        def decorate(*args, **kwargs):
            request: HttpRequest = args[0]

            if 'user' not in request.session or not hasattr(request, 'user') or not request.user.is_teacher():
                return redirect(redirect_url)

            return view_func(*args, **kwargs)
        return decorate
    return wrapper
