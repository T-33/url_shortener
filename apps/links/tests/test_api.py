import pytest
from rest_framework.test import APIClient
from apps.links.factories import UserFactory, LinkFactory
from apps.links.models import Link

@pytest.mark.django_db
class TestLinkApi:
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

    def test_regular_user_only_sees_his_own_links(self):
        """Test that a non-admin user can view only links created by him."""
        auth_user_link = LinkFactory(owner=self.user)
        other_user_link = LinkFactory(owner=UserFactory())

        response = self.client.get('/api/v1/links/')

        assert response.status_code == 200
        assert len(response.data) == 1

        response_ids = [item['id'] for item in response.data]
        assert other_user_link.id not in response_ids

