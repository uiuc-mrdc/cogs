from channels.generic.websocket import WebsocketConsumer
import json
from django.utils import timezone
from datetime import timedelta
from .models import Action, ScoringType, Team, Game, GameParticipant
import pytz
from asgiref.sync import async_to_sync
from django.db.models import CharField, TimeField, DateTimeField
from django.db.models.functions import Cast
from django.db.models.functions.datetime import TruncTime, TruncSecond

from . import custom_config as cfg

class GameConsumer(WebsocketConsumer):
    
    def connect(self):
        #adds itself to the group for its game_id
        async_to_sync(self.channel_layer.group_add)(str(self.scope["url_route"]["kwargs"]["game_id"]), self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        #removes itself from the group
        async_to_sync(self.channel_layer.group_discard)(str(self.scope["url_route"]["kwargs"]["game_id"]), self.channel_name)
        pass

    def receive(self, text_data): #Only JSON messages from the client pass through this
        dict_data = json.loads(text_data)
        func = self.switcher.get(dict_data['type']) #switcher is at the bottom
        return func(self, dict_data) #These two lines implement a sort of switch statement based on the type to differentiate between adding/deleting/etc.
        
    def addStandardAction(self, json_data):
        scoring_type = ScoringType.objects.get(pk=json_data['scoringType_id'])
        game_participant = GameParticipant.objects.get(pk=json_data['participant_id'])
        multiplier = json_data['multiplier']
        #updates db
        action = Action(
            scoring_type = scoring_type, 
            time = timezone.now(), 
            game_participant = game_participant,
            multiplier = multiplier,
            value = 1)
        action.save()
        
        #sends updated score to the group
        self.groupUpdateScore(game_participant)

        #sends response for making delete button ##This is necessary to store the action id
        self.send(text_data=json.dumps({
            'type':'deleteButton',
            'action_id':action.id,
            'scoring_type_name':scoring_type.name,
            'scoring_type_id':scoring_type.id,
            'multiplier':multiplier,
            'time':action.time.astimezone(pytz.timezone('America/Chicago')).strftime("%H:%M:%S"),
        }))
    
    def updateCounterAction(self, json_data):
        scoring_type = ScoringType.objects.get(pk=json_data['scoringType_id'])
        game_participant = GameParticipant.objects.get(pk=json_data['participant_id'])
        multiplier = json_data['multiplier']
        value = json_data['value']
        action, created = Action.objects.get_or_create(#If it doesn't exist yet creates the db row
            scoring_type=scoring_type, 
            game_participant=game_participant)
        #updates the db row's values
        action.multiplier = multiplier
        action.time = timezone.now()
        action.value = value
        action.save()
        
        self.groupUpdateScore(game_participant)
        
        #note there is no response, since it doesn't need a delete button
    
    def deleteAction(self, json_data):
        action = Action.objects.get(pk=json_data['action_id'])
        action.deleted = True
        action.save()
        self.groupUpdateScore(action.game_participant)
   
    def changeTeam(self, dict_data):
        action_list = list(Action.objects.filter(
            game_participant=dict_data['participant_id']
        ).filter(
            deleted=False
        ).order_by('scoring_type', 'id'
        ).values(
            'id',
            'scoring_type',
            'value', 
            'multiplier',
            #truncates the decimal off the seconds, then truncates down to the time, then casts it as a string
            str_time = Cast(TruncTime(TruncSecond('time', DateTimeField(), tzinfo=pytz.timezone('UTC')), TimeField(), tzinfo=pytz.timezone('America/Chicago')), CharField())
        ))
        
        self.send(text_data=json.dumps({
            'type': 'changeTeam',
            'actions': action_list
        }))
    
    def groupStartGame(self, dict_data):
        game_length = cfg.game_length #GAME LENGTH (minutes)
        end_time = timezone.now() + timedelta(minutes=game_length)
        game = Game.objects.get(pk=dict_data['game_id'])
        game.end_time = end_time
        game.start_time = end_time - timedelta(minutes=game_length)
        game.save()
        async_to_sync(self.channel_layer.group_send)(
            str(dict_data['game_id']),
            {
            'type':'clientStartGame', #note that this one directly calls the clientUpdateScore method, rather than going through the receive method, since it is in a native python dict
            'end_time':end_time.astimezone(pytz.timezone('America/Chicago')).strftime("%m/%d/%Y, %H:%M:%S") 
        })
        async_to_sync(self.channel_layer.group_send)(
            "timer_only",
            {
            'type':'StartGame', #note that this one directly calls the clientUpdateScore method, rather than going through the receive method, since it is in a native python dict
            'game_id':dict_data['game_id'],
            'end_time':end_time.astimezone(pytz.timezone('America/Chicago')).strftime("%m/%d/%Y, %H:%M:%S") 
        })
    def clientStartGame(self, dict_data):
        self.send(text_data=json.dumps(dict_data))
    def groupPauseGame(self, dict_data):
        game = Game.objects.get(pk=dict_data['game_id'])
        game.pause_time = timedelta(milliseconds=dict_data['time_remaining'])
        game.save()
        async_to_sync(self.channel_layer.group_send)(
            str(dict_data['game_id']),
            {
            'type':'clientPauseGame', #note that this one directly calls the clientUpdateScore method, rather than going through the receive method, since it is in a native python dict
            'time_remaining':dict_data['time_remaining']
        })
        async_to_sync(self.channel_layer.group_send)(
            "timer_only",
            {
            'type':'PauseGame',
            'time_remaining':dict_data['time_remaining']
        })
    def clientPauseGame(self, dict_data):
        self.send(text_data=json.dumps(dict_data))
    def groupRestartGame(self, dict_data):
        end_time = timezone.now() + timedelta(milliseconds=dict_data['time_remaining'])
        game = Game.objects.get(pk=dict_data['game_id'])
        game.end_time = end_time
        game.pause_time = timedelta(seconds=0)
        game.save()
        #note this is identical to groupStartGame from this point forward
        async_to_sync(self.channel_layer.group_send)(
            str(dict_data['game_id']),
            {
            'type':'clientStartGame', #note that this one directly calls the clientUpdateScore method, rather than going through the receive method, since it is in a native python dict
            'end_time':end_time.astimezone(pytz.timezone('America/Chicago')).strftime("%m/%d/%Y, %H:%M:%S")
        })
        async_to_sync(self.channel_layer.group_send)(
            "timer_only",
            {
            'type':'StartGame', #note that this one directly calls the clientUpdateScore method, rather than going through the receive method, since it is in a native python dict
            'game_id':dict_data['game_id'],
            'end_time':end_time.astimezone(pytz.timezone('America/Chicago')).strftime("%m/%d/%Y, %H:%M:%S")
        })
    def groupFinalizeGame(self, dict_data):
        game = Game.objects.get(pk=dict_data['game_id'])
        game.finished = True
        game.save()
        async_to_sync(self.channel_layer.group_send)(
            str(dict_data['game_id']),
            {
            'type':'clientFinalizeGame', #note that this one directly calls the clientFinalizeGame method, rather than going through the receive method, since it is in a native python dict
            'game_id':dict_data['game_id']
        })
        async_to_sync(self.channel_layer.group_send)(
            "timer_only",
            {
            'type':'FinalizeGame', #note that this one directly calls the clientFinalizeGame method, rather than going through the receive method, since it is in a native python dict
            'game_id':dict_data['game_id']
        })
    def clientFinalizeGame(self, dict_data):
        self.send(text_data=json.dumps(dict_data))
    #updates score for all clients in the group for this game_participant's game_id
    def groupUpdateScore(self, game_participant):
        async_to_sync(self.channel_layer.group_send)(
            str(game_participant.game_id),
            {
            'type':'clientUpdateScore', #note that this one directly calls the clientUpdateScore method, rather than going through the receive method, since it is in a native python dict
            'participant_id':game_participant.id,
            'score':game_participant.calculateScore(),
        })
        async_to_sync(self.channel_layer.group_send)(
            'game_queue',
            {
            'type':'UpdateScore', #note that this one directly calls the clientUpdateScore method, rather than going through the receive method, since it is in a native python dict
            'participant_id':game_participant.id,
            'score':game_participant.calculateScore(),
            'game_id':game_participant.game_id
        })
        
    def clientUpdateScore(self, dict_data): #when received from the group, sends the same data on to the client
        self.send(text_data=json.dumps(dict_data))
        
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
    def UpdateScore(self, dict_data): #sends score, game_id, and participant_id
        self.send(text_data=json.dumps(dict_data))
    
    def groupNewParticipant(self, dict_data):
        new_participant = GameParticipant(
            team = Team.objects.get(pk=dict_data['team_id']),
            game = Game.objects.get(pk=dict_data['game_id']),
            color = dict_data['color'],
        )
        new_participant.save()
