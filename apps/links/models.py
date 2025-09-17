from django.db import models
from django.contrib.auth import get_user_model

from .utils import generate_random_short_code
from .constants import SHORT_CODE_LENGTH
User = get_user_model()

class Link(models.Model):
    """
    Represents a single shortened link.
    """
    original_url = models.URLField()
    short_code = models.CharField(max_length=15, unique=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')

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