"""composeexample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('MatchQueue/', views.match_queue, name='match_queue'),
    path('Match/<int:match_id>/', views.match_x, name='match_x'),
    path('scoreboard/<int:match_id>/', views.scoreboard, name='scoreboard'),
    path('add_phone/', views.add_phone, name='add_phone'),
    #path('post_phone/', views.postPhone, name='post_phone'),
    path('WeighIn/', views.weigh_in, name='weigh_in'),
    #path('post_weigh_in/', views.postWeighIn, name='post_weigh_in'),
    #path('post_reset_weigh_in/', views.postResetWeighIn, name='post_reset_weigh_in'),
]
