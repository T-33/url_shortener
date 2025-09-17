import pytest
from apps.links.factories import LinkFactory


@pytest.mark.django_db
class TestLinkModels:
    def test_short_code_generation(self):
        """
        Test that custom save() method generates short_code on creation
        """
        link = LinkFactory()

        assert link.short_code is not None
        assert len(link.short_code) > 0