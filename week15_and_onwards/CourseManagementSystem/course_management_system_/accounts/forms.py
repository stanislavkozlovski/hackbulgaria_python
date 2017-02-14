import crypt

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

    def save(self, commit=True):
        self.instance.salt = crypt.mksalt(crypt.METHOD_SHA512)
        self.instance.password = crypt.crypt(self.instance.password, self.instance.salt)
        return super().save(commit)

