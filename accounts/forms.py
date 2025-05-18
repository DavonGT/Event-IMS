from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    middle_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password','first_name','middle_name', 'last_name', 'organization']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'username': 'Username',
            'password': 'Password',
            'confirm_password': 'Confirm Password',
            'first_name': 'First Name',
            'middle_name': 'Middle Name',
            'last_name': 'Last Name',
            'organization': 'Organization'
        }

        for field_name, field in self.fields.items():
            if field_name != 'role':
                field.label = None
                field.widget.attrs.update({'placeholder': placeholders.get(field_name, '')})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
