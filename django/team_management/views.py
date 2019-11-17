from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect
from django.http import HttpResponse

from .models import ScoringType, Team

def index(request):
    return render(request, "team_management/index.html", {})
    
def gameX(request, game_id): #game_id comes from the url
    counter_list = ScoringType.objects.filter(input_style="Counter")
    team_list = Team.objects.all()
    standard_buttons_list = ScoringType.objects.filter(input_style="Standard")
    
    context = {'game_id':game_id, 'team_list':team_list, 'standard_buttons_list':standard_buttons_list, 'counter_list':counter_list}
    return render(request, 'team_management/GameX.html',context)

def games(request):
    return render(request, 'team_management/games.html', {})