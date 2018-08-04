from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class UserLogout(APIView):

    def post(self, request, format=None):
        if request.user.is_authenticated:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response("로그아웃 되었습니다.", status=status.HTTP_204_NO_CONTENT)
        raise AuthenticationFailed("로그인이 되지 않은 사용자 입니다.")
