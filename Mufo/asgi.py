"""
ASGI config for Mufo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mufo.settings')

# application = get_asgi_application()

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
# from Chat.routing import websocket_urlpatterns   # Import the websocket_urlpatterns variable
from Chat.consumer import  ChatConsumer , NotifConsumer,TestConsumer
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mufo.settings')
django_asgi_app = get_asgi_application()


websocket_urlpatterns = [
    path('ws/chats/<str:room_code>/', ChatConsumer.as_asgi()),
    path('ws/notif/', NotifConsumer.as_asgi()),
    path('ws/test/', TestConsumer.as_asgi())
]

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': URLRouter(websocket_urlpatterns),
})
