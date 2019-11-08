from django.contrib import admin
from .models import Entry, ScoringOptions, Teams

admin.site.register(Entry)
admin.site.register(ScoringOptions)
admin.site.register(Teams)