"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from mysite.views import get_index, calc_n_factorial, calc_nth_fibonacci_numbers, calc_nth_primes, encode_rl, decode_rl

urlpatterns = [
    url(r'^index/$', get_index, name='index'),
    url(r'^index/calculateNFactorial/$', calc_n_factorial, name='calc_n_factorial'),
    url(r'^index/calculateNthFibonacci/$', calc_nth_fibonacci_numbers, name='calc_first_n_fibonacci'),
    url(r'^index/calculateNthPrimes/$', calc_nth_primes, name='calc_first_n_primes'),
    url(r'^index/decodeRL/$', decode_rl, name='rl_decode'),
    url(r'^index/encodeRL/$', encode_rl, name='rl_encode'),
    url(r'^admin/', admin.site.urls),
]
