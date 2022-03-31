from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .access_policy import InterviewAccessPolicy
from .models import Interview
from .serializers import InterviewSerializer


class InterviewViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewSerializer
    queryset = Interview.objects.all()
    permission_classes = [InterviewAccessPolicy]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["uuid"]

    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        return self.access_policy.scope_queryset(self.request, Interview.objects.all())
