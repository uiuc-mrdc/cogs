from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

def home(request):
    return render(request, "team_management/Home.html", {})

@permission_required('team_management.is_judge')
def match_x(request, match_id): #game_id comes from the url
    context={}
    return render(request, 'team_management/Match_X.html', context)

def scoreboard(request, match_id):
    context={}
    return render(request, 'team_management/Scoreboard.html', context)

def match_queue(request):
    context={}
    return render(request, 'team_management/Match_Queue.html', context)

@permission_required('team_management.is_judge')
def weigh_in(request):
    context={}
    return render(request, 'team_management/Weigh_In.html', context)

@login_required
def add_phone(request):
    context={}
    return render(request, 'team_management/Add_Phone.html', context)