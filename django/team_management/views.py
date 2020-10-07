from django.shortcuts import render, get_object_or_404
from django.db import connection
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils import timezone
'''
Remove unused models
'''
from .models import School, Team, TeamContact, Match, MatchStateChangeEvent, ContenderPosition, Contender, ScoringContext, ContenderContextChangeEvent, ScoringTypeGroup, ScoringType, ScoringEvent
from . import custom_config as cfg

def home(request):
    return render(request, "team_management/Home.html", {})

@permission_required('team_management.is_judge')
def match_x(request, match_id): #game_id comes from the url
    ''' Handle all in API
    dragon_list = ScoringType.objects.filter(input_style="Counter")
    treasurebox_list = ScoringType.objects.filter(input_style="Counter2")
    standard_buttons_list = ScoringType.objects.filter(input_style="Standard")
    
    #participant_list = Game.objects.get(pk=game_id).gameparticipant_set.all().select_related('team')
    participant_list = GameParticipant.objects.filter(game=game_id).select_related('team') #These two lines return equivalent querysets for Django, but the unused one hits the database twice. Also, select_related saves 4 queries, since it would have to fetch the team name every time it is requested, but select_related just joins it now
    
    game = Game.objects.get(pk=game_id)
    
    game_started = (game.start_time < timezone.now())
    
    try:
        Game.objects.get(finished=False, start_time__lt=timezone.now())
        other_active_game = True
    except ObjectDoesNotExist:
        other_active_game = False

    context = {
        'game':game, 
        'game_started':game_started,
        'participant_list':participant_list,
        'standard_buttons_list':standard_buttons_list,
        'dragon_list':dragon_list,
        'treasurebox_list':treasurebox_list,
        'game_length':cfg.game_length,
        'other_active_game':other_active_game,
        }
    '''
    context={}
    return render(request, 'team_management/GameX.html', context)
    
def scoreboard(request, game_id):
    ''' Use API
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
        'game_length':cfg.game_length,
        'time_between_matches':cfg.time_between_matches,
    }
    '''
    context={}
    return render(request, 'team_management/scoreboard.html', context)

def match_queue(request):
    ''' use API
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
        for i in range(cfg.teams_per_game): # fills in missing teams with a simple dictionary
            try:
                if int(teams[i].color) != i+1:
                    teams.insert(i, {'game_id':game.id, 'color':0})
            except IndexError: #at the end of the list, append until limit is reached
                teams.append({'game_id':game.id, 'color':0})
        upcoming_games_list.append(teams)
    
    
IS THIS A VALID USE OF TEMPLATING?
    empty_game = []
    for i in range(cfg.teams_per_game):
        empty_game.append({})
    
    teams_list = Team.objects.all()
    
    finished_games = Game.objects.filter(finished=True).order_by('-end_time')
    finished_games_list =[]
    for obj in finished_games:
        finished_games_list.append(obj.gameparticipant_set.all().select_related('team'))
    
    context = {
        "participant_list":current_game,
        "upcoming_games_list":upcoming_games_list,
        "teams_list":teams_list,
        "finished_games_list":finished_games_list,
        "empty_game":empty_game,
        "game_length":cfg.game_length,
        "time_between_matches":cfg.time_between_matches,
    }
    '''
    context={}
    return render(request, 'team_management/GameQueue.html', context)

''' use API. All handled in the JS
def postWeighIn(request):
    
    try:
        team = Team.objects.get(pk=request.POST['team_id'])
    except: #If no valid team, send back with an error
        teams_list = Team.objects.all()
        context = {
            'teams_list':teams_list,
            'error_message': "Please select a team"
            }
        return render(request, 'team_management/WeighIn.html', context)
    else: #check and update both weight and safety if the team was valid
        try:
            if request.POST['weight'] == 'on': 
                weight = True            
        except: 
            weight = False
        finally:
            try:
                if request.POST['safety'] == 'on':
                    safety = True
            except:
                safety = False
            finally:
                team.weigh_in = weight
                team.safety_check = safety
                team.save()
                return HttpResponseRedirect(reverse('weigh_in'))
'''


''' Should still be handled by the API. We may need a custom API view to do this
def postResetWeighIn(request):
    
    teams = Team.objects.all()
    
    for team in teams:
        team.weigh_in = False
        team.safety_check = False
    
    Team.objects.bulk_update(teams, ['weigh_in', 'safety_check'])
    return HttpResponseRedirect(reverse('home'))
'''

@permission_required('team_management.is_judge')
def weigh_in(request):
    ''' API
    teams_list = Team.objects.all()
    context={'teams_list':teams_list}
    '''
    context={}
    return render(request, 'team_management/WeighIn.html', context)

''' API
def postPhone(request):
    try:
        team = Team.objects.get(pk=request.POST['team_id'])
    except:
        teams_list = Team.objects.all()
        context = {
            'teams_list':teams_list,
            'error_message': "Please select a team"
            }
        return render(request, 'team_management/addPhone.html', context)
    else:
        if request.POST['num'] != "8005551234": #does not save if it is the defualt number
            phone = Phone(
                number = request.POST['num'],
                team = team,
                )
            phone.save()
        return HttpResponseRedirect(reverse('home'))
'''


@login_required
def add_phone(request):
    ''' API
    teams_list = Team.objects.all().order_by('team_name')
    context={'teams_list':teams_list}
    '''
    context={}
    return render(request, 'team_management/addPhone.html', context)