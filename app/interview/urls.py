from rest_framework.routers import DefaultRouter, SimpleRouter

from django.conf import settings

from .views import InterviewViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router = DefaultRouter()
router.register(r"interview", InterviewViewSet, basename="Interview")
urlpatterns = router.urls
