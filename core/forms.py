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
            'organization': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Organization Name'}),
            'name': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Event Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'location': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Location'}),
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }



class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'acronym', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization Name'}),
            'acronym': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Acronym'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }
