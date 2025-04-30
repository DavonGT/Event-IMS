from django.db import models
from django.conf import settings  # Import settings for custom user model

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Updated to use custom user model
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="attended_events")  # Updated

    def __str__(self):
        return self.name
