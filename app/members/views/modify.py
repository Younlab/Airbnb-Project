from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.user import UserProfileSerializer

User = get_user_model()


class UserProfileModefied(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('인증되지 않은 유저입니다.', status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            serializer = UserProfileSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('인증되지 않은 유저입니다.', status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            user.delete()
            return Response('삭제되었습니다.', status=status.HTTP_204_NO_CONTENT)
        return Response('인증되지 않은 유저입니다.', status=status.HTTP_400_BAD_REQUEST)