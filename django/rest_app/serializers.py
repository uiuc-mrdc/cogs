from django.contrib.auth.models import User, Group
from rest_framework import serializers
from team_management.models import Game


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ['url', 'start_time', 'end_time', 'finished', 'pause_time']