from channels.generic.websocket import WebsocketConsumer
import json
from django.utils import timezone
from .models import Action, ScoringType, Team, Game, GameParticipant
import pytz

class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        func = self.switcher.get(text_data_json['type']) #switcher is at the bottom
        return func(self, text_data_json) #These two lines implement a sort of switch statement based on the type to differentiate between adding/deleting/etc.
        
    def addStandardAction(self, json_data):
        scoring_type = ScoringType.objects.get(pk=json_data['scoringType_id'])
        game_participant = GameParticipant.objects.get(pk=json_data['participant_id'])
        multiplier = json_data['multiplier']
        action = Action(
            scoring_type = scoring_type, 
            time = timezone.now(), 
            game_participant = game_participant,
            multiplier = multiplier,
            value = 1)
        action.save()
        
        self.send(text_data=json.dumps({
            'team_name':game_participant.team.team_name,
            'action_id':action.id,
            'scoringType_name':scoring_type.name,
            'scoringType_id':scoring_type.id,
            'multiplier':multiplier,
            'time':action.time.astimezone(pytz.timezone('America/Chicago')).strftime("%H:%M:%S"),
        }))
    
    def updateCounterAction(self, json_data):
        scoring_type = ScoringType.objects.get(pk=json_data['scoringType_id'])
        participant_id = GameParticipant.objects.get(pk=json_data['participant_id'])
        multiplier = json_data['multiplier']
        value = json_data['value']
        action, created = Action.objects.get_or_create(
            scoring_type=scoring_type, 
            game_participant=participant_id)
        action.multiplier = multiplier
        #action.time = timezone.now()
        action.value = value
        action.save()
        #note there is no response, since it doesn't need a delete button
    
    def deleteAction(self, json_data):
        action = Action.objects.get(pk=json_data['action_id'])
        action.deleted = True
        action.save()
        
    switcher = { #must be defined after the functions
        'delete':deleteAction,
        'addStandardAction':addStandardAction,
        'updateCounterAction':updateCounterAction,
    }