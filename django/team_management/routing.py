from django.urls import re_path
from django.urls import path
from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    path("ws/game/<int:game_id>", consumers.GameConsumer, name="gameConsumer"),
]