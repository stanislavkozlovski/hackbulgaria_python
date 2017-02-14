"""course_management_system URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin

from course_management_app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^course/new/', views.new_course, name='new_course'),
    url(r'^course/edit/(.+)/', views.edit_course, name='edit_course'),
    url(r'^course/(.+)/$', views.view_course, name='view_course'),
    url(r'^lecture/new/', views.new_lecture, name='new_lecture'),
    url(r'^lecture/(\d+)$', views.view_lecture, name='view_lecture'),
    url(r'^lecture/edit/(\d+)/$', views.edit_lecture, name='edit_lecture'),
    url(r'.*', views.redirect_404),
]

