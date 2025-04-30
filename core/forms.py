from django import forms
from django.contrib.auth import get_user_model
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'start_datetime', 'end_datetime', 'attendees']

    # Use get_user_model() to get the actual user model
    attendees = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.all(), required=False)
