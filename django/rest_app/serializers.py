from django.contrib.auth.models import User, Group
from rest_framework import serializers
from team_management.models import Game, Team, ScoringType, GameParticipant


		
class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ['url', 'team_name', 'abbr', 'weigh_in', 'safety_check']
		
class ScoringTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScoringType
        fields = ['url', 'name', 'value']
		
class GameParticipantSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    class Meta:
        model = GameParticipant
        fields = '__all__'
		
#Rename to Match
class GameSerializer(serializers.HyperlinkedModelSerializer):
    #gameparticipant_set = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='gameparticipant-detail') #we can redefine the name of this in models.py with 'related_name'
    gameparticipant_set = GameParticipantSerializer(many=True, read_only=True)
    class Meta:
        model = Game
        fields = '__all__'#['url', 'start_time', 'end_time', 'finished', 'pause_time', 'gameparticipant_set']