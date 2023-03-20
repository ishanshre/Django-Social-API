from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from social_post.models import Post
from social_post.serializers import PostSerializer, PostCreateSerializer, PostListSerializer
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
