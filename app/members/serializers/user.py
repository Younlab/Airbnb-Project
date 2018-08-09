from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'profile_image',
            'phone_number',
            'birthday',
            'is_host',
            'create_date',
            'likes_posts',
        )


class UserProfileSerializer(serializers.ModelSerializer):

    # first_name = serializers.CharField(max_length=50, allow_blank=True)

    class Meta:
        model = User
        fields = (
            'profile_image',
            'phone_number',
            'birthday',
            'first_name',
            'last_name',
            'is_host',
        )
