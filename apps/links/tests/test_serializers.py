import pytest
from rest_framework.exceptions import ValidationError
from apps.links.serializers import LinkSerializer
from apps.links.factories import LinkFactory
from apps.links.constants import RESERVED_WORDS
import random

@pytest.mark.django_db
class TestLinkSerializers:
    def test_duplicate_short_code_raises_error(self):
        """Tests short code duplicate validation logic."""

        LinkFactory(short_code='already-taken')

        new_link_data = {
            'original_url': 'https://somesite.com/',
            'short_code': 'already-taken',
        }

        serializer = LinkSerializer(data=new_link_data)

        with pytest.raises(ValidationError, match='is already taken'):
            serializer.is_valid(raise_exception=True)

    def test_invalid_short_code_name_raises_error(self):
        """Tests short invalid name validation logic."""

        new_link_data = {
            'original_url': 'https://somesite.com/',
            'short_code': 'invalid+?code',
        }

        serializer = LinkSerializer(data=new_link_data)

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_reserved_short_code_raises_error(self):
        """
        Tests short code reserved words list validation logic.
        """
        new_link_data = {
            'original_url': 'https://somesite.com/',
            'short_code': random.choice(RESERVED_WORDS),
        }

        serializer = LinkSerializer(data=new_link_data)

        with pytest.raises(ValidationError, match='reserved word'):
            serializer.is_valid(raise_exception=True)
