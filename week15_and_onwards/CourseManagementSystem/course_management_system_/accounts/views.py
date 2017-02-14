import crypt

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core import serializers

from accounts.forms import UserForm, LoginForm
from accounts.models import User


# Create your views here.
def register(request: HttpRequest):
    """ Registers a user """
    if request.method == 'POST':
        form = UserForm(data=request.POST)

        if not form.is_valid():
            return redirect('/accounts/register')

        user = form.save()
        request.session['user'] = serializers.serialize('json', [user])
        return redirect(f'/accounts/{user.id}')

    return render(request, 'register.html', context={'form': UserForm()})


def login(request: HttpRequest):
    """ Logs a user in"""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if not form.is_valid():
            return redirect('/accounts/login')
        potential_login: LoginForm = form.data

        potential_user: User = User.objects.filter(email=potential_login['email']).first()
        if potential_user is None:
            return redirect('/accounts/login')
        # Almost there, validate passwords
        potential_password = crypt.crypt(potential_login['password'], potential_user.salt)

        if not potential_password == potential_user.password:
            return redirect('/accounts/login')
        # Successful login!
        request.session['user'] = serializers.serialize('json', [potential_user])
        return redirect(f'/accounts/{potential_user.id}')

    return render(request, 'login.html', context={'form': LoginForm()})


def profile(request: HttpRequest, profile_id):
    """ Opens the profile of a user """
    return render(request, 'base.html')

