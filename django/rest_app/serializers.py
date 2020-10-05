from django.contrib.auth.models import User, Group
from rest_framework import serializers
from team_management.models import Game, Team, ScoringType

#Rename to Match
class GameSerializer(serializers.HyperlinkedModelSerializer):
    gameparticipant_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True) #we can redefine the name of this in models.py with 'related_name'
    class Meta:
        model = Game
        fields = ['url', 'id', 'start_time', 'end_time', 'finished', 'pause_time', 'gameparticipant_set']
		
class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ['url', 'team_name', 'abbr', 'weigh_in', 'safety_check']
		
class ScoringTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScoringType
        fields = ['url', 'name', 'value']