from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.change_password_email_check import ChangePasswordEmailCheckSerializer

__all__ = (
    'ChangePasswordCheckEmail',
)

User = get_user_model()


class ChangePasswordCheckEmail(APIView):
    def post(self, request):
        serializer = ChangePasswordEmailCheckSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response('발송완료', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
