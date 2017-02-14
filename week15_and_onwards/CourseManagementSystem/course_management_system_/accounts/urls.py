from django.conf.urls import url

from accounts import views

urlpatterns = [
    url('^register$', views.register, name='register'),
    url('^(\d+)$', views.profile, name='user_profile')
]
