from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.user import UserSerializer
from ..serializers.change_password import ChangePasswordSerializer

User = get_user_model()


class ChangePassword(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            serializer = ChangePasswordSerializer(instance=user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("로그인이 필요한 활동입니다.", status=status.HTTP_400_BAD_REQUEST)
