from django.forms import models, fields as dj_field, widgets, PasswordInput
from course_management_app.models import Course, Lecture


class CourseForm(models.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'description', 'start_date', 'end_date',)
        widgets = {
            'name': dj_field.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': dj_field.TextInput(attrs={
                'class': 'form-control'
            }),
            'start_date': dj_field.TextInput(attrs={
                'class': 'datepicker form-control'
            }),
            'end_date': dj_field.TextInput(attrs={
                'class': 'datepicker form-control'
            })
        }


class LectureForm(models.ModelForm):
    class Meta:
        model = Lecture
        fields = ('name', 'week', 'course', 'url', )
        widgets = {
            'name': dj_field.TextInput(attrs={
                'class': 'form-control'
            }),
            'week': dj_field.NumberInput(attrs={
                'class': 'form-control'
            }),
            'course': widgets.Select(attrs={
                'class': 'form-control'
            }),
            'url': dj_field.TextInput(attrs={
                'class': 'form-control'
            })
        }
