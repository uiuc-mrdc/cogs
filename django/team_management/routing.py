from django.urls import re_path
from django.urls import path
from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    path("ws/Match/<int:match_id>", consumers.MatchConsumer, name="MatchConsumer"),
    path("ws/MatchQueue", consumers.MatchQueueConsumer, name="MatchQueueConsumer")
]