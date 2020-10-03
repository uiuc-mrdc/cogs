from django.contrib.auth.models import User, Group
from rest_framework import serializers
from team_management.models import Game, Team, ScoringType

#Rename to Match
class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ['url', 'id', 'start_time', 'end_time', 'finished', 'pause_time']
		
class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ['url', 'team_name', 'abbr', 'weigh_in', 'safety_check']
		
class ScoringTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScoringType
        fields = ['url', 'name', 'value']