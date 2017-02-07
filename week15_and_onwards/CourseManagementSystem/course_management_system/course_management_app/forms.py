from django.forms import models, fields as dj_field

from course_management_app.models import Course


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