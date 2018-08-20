from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

User = get_user_model()


class UserAuthSerializer(AuthTokenSerializer):

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("존재하지 않는 이메일 입니다.")

        return value

    def create(self, validated_data):
        user = User.objects.get(username=validated_data['username'])

        if user.activate is not True:
            return serializers.ValidationError("인증되지 않은 이메일 입니다.")

        return validated_data