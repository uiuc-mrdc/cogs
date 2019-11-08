from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect
from django.http import HttpResponse

from .models import ScoringOptions

context_dict = {}
def index(request):
    
    return render(request, "team_management/index.html", context_dict)
    
def gameX(request):
    #DragonBallList = ScoringOptions.objects.filter(InputGroup="Dragon Ball Counters")
    
    StandardButtonsList = ScoringOptions.objects.filter(InputGroup="Standard")
    context = {'StandardButtonsList':StandardButtonsList}
    return render(request, 'team_management/gameX.html',context)