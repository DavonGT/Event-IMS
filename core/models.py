from django.db import models
from django.conf import settings  # Import settings for custom user model

class Organization(models.Model):
    name = models.CharField(max_length=100)
    acronym = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return self.name

class Event(models.Model):

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  

    def __str__(self):
        return self.name
