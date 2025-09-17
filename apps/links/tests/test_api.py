import pytest
from rest_framework.test import APIClient
from apps.links.factories import UserFactory, LinkFactory
from apps.links.models import Link

@pytest.mark.django_db
class TestLinkSerializers:
    def setup_method(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_short_code_provided_create_link_succeeds(self):
        """Tests happy path with authenticated user and provided not taken short code"""
        payload = {
            'original_url': 'https://somelink.com/',
            'short_code': 'shortlink'
        }

        response = self.client.post('/api/v1/links/', payload)

        assert response.status_code == 201
        assert Link.objects.count() == 1
        created_link = Link.objects.first()
        assert created_link.owner == self.user
        assert created_link.original_url == payload['original_url']
        assert created_link.short_code == payload['short_code']

    def test_no_provided_short_code_create_link_succeeds(self):
        """Test creating a link as authenticated user when short code is not provided short_code"""
        payload = {
            'original_url': 'https://somelink.com/'
        }

        response = self.client.post('/api/v1/links/', payload)

        assert response.status_code == 201
        assert Link.objects.count() == 1
        created_link = Link.objects.first()
        assert created_link.owner == self.user
        assert created_link.original_url == payload['original_url']