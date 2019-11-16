from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect
from django.http import HttpResponse

from .models import ScoringType, Team

context_dict = {}
def index(request):
    
    return render(request, "team_management/index.html", context_dict)
    
def gameX(request, game_id): #game_id comes from the url
    dragon_ball_list = ScoringType.objects.filter(input_group="Dragon Ball")
    team_list = Team.objects.all()
    standard_buttons_list = ScoringType.objects.filter(input_group="Standard")
    
    context = {'game_id':game_id, 'team_list':team_list, 'standard_buttons_list':standard_buttons_list, 'dragon_ball_list':dragon_ball_list}
    return render(request, 'team_management/GameX.html',context)

def games(request):
    return render(request, 'team_management/games.html',{})