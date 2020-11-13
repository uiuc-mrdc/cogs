from team_management.models import School, Team, TeamContact, Match, MatchStateChangeEvent, ContenderPosition, Contender, ScoringContext, ContenderContextChangeEvent, ScoringTypeGroup, ScoringType, ScoringEvent
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
import rest_app.serializers as serializers
from rest_framework.response import Response
from rest_framework import status


class AvailableTeamsList(APIView): #Used by Match_Queue.html
	"""
	Lists Teams a user has permission to queue up for a Match
	"""
	def get(self, request, format=None):
		print(request.user.has_perm('team_management.can_queue_themselves'))
		print(request.user)
		if request.user.has_perm('team_management.can_queue_all_teams'):
			teams = Team.objects.all()
			serializer = serializers.TeamSerializer(teams, many=True, context={'request': request})
			return Response(serializer.data)
		elif request.user.has_perm('team_management.can_queue_themselves'):
			team = request.user.team
			serializer = serializers.TeamSerializer(team, context={'request': request})
			return Response(serializer.data)
		else:
			print('forbidden')
			return Response(status=status.HTTP_403_FORBIDDEN)
	
	
class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Teams to be viewed or edited.
    """
    queryset = Team.objects.all()
    serializer_class = serializers.TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

class TeamContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TeamContacts to be viewed or edited.
    """
    queryset = TeamContact.objects.all()
    serializer_class = serializers.TeamContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class SchoolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Schools to be viewed or edited.
    """
    queryset = School.objects.all()
    serializer_class = serializers.SchoolSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class ContenderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Contenders to be viewed or edited.
    """
    queryset = Contender.objects.all()
    serializer_class = serializers.ContenderSerializer
    permission_classes = [permissions.IsAuthenticated]

class MatchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows games to be viewed or edited.
    """
    queryset = Match.objects.all()
    serializer_class = serializers.MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

class MatchStateChangeEventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows MatchStateChangeEvents to be viewed or edited.
    """
    queryset = MatchStateChangeEvent.objects.all()
    serializer_class = serializers.MatchStateChangeEventSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContenderPositionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ContenderPositions to be viewed or edited.
    """
    queryset = ContenderPosition.objects.all()
    serializer_class = serializers.ContenderPositionSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContenderContextChangeEventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ContenderContextChangeEvents to be viewed or edited.
    """
    queryset = ContenderContextChangeEvent.objects.all()
    serializer_class = serializers.ContenderContextChangeEventSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScoringContextViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ScoringContexts to be viewed or edited.
    """
    queryset = ScoringContext.objects.all()
    serializer_class = serializers.ScoringContextSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScoringTypeGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ScoringTypeGroups to be viewed or edited.
    """
    queryset = ScoringTypeGroup.objects.all()
    serializer_class = serializers.ScoringTypeGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScoringTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows scoring types to be viewed or edited.
    """
    queryset = ScoringType.objects.all()
    serializer_class = serializers.ScoringTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
	
class ScoringEventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ScoringEvents to be viewed or edited.
    """
    queryset = ScoringEvent.objects.all()
    serializer_class = serializers.ScoringEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAuthenticated]