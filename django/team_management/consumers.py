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
        func = self.switcher.get(text_data_json['type']) 
        return func(self, text_data_json) #These two lines implement a sort of switch statement based on the type to differentiate between adding/deleting/etc.
        
    def addLiveScore(self, json_data):
        scoring_type = ScoringType.objects.get(pk=json_data['scoringType_id'])
        team = Team.objects.get(pk=json_data['team_id'])
        print(json_data)
        #self.send(text_data=json.dumps({
        #    'message': message
        #}))
        item = LiveScore(scoring_type=scoring_type, time=timezone.now(), team=team)
        item.save()
        
        self.send(text_data=json.dumps({
            'team_name':team.team_name,
            'liveScore_id':item.id,
            'scoringType_name':scoring_type.name,
            'scoringType_id':scoring_type.id,
            'time':str(item.time),
        }))
    
    def deleteLiveScore(self, json_data):
        print(json_data)
        LiveScore.objects.get(pk=json_data['scoringType_id']).delete() #Passes LiveScore.id as ScoringType.id to save data space
    
    switcher = {
        'delete':deleteLiveScore,
        'addLiveScore':addLiveScore,
    }