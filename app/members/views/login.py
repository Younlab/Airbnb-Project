from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.login import UserLoginSerializer

User = get_user_model()


class UserLogin(APIView):

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            # UserSerializer 나중에 만들어서 바꾸어 줘야함
            'user': UserLoginSerializer(user).data,
        }
        return Response(data)
