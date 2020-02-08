from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect
from django.http import HttpResponse

from .models import ScoringType, Team, Game, GameParticipant

def index(request):
    print(GameParticipant.objects.get(pk=1).score())
    return render(request, "team_management/index.html", {})
    
def gameX(request, game_id): #game_id comes from the url
    dragon_list = ScoringType.objects.filter(input_style="Counter")
    treasurebox_list = ScoringType.objects.filter(input_style="Counter2")
    standard_buttons_list = ScoringType.objects.filter(input_style="Standard")
    
    participant_list = Game.objects.get(pk=game_id).gameparticipant_set.all()
    #participant_list = GameParticipant.objects.filter(game__id=game_id) #This and the line above return equivalent QuerySets, I think
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