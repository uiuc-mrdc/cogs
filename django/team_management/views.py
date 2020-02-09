from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect
from django.http import HttpResponse

from .models import ScoringType, Team, Game, GameParticipant

def index(request):
    return render(request, "team_management/index.html", {})
    
def gameX(request, game_id): #game_id comes from the url
    dragon_list = ScoringType.objects.filter(input_style="Counter")
    treasurebox_list = ScoringType.objects.filter(input_style="Counter2")
    standard_buttons_list = ScoringType.objects.filter(input_style="Standard")
    
    #participant_list = Game.objects.get(pk=game_id).gameparticipant_set.all().select_related('team')
    participant_list = GameParticipant.objects.filter(game=game_id).select_related('team') #These two lines return equivalent querysets for Django, but the unused one hits the database twice. Also, select_related saves 4 queries, since it would have to fetch the team name every time it is requested, but select_related just joins it now

    context = {
        'game_id':game_id, 
        'participant_list':participant_list,
        'standard_buttons_list':standard_buttons_list,
        'dragon_list':dragon_list,
        'treasurebox_list':treasurebox_list,
        }
    return render(request, 'team_management/GameX.html', context)

def games(request):
    return render(request, 'team_management/games.html', {})