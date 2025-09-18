from django.db import models
from django.contrib.auth import get_user_model

from .utils import generate_random_short_code
from .constants import SHORT_CODE_LENGTH
User = get_user_model()

class LinkManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('owner')

    def for_user(self, user):
        """
        Returns a queryset of links for a given user.
            - Admin users can see all links.
            - Regular users can see only their own links.
        """
        if user.is_staff:
            return self.all()

        return self.filter(owner=user)

class Link(models.Model):
    """
    Represents a single shortened link.
    """
    original_url = models.URLField()
    short_code = models.CharField(max_length=15, unique=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')

    objects = LinkManager()

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_random_short_code(length=SHORT_CODE_LENGTH)
            while Link.objects.filter(short_code=self.short_code).exists():
                self.short_code = generate_random_short_code(SHORT_CODE_LENGTH)

        super().save(*args, **kwargs)

class Click(models.Model):
    """
    Represents a single Click event for a Link
    """
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='clicks')
    clicked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    referer = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'Click on {self.link.short_code} at {self.clicked_at}'