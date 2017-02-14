from django.utils.translation import ugettext_lazy as _
from django.db import models


# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(_('password'), max_length=128)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
