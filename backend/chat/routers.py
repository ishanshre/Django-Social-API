from rest_framework.routers import DefaultRouter

from chat import apis


router = DefaultRouter()

router.register("chats",apis.ChatModelViewSet, basename="chat")

urlpatterns = router.urls