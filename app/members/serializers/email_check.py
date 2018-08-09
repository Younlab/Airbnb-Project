from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserEmailSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(max_length=200)

    class Meta:
        model = User
        fields = (
            'username',
        )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이 이메일 주소로 등록된 계정이 이미 존재합니다. 로그인을 시도해보세요.")
        return value