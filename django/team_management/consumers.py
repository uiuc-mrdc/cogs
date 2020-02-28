from channels.generic.websocket import WebsocketConsumer
import json
from django.utils import timezone
from .models import Action, ScoringType, Team, Game

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
        team = Team.objects.get(pk=json_data['team_id'])
        game = Game.objects.get(pk=json_data['game_id'])
        multiplier = json_data['multiplier']
        action = Action(
            scoring_type = scoring_type, 
            time = timezone.now(), 
            team = team, 
            multiplier = multiplier,
            game = game)
        action.save()
        
        self.send(text_data=json.dumps({
            'team_name':team.team_name,
            'action_id':action.id,
            'scoringType_name':scoring_type.name,
            'scoringType_id':scoring_type.id,
            'time':str(action.time),
        }))
    
    def addCounterAction(self, json_data):
        scoring_type = ScoringType.objects.get(pk=json_data['scoringType_id'])
        team = Team.objects.get(pk=json_data['team_id'])
        game = Game.objects.get(pk=json_data['game_id'])
        #multiplier = ?????
        direction = json_data['value']
        action = Action(scoring_type=scoring_type, time=timezone.now(), team=team, game=game, upDown=direction)
        action.save()
        #note there is no response, since it doesn't need a delete button
    
    def deleteAction(self, json_data):
        action = Action.objects.get(pk=json_data['action_id'])
        action.deleted = True
        action.save()
        
    switcher = { #must be defined after the functions
        'delete':deleteAction,
        'addStandardAction':addStandardAction,
        'addCounterAction':addCounterAction,
    }
    
class ExternalScriptConsumer(WebsocketConsumer):
    def connect(self):
        #adds itself to the group 'timer_only'
        async_to_sync(self.channel_layer.group_add)('timer_only', self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        #removes itself from the group
        async_to_sync(self.channel_layer.group_discard)('timer_only', self.channel_name)
        pass
    
    def StartGame(self, dict_data): #sends end_time and game_id #also used to restart the game after pausing
        self.send(text_data=json.dumps(dict_data))

    def PauseGame(self, dict_data): #sends time_remaining (in milliseconds) and game_id
        self.send(text_data=json.dumps(dict_data))

    def FinalizeGame(self, dict_data): #sends game_id
        self.send(text_data=json.dumps(dict_data))
        
    def groupUpdateScore(self, dict_data): ##Needs to be sent game_id and participant_id
        game_participant = GameParticipant.objects.get(pk=dict_data['participant_id'])
        
        async_to_sync(self.channel_layer.group_send)(
            dict_data['game_id'],
            {
            'type':'clientUpdateScore',
            'participant_id':game_participant.id,
            'score':game_participant.calculateScore(),
        })
    