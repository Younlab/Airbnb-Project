from django.contrib.auth import get_user_model
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.email_check import UserEmailSerializer

User = get_user_model()


class UserEmailCheck(APIView):

    def post(self, request):
        serializer = UserEmailSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise serializers.ValidationError("이 이메일 주소로 등록된 계정이 이미 존재합니다. 로그인을 시도해보세요.")
