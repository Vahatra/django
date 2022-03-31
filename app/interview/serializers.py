from rest_framework import serializers

from .models import Interview


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ("uuid",)
        read_only_fields = ("uuid",)
