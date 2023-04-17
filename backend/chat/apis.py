from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from chat.serializers import ChatSerializer
from chat.models import Chat



class ChatModelViewSet(ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['GET','PUT','DELETE','OPTIONS','HEAD']
    
    def get_queryset(self):
        return Chat.objects.filter(from_user=self.request.user)