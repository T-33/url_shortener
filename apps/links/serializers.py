from typing import Optional

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Link, Click
from .constants import RESERVED_WORDS
from .utils import is_valid_short_code_name

class LinkSerializer(ModelSerializer):
    """
    Serializes a Link object for API interactions.

    This serializer handles the representation of Link models, including
    the logic for creating new links with optional custom short codes.

    **Fields:**
        - 'id': unique link identifier. Readonly.
        - 'original_url': The URL to be shortened.
        - 'short_code': Short code original_url will be shortened to.
        If not provided, a random string would be assigned as the short code.
        - 'created_at': Datetime when link was created. Readonly.
        - 'owner': Link's creator's username. Readonly.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    short_code = serializers.CharField(
        max_length=15,
        required=False,
    )

    class Meta:
        model = Link
        fields = ['id', 'original_url', 'short_code', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at']

    def validate_short_code(self, value):
        """
        Check if provided short code is already taken or a reserved word.
        """
        if not value:
            return value

        if not is_valid_short_code_name(value):
            raise serializers.ValidationError('Short code must contain only alphanumerical characters and hyphen, underscore.')

        if Link.objects.filter(short_code=value).exists():
            raise serializers.ValidationError('Specified short code is already taken. Please choose another.')

        if value.lower() in RESERVED_WORDS:
            raise serializers.ValidationError('Specified short code is a reserved word and cannot be chosen. Please choose another.')

        return value

class ClickSerializer(ModelSerializer):
    """
    Serializer the Click object for analytics.

    Primarily a readonly serializer used to display data about a specific click event.
    It includes a nested representation of a Link object.
    """
    link = LinkSerializer()

    class Meta:
        model = Click
        fields = ['link', 'clicked_at', 'ip_address', 'user_agent']
