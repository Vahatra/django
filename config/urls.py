from django.conf import settings
from django.contrib import admin
from django.urls import include, path

API_PREFIX = "api/v0"

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),
]

# API URLS
api_urlpatterns = [
    # JWT
    path(f"{API_PREFIX}/", include("djoser.urls.jwt")),
    # Social auth
    path(f"{API_PREFIX}/", include("djoser.social.urls")),
    # User management
    path(f"{API_PREFIX}/", include("djoser.urls")),
]

urlpatterns += api_urlpatterns

if settings.DEBUG:
    from rest_framework import permissions

    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view

    api_schema_view = get_schema_view(
        openapi.Info(title="API", description="API", default_version="v0"),
        public=True,
        permission_classes=(permissions.AllowAny,),
        patterns=api_urlpatterns,
    )

    swagger_urlpatterns = [
        path(
            r"swagger/",
            api_schema_view.with_ui("swagger", cache_timeout=0),
            name="swagger",
        ),
        path(
            r"redoc/", api_schema_view.with_ui("redoc", cache_timeout=0), name="redoc",
        ),
    ]

    urlpatterns += swagger_urlpatterns
