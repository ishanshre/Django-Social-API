from rest_framework import serializers

from social_post.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','content','avatar','caption','created_by','created_at','updated_at']
    
    