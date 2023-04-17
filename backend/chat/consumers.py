from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
import json

from chat.models import Group, Chat

from django.contrib.auth import get_user_model

User = get_user_model()

class ChatJsonAsyncWebSockerConsumer(AsyncJsonWebsocketConsumer):
    """
        Inheriting AsyncJsonWebsokcerConsumer. It has built in functionality for encoding and decoding json
    """

    @database_sync_to_async
    def create_chat(self, content, receiver_pk):
        group = Group.objects.get(name=self.groupName)
        from_user = self.user
        to_user = User.objects.get(id=receiver_pk)
        chat = Chat.objects.create(
            content=content,
            group=group,
            from_user=from_user,
            to_user=to_user
        )
        chat.save()
        return chat

    @database_sync_to_async
    def create_group(self, name):
        group, created = Group.objects.get_or_create(name=name)
        return group
        

    async def connect(self):
        print("Json web socket is open")
        print("channel Layer: ", self.channel_layer)
        print("channel_name:::", self.channel_name)
        self.user = self.scope['user']
        print(type(self.user))
        self.groupName = self.scope['url_route']['kwargs']['groupName']
        self.group = await self.create_group(self.groupName)
        await self.channel_layer.group_add(self.groupName, self.channel_name)
        await self.accept()
    
    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        print("Message from client ---:", text_data)
        data = json.loads(text_data)
        print("actual_msg: ", data['content'])
        content = data['content']
        receiver_pk = self.scope['url_route']['kwargs']['receiver_pk']
        if self.user.is_authenticated:
            chat = await self.create_chat(content, receiver_pk)
            await self.channel_layer.group_send(self.groupName, {
                "type":"chat.message",
                "content":chat.content
            })
        else:
            await self.send_json({"error":"login required"})
    
    async def chat_message(self, event):
        print("chat message:, ", event)
        await self.send_json(
            {
                "content":event['content'],
                "username":self.user.username
            }
        )
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.groupName,
            self.channel_name
        )