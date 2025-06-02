from django import forms
from .models import Event, Organization, ExtensionActivity, College


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            if hasattr(user, 'role') and user.role == 'organizer':
                if user.organization:
                    self.fields['organization'].initial = user.organization.id
                    self.fields['organization'].disabled = True
            elif hasattr(user, 'role') and user.role == 'admin':
                self.fields['organization'].disabled = False
    
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
    
    

class UploadFileForm(forms.Form):
    organization_file = forms.FileField(label='Upload Organization CSV File')
    event_file = forms.FileField(label='Upload Event CSV File')

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['organization_file'].required = False
        self.fields['event_file'].required = False


class CollegeForm(forms.ModelForm):
    class Meta:
        model = College
        fields = ['name', 'acronym', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'College Name'}),
            'acronym': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Acronym'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 3}),
        }


class ExtensionActivityForm(forms.ModelForm):
    class Meta:
        model = ExtensionActivity
        fields = [
            'name', 'college', 'description', 
            'location', 'start_datetime', 'end_datetime'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Activity Name'}),
            'college': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }


