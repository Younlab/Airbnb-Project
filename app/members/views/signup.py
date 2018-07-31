from django.contrib.auth import get_user_model
from rest_framework import generics

from ..serializers.signup import UserSignupSerializer

User = get_user_model()


# 비교할 queryset은 User를 사용
# serializer는 UserSignupSerializer로 사용
class UserSignup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
