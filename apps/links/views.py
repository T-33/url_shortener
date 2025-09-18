from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Link, Click
from .serializers import LinkSerializer, ClickSerializer

User = get_user_model()

def link_redirect_view(request, short_code: str):

    link = get_object_or_404(Link, short_code=short_code)

    Click.objects.create(
        link=link,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )

    return redirect(link.original_url)

class LinkViewset(ModelViewSet):
    """
    API endpoint  that allows links to be viewed and edited.
        - Authenticated users can create links.
        - Users can only view and edit their own links.
        - Staff users can view and edit all links.
    """
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Associate the link with the currently authenticated user."""
        user = self.request.user
        serializer.save(owner=user)

    def get_queryset(self):
        """
        Dynamically filter the queryset based on the user.
        """
        user = self.request.user
        return Link.objects.for_user(user)

class ClickViewset(ModelViewSet):
    """
    API endpoint that allow clicks to be viewed and edited.
        - Only admins can interact with clicks.
    """
    queryset = Click.objects.all()
    serializer_class = ClickSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]