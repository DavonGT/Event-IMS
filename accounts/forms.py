from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
            'confirm_password': 'Confirm Password',
        }

        for field_name, field in self.fields.items():
            if field_name != 'role':
                field.label = None
                field.widget.attrs.update({'placeholder': placeholders.get(field_name, '')})
