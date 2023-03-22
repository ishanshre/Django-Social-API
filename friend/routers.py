from rest_framework.routers import DefaultRouter

from friend import apis

router = DefaultRouter()
router.register("friends", apis.FriendModelViewSet)

urlpatterns = router.urls