from django.db import models
from django.core.validators import MinValueValidator
from django.core.urlresolvers import reverse


# Create your models here.
class Course(models.Model):
    name = models.TextField(unique=True)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view_course', args=[self.name])


class Lecture(models.Model):
    name = models.TextField()
    week = models.IntegerField(validators=[MinValueValidator(1)])
    course = models.ForeignKey(Course)
    url = models.TextField()

    def get_absolute_url(self):
        return reverse('view_lecture', args=[self.id])

    class Meta:
        ordering = ('week', )
        unique_together = ('course', 'name')
