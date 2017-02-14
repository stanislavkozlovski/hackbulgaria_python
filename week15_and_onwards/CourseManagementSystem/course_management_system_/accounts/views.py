from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from accounts.forms import UserForm


# Create your views here.
def register(request: HttpRequest):
    if request.method == 'POST':
        pass

    return render(request, 'register.html', context={'form': UserForm()})