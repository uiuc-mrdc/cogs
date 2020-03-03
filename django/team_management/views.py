from django.shortcuts import render, get_object_or_404
from django.db import connection
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import permission_required

from .models import ScoringType, Team, Game, GameParticipant, Phone

def index(request):
    return render(request, "team_management/index.html", {})

@permission_required('team_management.judge')
def gameX(request, game_id): #game_id comes from the url
    dragon_list = ScoringType.objects.filter(input_style="Counter")
    treasurebox_list = ScoringType.objects.filter(input_style="Counter2")
    standard_buttons_list = ScoringType.objects.filter(input_style="Standard")
    
    #participant_list = Game.objects.get(pk=game_id).gameparticipant_set.all().select_related('team')
    participant_list = GameParticipant.objects.filter(game=game_id).select_related('team') #These two lines return equivalent querysets for Django, but the unused one hits the database twice. Also, select_related saves 4 queries, since it would have to fetch the team name every time it is requested, but select_related just joins it now
    
    game = Game.objects.get(pk=game_id)
    
    game_started = (game.start_time < timezone.now())
    context = {
        'game':game, 
        'game_started':game_started,
        'participant_list':participant_list,
        'standard_buttons_list':standard_buttons_list,
        'dragon_list':dragon_list,
        'treasurebox_list':treasurebox_list,
        }
    return render(request, 'team_management/GameX.html', context)
    
def scoreboard(request, game_id):
    participant_list = GameParticipant.objects.filter(game=game_id).select_related('team') #These two lines return equivalent querysets for Django, but the unused one hits the database twice. Also, select_related saves 4 queries, since it would have to fetch the team name every time it is requested, but select_related just joins it now
    try:
        game = Game.objects.get(pk=game_id)
        game_started = (game.start_time < timezone.now())
    except: 
        game = {'id':game_id}
        game_started = False
    context = {
        'game':game,
        'game_started':game_started,
        'participant_list':participant_list,
    }
    return render(request, 'team_management/scoreboard.html', context)

def games(request):
    return render(request, 'team_management/games.html', {})

def postPhone(request):
    try:
        print(request.POST)
        team = Team.objects.get(pk=request.POST['team_id'])
        print('no error')
    except:
        teams_list = Team.objects.all()
        context = {'teams_list':teams_list,
            'error_message': "Please select a team"
            }
        return render(request, 'team_management/addPhone.html', context)
    else:
    
        phone = Phone(
            number = request.POST['num'],
            team = team,
            )
        phone.save()
        return HttpResponseRedirect(reverse('index'))

@login_required
def addPhone(request):
    teams_list = Team.objects.all()
    print(teams_list)
    context={'teams_list':teams_list}
    return render(request, 'team_management/addPhone.html', context)