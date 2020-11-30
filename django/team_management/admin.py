'''
Add custome admin items where useful. For example, customize so we can edit MatchStateChangeEvent in Match
'''
from django.contrib import admin
from .models import School, Team, TeamContact, Match, MatchStateChangeEvent, ContenderPosition, Contender, ScoringContext, ContenderContextChangeEvent, ScoringTypeGroup, ScoringType, ScoringEvent

#These are default and have no special layout. All fields appear except auto-fields or fields with editable=False
admin.site.register(School)
#admin.site.register(Team)
admin.site.register(TeamContact)
#admin.site.register(Match)
admin.site.register(MatchStateChangeEvent)
admin.site.register(ContenderPosition)
admin.site.register(Contender)
admin.site.register(ScoringContext)
admin.site.register(ContenderContextChangeEvent)
admin.site.register(ScoringTypeGroup)
admin.site.register(ScoringType)
admin.site.register(ScoringEvent)



#custom format for Match
class ContenderInline(admin.TabularInline):
    model = Contender
    extra = 2
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    inlines = [
        ContenderInline,
    ]

#custom format for Team
class TeamContactInline(admin.TabularInline):
    model = TeamContact
    extra = 2
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [
        TeamContactInline,
    ]