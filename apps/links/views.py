from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Link, Click
from .serializers import LinkSerializer

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

class ClickViewset(ModelViewSet):
    queryset = Click.objects.all()
    permission_classes = [IsAuthenticated]