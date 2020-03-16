from django.shortcuts import render, get_object_or_404
from django.db import connection
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib import messages

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
    participant_list = GameParticipant.objects.filter(game=game_id).select_related('team')
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
    try:
        current_game = Game.objects.get(finished=False, start_time__lt=timezone.now()).gameparticipant_set.all().select_related('team').select_related('game')
    except ObjectDoesNotExist:
        current_game = []
    except MultipleObjectsReturned:
        messages.error(request, "Oops, there are >1 active games. Make sure only one game is started without being finalized")
        current_game = []
    
    upcoming_games = Game.objects.filter(finished=False, start_time__gt=timezone.now())
    upcoming_games_list = []
    for game in upcoming_games:
        teams = list(game.gameparticipant_set.all().order_by('color').select_related('team'))
        for i in range(4): # fills in missing teams with a simple dictionary
            try:
                if int(teams[i].color) != i+1:
                    teams.insert(i, {'game_id':game.id, 'color':0})
            except IndexError: #at the end of the list, append until limit is reached
                teams.append({'game_id':game.id, 'color':0})
        upcoming_games_list.append(teams)
    
    teams_list = Team.objects.all()
    
    finished_games = Game.objects.filter(finished=True).order_by('end_time')
    finished_games_list =[]
    for obj in finished_games:
        finished_games_list.append(obj.gameparticipant_set.all().select_related('team'))
    
    context = {
        "participant_list":current_game,
        "upcoming_games_list":upcoming_games_list,
        "teams_list":teams_list,
        "finished_games_list":finished_games_list,
    }
    return render(request, 'team_management/GameQueue.html', context)

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