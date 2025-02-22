from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('chat/<str:userId>/<str:token>/', consumers.ChatConsumer.as_asgi()),
]