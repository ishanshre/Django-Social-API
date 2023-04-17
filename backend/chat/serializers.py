from chat.models import Chat

from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()



class ChatSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Chat
        fields = [
            'id',
            'group',
            'from_user',
            'to_user',
            'read',
            'created_at',
            'updated_at',
        ]