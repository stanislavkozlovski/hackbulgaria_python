from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Course(models.Model):
    name = models.TextField(unique=True)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Lecture(models.Model):
    name = models.TextField()
    week = models.IntegerField(validators=[MinValueValidator(1)])
    course = models.ForeignKey(Course)
    url = models.TextField()
