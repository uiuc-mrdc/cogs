from django.contrib.auth.models import User, Group
from rest_framework import serializers
from team_management.models import School, Team, TeamContact, Match, MatchStateChangeEvent, ContenderPosition, Contender, ScoringContext, ContenderContextChangeEvent, ScoringTypeGroup, ScoringType, ScoringEvent

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class TeamContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TeamContact
        fields = '__all__'

class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    team_set = TeamSerializer(many=True, read_only=True)
    class Meta:
        model = School
        fields = '__all__'

class ContenderPositionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContenderPosition
        fields = '__all__'

class ContenderSerializer(serializers.HyperlinkedModelSerializer):
    team = TeamSerializer(read_only=True)
    score = serializers.IntegerField(max_value=None, min_value=None, source='calculate_score', read_only=True)
    contender_position = ContenderPositionSerializer(read_only=True)
    class Meta:
        model = Contender
        fields = '__all__'

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    #contenders = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='contender-detail') #This is the same as below in end result
    contenders = ContenderSerializer(many=True, read_only=True) #we can rename this in models.py with related_name
    class Meta:
        model = Match
        fields = '__all__'
        
class MatchStateChangeEventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MatchStateChangeEvent
        fields = '__all__'
        


class ContenderContextChangeEventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContenderContextChangeEvent
        fields = '__all__'

class ScoringContextSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScoringContext
        fields = '__all__'

class ScoringTypeGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScoringTypeGroup
        fields = '__all__'

class ScoringTypeSerializer(serializers.HyperlinkedModelSerializer):
    scoring_type_group = ScoringTypeGroupSerializer(read_only=True)
    class Meta:
        model = ScoringType
        fields = '__all__'

class ScoringEventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScoringEvent
        fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
        
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']