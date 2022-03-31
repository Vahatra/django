from rest_framework import status
from rest_framework.response import Response

from django.db.models import ProtectedError


class DestroyProtectedMixin:
    """
    Mixin for handling ProtectedError exceptions.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError as e:
            return Response(
                {"protected": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
