from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

from friend.models import Friend
from friend.serializers import (
    FriendSerializer,
    FriendCreateSerialzer,
    FriendStatusSerializer,
)
from friend.permissions import IsRequestedBy


class FriendModelViewSet(ModelViewSet):
    http_method_names = ['get','post','put', 'delete','options','head']
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()
    permission_classes = [IsAuthenticated,IsRequestedBy]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return FriendCreateSerialzer
        if self.request.method == 'PUT':
            return FriendStatusSerializer
        return FriendSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Friend.objects.filter(Q(requested_by=self.request.user) | Q(requested_to=self.request.user))
        return Friend.objects.filter(requested_by=self.request.user)
    
    def get_serializer_context(self):
        return {
            "requested_by":self.request.user
        }