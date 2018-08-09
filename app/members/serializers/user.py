from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'profile_image',
            'phone_number',
            'birthday',
            'is_host',
            'likes_posts',
        )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'profile_image',
            'phone_number',
            'birthday',
            'username',
            'is_host',
        )
