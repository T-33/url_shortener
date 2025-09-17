import factory
from faker import Faker
from django.contrib.auth import get_user_model
from .models import Link

fake = Faker()
User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

class LinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Link

    original_url = factory.Faker('url')
    owner = factory.SubFactory(UserFactory)
