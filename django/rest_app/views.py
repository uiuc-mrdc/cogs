from team_management.models import Game
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows games to be viewed or edited.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
