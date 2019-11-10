from django.contrib import admin
from .models import ScoringType, Team, LiveScore

admin.site.register(ScoringType)
admin.site.register(Team)
admin.site.register(LiveScore)
