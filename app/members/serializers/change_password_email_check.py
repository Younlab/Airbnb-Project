from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers

User = get_user_model()


class ChangePasswordEmailCheckSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200, write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
        )

    def validate_email(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("존재하지 않는 이메일 입니다.")
        return value

    def create(self, validated_data):
        user = User.objects.get(username=validated_data['email'])

        message = render_to_string('change_password_check_email.html', {
            'user': user,
            'domain': 'leesoo.kr',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8')
        })

        mail_subject = 'Email_check'
        to_email = validated_data['email']
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return validated_data
