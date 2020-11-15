from team_management.models import School, Team, TeamContact, Match, MatchStateChangeEvent, ContenderPosition, Contender, ScoringContext, ContenderContextChangeEvent, ScoringTypeGroup, ScoringType, ScoringEvent
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
import rest_app.serializers as serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import action

class AvailableTeamsList(generics.ListAPIView): #Used by Match_Queue.html
	"""
	Lists Teams a user has permission to queue up for a Match
	"""
	serializer_class = serializers.TeamSerializer
	def get_queryset(self):
		print(self.request.user.has_perm('team_management.can_queue_themselves'))
		print(self.request.user)
		if self.request.user.has_perm('team_management.can_queue_all_teams'):
			return Team.objects.all()
		elif self.request.user.has_perm('team_management.can_queue_themselves'):
			return [self.request.user.team] #this model instance must act like a queryset, not a single instance
		else:
			return []
	
	
class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Teams to be viewed or edited.
    """
    queryset = Team.objects.all()
    serializer_class = serializers.TeamSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class TeamContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TeamContacts to be viewed or edited.
    """
    queryset = TeamContact.objects.all()
    serializer_class = serializers.TeamContactSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    
class SchoolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Schools to be viewed or edited.
    """
    queryset = School.objects.all()
    serializer_class = serializers.SchoolSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class ContenderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Contenders to be viewed or edited.
    """
    queryset = Contender.objects.all()
    serializer_class = serializers.ContenderSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    #custom action to use a non-nested version of the serializer, so we can POST with only the primary keys
    #Note that it also responds with the entire match so the client can rebuild the entire match
    @action(detail=False, methods=['post'], serializer_class=serializers.ContenderSerializer)
    def new_contender(self, request, pk=None):
        serializer = serializers.NonNestedContenderSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            contender = serializer.save()
            response_data = serializers.MatchSerializer(contender.match, context={'request':request}).data
            response_data['type'] = 'new_contender'
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'match_queue',
                response_data)
            return Response(response_data)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

class MatchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows games to be viewed or edited.
    """
    queryset = Match.objects.all()
    serializer_class = serializers.MatchSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    #mimics the normal create method and sends a websocket message
    def create(self, *args, **kwargs):
        response = super().create(*args, **kwargs)
        response.data['type'] = 'new_blank_match'
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'match_queue',
            response.data)
        return response 

class MatchStateChangeEventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows MatchStateChangeEvents to be viewed or edited.
    """
    queryset = MatchStateChangeEvent.objects.all()
    serializer_class = serializers.MatchStateChangeEventSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class ContenderPositionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ContenderPositions to be viewed or edited.
    """
    queryset = ContenderPosition.objects.all()
    serializer_class = serializers.ContenderPositionSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class ContenderContextChangeEventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ContenderContextChangeEvents to be viewed or edited.
    """
    queryset = ContenderContextChangeEvent.objects.all()
    serializer_class = serializers.ContenderContextChangeEventSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class ScoringContextViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ScoringContexts to be viewed or edited.
    """
    queryset = ScoringContext.objects.all()
    serializer_class = serializers.ScoringContextSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class ScoringTypeGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ScoringTypeGroups to be viewed or edited.
    """
    queryset = ScoringTypeGroup.objects.all()
    serializer_class = serializers.ScoringTypeGroupSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class ScoringTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows scoring types to be viewed or edited.
    """
    queryset = ScoringType.objects.all()
    serializer_class = serializers.ScoringTypeSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
	
class ScoringEventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ScoringEvents to be viewed or edited.
    """
    queryset = ScoringEvent.objects.all()
    serializer_class = serializers.ScoringEventSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]