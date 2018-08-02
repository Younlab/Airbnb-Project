from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    # serializer에는 password_check가 없기에 비교해줄 필드를 임의로 만듬
    password_check = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'password_check',
        )

    # db에 유저가 존재할경우 에러발생
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 있는 아이디 입니다. 다른 아이디를 입력하세요")
        return value

    # password의 길이가 8글자 아래일 경우 에러발생
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 8글자 이상이여야 합니다.")
        return value

    # 위의 validated의 값이 다 통과되고 password와 password_check의 값이 같으면
    # create_user로 user값 생성
    # create로 만들경우 해싱된 값이 아닌 user가 쓴 값이 그대로 들어감
    def create(self, validated_data):
        if validated_data['password'] != validated_data['password_check']:
            raise serializers.ValidationError("비밀번호와 비밀번호 확인이 같지 않습니다.")
        else:
            user = User.objects.create_user(
                username=self.validated_data['username'],
                email=self.validated_data['email'],
                password=self.validated_data['password']
            )
            user.save()

        return validated_data
