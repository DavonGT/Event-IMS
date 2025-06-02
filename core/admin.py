from django.contrib import admin

# Register your models here.

from .models import Event, Organization, College, ExtensionActivity

admin.site.register(Event)
admin.site.register(Organization)
admin.site.register(College)
admin.site.register(ExtensionActivity)