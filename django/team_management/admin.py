from django.contrib import admin
from .models import ScoringType, Team, Action, Game, GameParticipant

admin.site.register(ScoringType)
admin.site.register(Team)
admin.site.register(Action)
admin.site.register(Game)
admin.site.register(GameParticipant)