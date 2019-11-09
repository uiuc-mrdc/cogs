from channels.generic.websocket import WebsocketConsumer
import json
from django.utils import timezone
from .models import LiveScore, ScoringType, Team

class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action_id = ScoringType.objects.get(pk=text_data_json['action_id'])
        team_id = Team.objects.get(pk=text_data_json['team_id'])
        print(text_data_json)
        #self.send(text_data=json.dumps({
        #    'message': message
        #}))
        item = LiveScore(action_id=action_id, time=timezone.now(), team_id=team_id)
        item.save()
        
        print(LiveScore.objects.all())
        
        self.send('success!')