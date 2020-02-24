from channels.generic.websocket import WebsocketConsumer
import json
from django.utils import timezone
from .models import Action, ScoringType, Team, Game, GameParticipant
import pytz
from asgiref.sync import async_to_sync

class GameConsumer(WebsocketConsumer):
    groups = ["judges"]
    
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        
        dict_data = json.loads(text_data)
        print('went through receive', dict_data['type'])
        func = self.switcher.get(dict_data['type']) #switcher is at the bottom
        return func(self, dict_data) #These two lines implement a sort of switch statement based on the type to differentiate between adding/deleting/etc.
        
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
        
        async_to_sync(self.channel_layer.group_send)(
            "judges",
            {
            'type':'updateScore', #note that this one directly calls the updateScore method, rather than going through the receive method, since it is in a native python dict (I think)
            'participant_id':game_participant.id,
            'score':game_participant.score(),
        })
        
        self.send(text_data=json.dumps({
            'type':'deleteButton',
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
        
    def updateScore(self, dict_data):
        self.send(text_data=json.dumps(dict_data))
        
    switcher = { #must be defined after the functions
        'delete':deleteAction,
        'addStandardAction':addStandardAction,
        'updateCounterAction':updateCounterAction,
        'updateScore':updateScore,
    }