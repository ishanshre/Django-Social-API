from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from chat.serializers import ChatSerializer, ChatEditSerializer
from chat.models import Chat

from django.db.models import Q

from chat.permissions import IsChatSender

class ChatModelViewSet(ModelViewSet):
    serializer_class = ChatSerializer
    http_method_names = ['get','put','delete','options','head']

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAuthenticated(), IsChatSender()]
        return [IsAuthenticated()]
    
    def get_serializer(self, *args, **kwargs):
        if self.request.method in ['PUT', 'DELETE']:
            return ChatEditSerializer
        return ChatSerializer
    
    def get_queryset(self):
        return Chat.objects.filter(Q(from_user=self.request.user)|Q(to_user=self.request.user))