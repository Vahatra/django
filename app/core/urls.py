from dynamic_preferences.api.viewsets import GlobalPreferencesViewSet
from dynamic_preferences.users.viewsets import UserPreferencesViewSet
from rest_framework import routers

from django.conf.urls import include
from django.urls import path

router = routers.SimpleRouter()
router.register(r"global", GlobalPreferencesViewSet, basename="GlobalPreferences")
router.register(r"user", UserPreferencesViewSet, basename="UserPreferences")
urlpatterns = [path("preferences/", include(router.urls))]
