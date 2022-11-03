from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("stomp", consumers.StompWebSocketConsumer.as_asgi()),
]
