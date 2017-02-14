from django.forms import models, fields as dj_field, widgets, PasswordInput

from accounts.models import User


class UserForm(models.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', )
        widgets = {
            'email': dj_field.EmailInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}),
            'first_name': dj_field.TextInput(attrs={'class': 'form-control'}),
            'last_name': dj_field.TextInput(attrs={'class': 'form-control'})
        }