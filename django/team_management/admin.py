from django.contrib import admin
from .models import ScoringType, Team, Action, Game, GameParticipant, Phone

from . import custom_config as cfg

#These are default and have no special layout. All fields appear except auto-fields or fields with editable=False
admin.site.register(ScoringType)
#admin.site.register(Team)
admin.site.register(Action) 
#admin.site.register(Game)
admin.site.register(GameParticipant)
admin.site.register(Phone)

#custom format for Game
class ParticipantInline(admin.TabularInline):
    model = GameParticipant
    extra = 2
    exclude = ('score',)
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Time Info', {'fields': ['start_time', 'end_time', 'pause_time']}),
        ('Other', {'fields': ['finished', 'special_name']}),
    ]
    inlines = [
        ParticipantInline,
    ]

#custom format for Team
class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 2
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [
        PhoneInline,
    ]