from rest_framework.routers import DefaultRouter, SimpleRouter

from django.conf import settings

from .views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
urlpatterns = router.urls
