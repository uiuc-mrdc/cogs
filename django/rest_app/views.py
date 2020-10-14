from team_management.models import Game, Team, ScoringType, GameParticipant
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import GameSerializer, TeamSerializer, ScoringTypeSerializer, GameParticipantSerializer


class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows games to be viewed or edited.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]

class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teams to be viewed or edited.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
	
class ScoringTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows scoring types to be viewed or edited.
    """
    queryset = ScoringType.objects.all()
    serializer_class = ScoringTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
	
class GameParticipantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows scoring types to be viewed or edited.
    """
    queryset = GameParticipant.objects.all()
    serializer_class = GameParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]