from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """

    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    following = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "identity",
            "name",
            "email",
            "password",
            "profile_image",
            "bio",
            "followers",
            "following",
            "birth_date",
            "gender",
            "phone",
            "address",
            "our_books",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "followers": {"read_only": True},
            "following": {"read_only": True},
            "our_books": {"read_only": True},
        }

    def create(self, validated_data):
        """
        Encrypt password.
        """
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
