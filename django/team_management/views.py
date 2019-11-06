from django.shortcuts import render
from django.db import connection
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

context_dict = {}
def index(request):
    
    return render(request, "team_management/index.html", context_dict)
