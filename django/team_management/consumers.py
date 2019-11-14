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
        scoring_type = ScoringType.objects.get(pk=text_data_json['scoringType_id'])
        team = Team.objects.get(pk=text_data_json['team_id'])
        print(text_data_json)
        #self.send(text_data=json.dumps({
        #    'message': message
        #}))
        item = LiveScore(scoring_type=scoring_type, time=timezone.now(), team=team)
        item.save()
        
        self.send(text_data=json.dumps({
            'team_name':team.team_name,
            'liveScore_id':item.id,
            'scoringType_name':scoring_type.name,
            'time':str(item.time),
        }))