from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect
from django.http import HttpResponse

from .models import ScoringType, Team, Game, GameParticipant

def index(request):
    return render(request, "team_management/index.html", {})
    
def gameX(request, game_id): #game_id comes from the url
    counter_list = ScoringType.objects.filter(input_style="Counter")
    standard_buttons_list = ScoringType.objects.filter(input_style="Standard")
    
    participant_list = Game.objects.get(pk=game_id).gameparticipant_set.all()
    #participant_list = GameParticipant.objects.filter(game__id=game_id) #This and the line above return equivalent QuerySets, I think
    context = {
        'game_id':game_id, 
        'participant_list':participant_list,
        'standard_buttons_list':standard_buttons_list,
        'counter_list':counter_list
        }
    return render(request, 'team_management/GameX.html', context)

def games(request):
    return render(request, 'team_management/games.html', {})