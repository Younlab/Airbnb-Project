from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=200, write_only=True)
    check_password = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = User
        fields = (
            'new_password',
            'check_password',
        )

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('check_password'):
            raise serializers.ValidationError("비밀번호와 비밀번호 확인이 같지 않습니다.")
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new_password'))
        instance.save()
        return instance