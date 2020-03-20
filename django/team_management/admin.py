from django.contrib import admin
from .models import ScoringType, Team, Action, Game, GameParticipant, Phone

#We won't need all of these in the admin site eventually. Probably not Action
admin.site.register(ScoringType)
admin.site.register(Team)
admin.site.register(Action) 
admin.site.register(Game)
admin.site.register(GameParticipant)
admin.site.register(Phone)