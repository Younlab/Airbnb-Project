import requests
import json

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializers.user import UserSerializer

User = get_user_model()


class KakaoAuth(APIView):

    def get(self, request):
        code = request.GET.get('code')
        user = authenticate(request, code=code)

        token, __ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }

        return Response(data)
