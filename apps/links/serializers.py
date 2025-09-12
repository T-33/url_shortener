from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Link
from .utils import to_base62

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

        RESERVED_WORDS = ['api', 'admin', 'login', 'status']
        if value.lower() in RESERVED_WORDS:
            raise serializers.ValidationError('Specified short code is a reserved word and cannot be chosen. Please choose another.')

        return value

    def create(self, validated_data):
        """
        Creates s Link with specified non taken short_code or generates base62 short code from Link id.
        """
        link = Link.objects.create(**validated_data)

        user_provided_short_code = validated_data.get('short_code')

        if not user_provided_short_code:
            short_code = to_base62(link.id)
            link.short_code = short_code
            link.save(update_fields=['short_code'])

        return link