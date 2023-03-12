from rest_framework.routers import DefaultRouter

from social_post.apis import PostModelViewSet
router = DefaultRouter()
router.register("posts", PostModelViewSet)

urlpatterns = router.urls