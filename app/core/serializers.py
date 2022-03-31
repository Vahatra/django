from rest_framework import serializers


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "uuid",
            "label",
            "codename",
        )
        read_only_fields = ("uuid", "codename")
        abstract = True
