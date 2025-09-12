from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Link
from .serializers import LinkSerializer

User = get_user_model()

class LinkViewset(ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)

    def get_queryset(self):

        user = self.request.user

        if user.is_staff:
            return Link.objects.all()
        else:
            return Link.objects.filter(owner=user)
