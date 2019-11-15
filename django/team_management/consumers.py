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
        func = self.switcher.get(text_data_json['type']) #switcher is at the bottom
        return func(self, text_data_json) #These two lines implement a sort of switch statement based on the type to differentiate between adding/deleting/etc.
        
    def standardLiveScore(self, json_data):
        scoring_type = ScoringType.objects.get(pk=json_data['scoringType_id'])
        team = Team.objects.get(pk=json_data['team_id'])
        live_score = LiveScore(scoring_type=scoring_type, time=timezone.now(), team=team)
        live_score.save()
        
        self.send(text_data=json.dumps({
            'team_name':team.team_name,
            'liveScore_id':live_score.id,
            'scoringType_name':scoring_type.name,
            'scoringType_id':scoring_type.id,
            'time':str(live_score.time),
        }))
    
    def counterLiveScore(self, json_data):
        scoring_type = ScoringType.objects.get(pk=json_data['scoringType_id'])
        team = Team.objects.get(pk=json_data['team_id'])
        live_score = LiveScore(scoring_type=scoring_type, time=timezone.now(), team=team)
        live_score.save()
        #note there is no response, since it doesn't need a delete button
    
    def deleteLiveScore(self, json_data):
        LiveScore.objects.get(pk=json_data['scoringType_id']).delete() #Passes LiveScore.id as ScoringType.id to save data space
        
    switcher = { #must be defined after the functions
        'delete':deleteLiveScore,
        'standardLiveScore':standardLiveScore,
        'counterLiveScore':counterLiveScore,
    }