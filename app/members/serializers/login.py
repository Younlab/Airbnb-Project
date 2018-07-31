from django.contrib.auth import get_user_model, login, authenticate
from rest_framework import serializers, request

User = get_user_model()


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )

    def validate_login(self, validated_data):
        # if not User.objects.get(username=validated_data['username']).exists():
        #     raise serializers.ValidationError("존재하지 않는 아이디 입니다.")
        # else:
        #     if not User.objects.get(password=validated_data['password']).exists():
        #         raise serializers.ValidationError("일치하지 않는 비밀번호 입니다.")
        #     else:

        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if user:
            login(request, user)
        else:
            if not User.objects.get(username=validated_data['username']).exists():
                raise serializers.ValidationError("존재하지 않는 아이디 입니다.")
            else:
                raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")