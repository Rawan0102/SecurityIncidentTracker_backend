from django.contrib import admin
from .models import Profile, Incident, Report, Comment
admin.site.register(Profile)
admin.site.register(Incident)
admin.site.register(Report)
admin.site.register(Comment)