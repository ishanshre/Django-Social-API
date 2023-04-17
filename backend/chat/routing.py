from django.urls import path

from chat.consumers import ChatJsonAsyncWebSockerConsumer


websocket_urlpatterns = [
    path("ws/chat/<str:groupName>/<int:receiver_pk>/", ChatJsonAsyncWebSockerConsumer.as_asgi()),
]