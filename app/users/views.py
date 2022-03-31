from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from ..utils.tasks import send_email_task
from .access_policy import UserAccessPolicy
from .serializers import (
    NewPasswordSerializer,
    ProfileSerializer,
    SendEmailResetSerializer,
    UserSerializer,
)

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserFilter(filters.FilterSet):
    address_1 = filters.CharFilter(
        field_name="profile__address_1",
        lookup_expr="contains",
    )
    address_2 = filters.CharFilter(
        field_name="profile__address_2",
        lookup_expr="contains",
    )
    zip_code = filters.CharFilter(
        field_name="profile__zip_code",
        lookup_expr="exact",
    )
    city = filters.CharFilter(
        field_name="profile__city",
        lookup_expr="exact",
    )
    state = filters.CharFilter(
        field_name="profile__state",
        lookup_expr="exact",
    )
    country = filters.CharFilter(
        field_name="profile__country",
        lookup_expr="exact",
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserAccessPolicy]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        qs = User.objects.select_related("profile")
        return self.access_policy.scope_queryset(self.request, qs)

    def get_instance(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action == "reset_password":
            return SendEmailResetSerializer
        elif self.action == "reset_password_confirm":
            return NewPasswordSerializer
        else:
            return self.serializer_class

    # disable
    def destroy(self, request, *args, **kwargs):
        instance: User = self.get_object()
        instance.is_active = False
        instance.save(update_fields=["is_active"])

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

    @action(["post"], detail=True)
    def activate(self, request, *args, **kwargs):
        instance: User = self.get_object()
        instance.is_active = True
        instance.save(update_fields=["is_active"])

        return Response(status=status.HTTP_200_OK)

    @action(["post"], detail=True)
    def deactivate(self, request, *args, **kwargs):
        instance: User = self.get_object()
        instance.is_active = False
        instance.save(update_fields=["is_active"])

        return Response(status=status.HTTP_200_OK)

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            uuid = str(user.pk)
            token = default_token_generator.make_token(user)
            url = f"{settings.APP_FRONTEND_URL}/reset_password_confirm/{uuid}/{token}"
            send_email_task(
                subject="password reset",
                message=url,
                recipient_list=[user.email],
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.user.set_password(serializer.data["new_password"])
        serializer.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        description="Add a profile to a user",
        request=ProfileSerializer,
        methods=["POST"],
        responses={201: ProfileSerializer},
    )
    @extend_schema(
        description="Modify a user's profile",
        request=ProfileSerializer,
        methods=["PATCH", "PUT"],
        responses={200: ProfileSerializer},
    )
    @extend_schema(
        description="Delete a user's profile",
        request=None,
        methods=["DELETE"],
        responses={204: None},
    )
    @action(["post", "patch", "put", "delete"], detail=True)
    def profile(self, request, *args, **kwargs):
        user: User = self.get_object()
        if request.method == "POST":
            serializer = ProfileSerializer(
                data=request.data,
                context={"user": user},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "PATCH" or request.method == "PUT":
            serializer = ProfileSerializer(
                instance=user.profile,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        # if "DELETE"
        user.profile.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
