from django.urls import re_path
from django.urls import path
from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    path("ws/Match/<int:match_id>", consumers.MatchConsumer.as_asgi(), name="MatchConsumer"),
    path("ws/MatchQueue", consumers.MatchQueueConsumer.as_asgi(), name="MatchQueueConsumer")
]