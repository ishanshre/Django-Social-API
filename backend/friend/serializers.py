from rest_framework import serializers

from friend.models import Friend

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = "__all__"

class FriendCreateSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['id','requested_to']
    
    def validate(self, attrs):
        requested_to = attrs.get('requested_to', '')
        requested_by = self.context['requested_by']
        if Friend.objects.filter(requested_to=requested_to, requested_by=requested_by).exists() or Friend.objects.filter(requested_to=requested_by, requested_by=requested_to).exists():
            raise serializers.ValidationError({"error":"already a friend or request sent"})
        return super().validate(attrs)
    
    def create(self, validated_data):
        requested_by = self.context['requested_by']
        requested_to = validated_data['requested_to']
        friend = Friend.objects.create(requested_by=requested_by, requested_to=requested_to)
        friend.save()
        return friend


class FriendStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['id','status']