from rest_framework import serializers

from social_post.models import Post, Comment, Like

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


class CommentCreateSerializer(serializers.ModelSerializer):
    created_by = UserInfoSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['body','created_by','created_at','updated_at']
    
    def create(self, validated_date):
        user = self.context['user']
        post = self.context['post']
        comment = Comment.objects.create(**validated_date, created_by=user, post=post)
        comment.save()
        return comment

class CommentSerializer(serializers.ModelSerializer):
    created_by = UserInfoSerializer(read_only=True)
    class Meta: 
        model = Comment
        fields = ['id', 'body','created_by', 'created_at', 'updated_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id']
    
    def validate(self, attrs):
        user = self.context['user']
        post = self.context['post']
        if Like.objects.filter(created_by=user, post=post).exists():
            raise serializers.ValidationError({"error":"cannot like same post by same user more than one time"})
        return super().validate(attrs)

    def create(self, validated_data):
        user = self.context['user']
        post = self.context['post']
        like = Like.objects.create(created_by=user, post=post)
        like.save()
        return like