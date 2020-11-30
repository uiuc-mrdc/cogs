from channels.generic.websocket import WebsocketConsumer
import json
from django.utils import timezone
from datetime import timedelta
import pytz
from asgiref.sync import async_to_sync
from django.db.models import CharField, TimeField, DateTimeField
from django.db.models.functions import Cast
from django.db.models.functions.datetime import TruncTime, TruncSecond

from . import custom_config as cfg

class MatchConsumer(WebsocketConsumer):
    
    def connect(self):
        #adds itself to the group for its game_id
        async_to_sync(self.channel_layer.group_add)(str(self.scope["url_route"]["kwargs"]["match_id"]), self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        #removes itself from the group
        async_to_sync(self.channel_layer.group_discard)(str(self.scope["url_route"]["kwargs"]["match_id"]), self.channel_name)
        pass

    def receive(self, text_data): #Only JSON messages from the client pass through this
        dict_data = json.loads(text_data)
        return

class MatchQueueConsumer(WebsocketConsumer):
    def connect(self):
        #adds itself to the group 'timer_only'
        async_to_sync(self.channel_layer.group_add)('timer_only', self.channel_name)
        async_to_sync(self.channel_layer.group_add)('match_queue', self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        #removes itself from the group
        async_to_sync(self.channel_layer.group_discard)('timer_only', self.channel_name)
        async_to_sync(self.channel_layer.group_discard)('match_queue', self.channel_name)
        pass
    
    def receive(self, text_data): #Only JSON messages from the client pass through this
        dict_data = json.loads(text_data)
        return