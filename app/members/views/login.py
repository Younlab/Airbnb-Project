import requests
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.login import UserLoginSerializer
from ..serializers.user import UserSerializer

User = get_user_model()


class UserLogin(APIView):

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.activate is True:
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                # UserSerializer 나중에 만들어서 바꾸어 줘야함
                'user': UserSerializer(user).data,
            }
            return Response(data)
        raise serializers.ValidationError("인증되지 않은 이메일 입니다.")


class FacebookUserLogin(APIView):
    def post(self, request):
        facebook_id = request.data['id']
        username = request.data['email']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        profile_image = request.data['url']

        user, __ = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
            }
        )
        user.facebook_id = facebook_id
        user.activate = True
        user.profile_image.save(
            'profile_image.png',
            ContentFile(requests.get(profile_image).content)
        )
        user.save()

        token, __ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }

        return Response(data)
