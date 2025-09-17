from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Link
from .constants import RESERVED_WORDS

class LinkSerializer(ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    short_code = serializers.CharField(
        max_length=15,
        required=False,
    )

    class Meta:
        model = Link
        fields = ['original_url', 'short_code', 'created_at', 'owner']
        read_only_fields = ['created_at']

    def validate_short_code(self, value):
        """
        Check if provided short code is already taken or a reserved word.
        """
        if not value:
            return value

        if Link.objects.filter(short_code=value).exists():
            raise serializers.ValidationError('Specified short code is already taken. Please choose another.')

        if value.lower() in RESERVED_WORDS:
            raise serializers.ValidationError('Specified short code is a reserved word and cannot be chosen. Please choose another.')

        return value