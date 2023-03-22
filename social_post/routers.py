# from rest_framework.routers import DefaultRouter

# from social_post.apis import PostModelViewSet
# router = DefaultRouter()
# router.register("posts", PostModelViewSet, basename='posts')

# urlpatterns = router.urls

from rest_framework_nested import routers

from social_post import apis

router = routers.DefaultRouter()
router.register("posts", apis.PostModelViewSet, basename='posts')
posts_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
posts_router.register("comments", apis.CommentModelViewSet, basename="post-comments")
posts_router.register("likes", apis.LikeModelViewSet, basename="post-likes")
urlpatterns = router.urls + posts_router.urls