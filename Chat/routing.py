# from . import consumer
# from django.urls import path

# websocket_urlpatterns = [
#     path('ws/chat/<str:room_code>/', consumer.ChatConsumer.as_asgi()),
#     path('ws/notif/', consumer.NotifConsumer.as_asgi())
# ]

# routing.py

from . import consumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/chats/<str:room_code>/', consumer.ChatConsumer.as_asgi()),
    path('ws/notif/', consumer.NotifConsumer.as_asgi())
]
