from django.db import models
from django.conf import settings  # Import settings for custom user model
from django.utils import timezone
from django.core.exceptions import ValidationError
import os

def validate_pdf(value):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != '.pdf':
        raise ValidationError('File must be a PDF document.')

class Organization(models.Model):
    name = models.CharField(max_length=100)
    acronym = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class College(models.Model):
    name = models.CharField(max_length=100)
    acronym = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class EventManager(models.Manager):
    def upcoming(self):
        return self.filter(start_datetime__gte=timezone.now()).order_by('start_datetime')

class Event(models.Model):
    TYPE_OF_EVENT = (
        ('University-Wide', 'university-wide'),
        ('College-Wide', 'college-wide'),
        ('Course-Specific', 'course-specific'),
    )

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    host = models.ForeignKey('accounts.User', on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    description = models.TextField(default='No description provided')
    location = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField() 
    event_type = models.CharField(max_length=20, choices=TYPE_OF_EVENT, default='College-Wide')
    soft_copy = models.FileField(
        upload_to='event_documents/',
        validators=[validate_pdf],
        help_text='Upload PDF document only',
        null=False,
        blank=False
    )

    objects = EventManager()
    def __str__(self):
        return self.name


class ExtensionActivity(models.Model):
    name = models.CharField(max_length=100)
    host = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='extension_activities')
    description = models.TextField(default='No description provided')
    location = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    soft_copy = models.FileField(
        upload_to='extension_documents/',
        validators=[validate_pdf],
        help_text='Upload PDF document only',
        null=False,
        blank=False
    )

    def __str__(self):
        return self.name





