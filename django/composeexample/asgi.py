"""
ASGI config for {{ project_name }} project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
"""
Also see https://channels.readthedocs.io/en/latest/deploying.html#configuring-the-asgi-application 
    for a full example of a Django Channels asgi.py
"""

import os

from django.core.asgi import get_asgi_application
import team_management.routing
from channels.routing import ProtocolTypeRouter, URLRouter


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'composeexample.settings')
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            team_management.routing.websocket_urlpatterns
        )
    ),
})