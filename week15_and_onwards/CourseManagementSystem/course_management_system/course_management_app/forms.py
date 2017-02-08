from django.forms import models, fields as dj_field, widgets
from course_management_app.models import Course, Lecture


class CourseForm(models.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'description', 'start_date', 'end_date',)
        widgets = {
            'name': dj_field.TextInput(),
            'description': dj_field.TextInput(),
            'start_date': dj_field.TextInput(attrs={
                'class': 'datepicker'
            }),
            'end_date': dj_field.TextInput(attrs={
                'class': 'datepicker'
            })
        }


class LectureForm(models.ModelForm):
    class Meta:
        model = Lecture
        fields = ('name', 'week', 'course', 'url', )
        widgets = {
            'name': dj_field.TextInput(),
            'week': dj_field.NumberInput(),
            'course': widgets.Select(),
            'url': dj_field.TextInput()
        }
