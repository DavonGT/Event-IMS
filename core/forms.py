from django import forms
from .models import Event, Organization

class EventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = [
            'organization',
            'name', 'description', 'location', 
            'start_datetime', 'end_datetime', 'event_type'
            ]
        
        widgets = {
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
