from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):
    """
    Handles User model serialization and deserialization.
    - Hashes password
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        write_only_fields = ['password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)

        return user