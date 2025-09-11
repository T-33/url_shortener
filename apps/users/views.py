from rest_framework.viewsets import ModelViewSet

from django.contrib.auth import get_user_model
from rest_framework import permissions

from .serializer import UserSerializer

User = get_user_model()

class UserViewset(ModelViewSet):
    """
    A viewset for viewing and editing User instances.
    - Admins can see all users.
    - Regular users can see themselves only .
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        This view should return a list of all users for admins
        and current user for non-staff members.
        """
        user = self.request.user

        if user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(pk=user.pk)

    def get_permissions(self):
        """Instantiates and returns a list of permissions this view requires"""
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]
