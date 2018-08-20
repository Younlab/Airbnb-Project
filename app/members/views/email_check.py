from django.contrib.auth import get_user_model
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.email_check import UserEmailSerializer

__all__ = (
    'UserEmailCheck',
)

User = get_user_model()


class UserEmailCheck(APIView):

    def post(self, request):
        serializer = UserEmailSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
