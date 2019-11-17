from django.contrib import admin
from .models import ScoringType, Team, Action, Game

admin.site.register(ScoringType)
admin.site.register(Team)
admin.site.register(Action)
admin.site.register(Game)