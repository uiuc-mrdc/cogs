from channels.generic.websocket import WebsocketConsumer
import json
from django.utils import timezone
from .models import LiveScore, ScoringType

class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action_id = text_data_json['action_id']
        team_id = text_data_json['team_id']
        print(text_data_json)
        #self.send(text_data=json.dumps({
        #    'message': message
        #}))
        print(ScoringType.objects.filter(id=2))
        
        #item = LiveScore(action_id="Brew Potion", time=timezone.now(), team_id=team_id)
        #item.save()
        
        print(LiveScore.objects.all())
        item2 = LiveScore.objects.get(id=1)
        print(item2.action_id)
        
        #self.send(str(item.action_id))