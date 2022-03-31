# import os
# import profile

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

# from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import Profile, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "uuid",
            "address_1",
            "address_1",
            "zip_code",
            "city",
            "state",
            "country",
        )
        read_only_fields = ("uuid",)

    def create(self, validated_data):
        user = self.context.get("user", None)
        if not user:
            raise ValidationError("unspecified user", code="progamming_error")
        instance: User = User.objects.create_user(user=user, **validated_data)

        return instance


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "uuid",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            # "avatar",
            "created",
            "last_login",
            "is_active",
            "profile",
        )
        read_only_fields = (
            "uuid",
            "is_active",
            "created",
            "last_login",
            "profile",
        )
        # extra_kwargs = {"avatar": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data.pop("username", None)
        password = validated_data.pop("password", None)
        try:
            validate_password(password)
        except DjangoValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )
        instance: User = User.objects.create_user(
            username=username, password=password, **validated_data
        )

        return instance

    def validate(self, attrs):
        password = attrs.get("password", None)
        if password and self.instance:
            password = attrs.pop("password")
            try:
                validate_password(password)
            except DjangoValidationError as e:
                serializer_error = serializers.as_serializer_error(e)
                raise serializers.ValidationError(
                    {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
                )
            self.instance.set_password(password)

        return attrs

    # def to_representation(self, instance: User):
    #     data = super().to_representation(instance)
    #     if instance.avatar.name:
    #         relpath = os.path.relpath(instance.avatar.path, settings.MEDIA_ROOT)
    #         data["avatar_url"] = os.path.join(settings.MEDIA_URL, relpath)

    #     return data


class SendEmailResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def get_user(self, is_active=True):
        try:
            user = User.objects.get(
                is_active=is_active,
                email=self.data.get("email", ""),
            )
            if user.has_usable_password():
                return user
        except User.DoesNotExist:
            raise ValidationError("email not found", code="email_not_found")


class UidAndTokenSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        # uuid validation have to be here, because validate_<field_name>
        # doesn't work with modelserializer
        try:
            self.user = User.objects.get(pk=self.initial_data.get("uuid", ""))
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise ValidationError("invalid uuid")

        is_token_valid = default_token_generator.check_token(
            self.user, self.initial_data.get("token", "")
        )
        if is_token_valid:
            return validated_data
        else:
            raise ValidationError("invalid token")


class NewPasswordSerializer(UidAndTokenSerializer, serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        user = self.context["request"].user or self.user

        try:
            validate_password(attrs["new_password"], user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return super().validate(attrs)
