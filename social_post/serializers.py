from rest_framework import serializers

from social_post.models import Post

from accounts.serializers import UserInfoSerializer



class PostListSerializer(serializers.ModelSerializer):
    created_by = UserInfoSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id','title','preview_pic', 'created_by']

        
class PostSerializer(serializers.ModelSerializer):
    created_by = UserInfoSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id','title','content','preview_pic','caption','created_by','created_at','updated_at']
    

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title','content','preview_pic','caption']
    
    def create(self, validated_data):
        user= self.context['user']
        post = Post.objects.create(**validated_data, created_by=user)
        post.save()
        return post