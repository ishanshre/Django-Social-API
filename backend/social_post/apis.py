from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from social_post.models import Post, Comment, Like
from social_post.serializers import (
    PostSerializer,
    PostCreateSerializer,
    PostListSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    LikeSerializer,
)
from social_post.permissions import IsOwnerOrReadOnly


class PostModelViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostCreateSerializer
        return PostSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}
    
    def list(self, request, *args, **kwargs):
        serializer = PostListSerializer(self.queryset, many=True)
        return Response(serializer.data)


class CommentModelViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(active=True)
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(post__id=self.kwargs['post_pk'])
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentCreateSerializer
        return CommentSerializer
    
    def get_serializer_context(self):
        post = Post.objects.get(id=self.kwargs['post_pk'])
        return {
            "user": self.request.user,
            "post":post
        }

class LikeModelViewSet(ModelViewSet):
    http_method_names = ['get','post','delete','options','heads']
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(post__id=self.kwargs['post_pk'])

    def get_serializer_context(self):
        post = Post.objects.get(id=self.kwargs['post_pk'])
        return {
            'user':self.request.user,
            'post':post
        }