from django.conf.urls import url

from accounts import views

urlpatterns = [
    url('^register$', views.register, name='register'),
    url('^login$', views.login, name='login'),
    url('^(\d+)$', views.profile, name='user_profile'),
    url('^profile$', views.my_profile, name='my_profile')
]
