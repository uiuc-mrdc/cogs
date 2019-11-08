from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect
from django.http import HttpResponse

from .models import ScoringType

context_dict = {}
def index(request):
    
    return render(request, "team_management/index.html", context_dict)
    
def gameX(request):
    #DragonBallList = ScoringOptions.objects.filter(input_group="Dragon Ball Counters")
    
    standard_buttons_list = ScoringType.objects.filter(input_group="Standard")
    context = {'StandardButtonsList':standard_buttons_list}
    return render(request, 'team_management/GameX.html',context)
