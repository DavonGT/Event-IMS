from django import forms
from django.contrib.auth import get_user_model
from .models import Event, Organization

class EventForm(forms.ModelForm):

    organization = forms.ModelChoiceField(queryset=Organization.objects.all())

    class Meta:
        model = Event
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
        fields = ['name', 'description', 'location', 'start_datetime', 'end_datetime', 'organization']

