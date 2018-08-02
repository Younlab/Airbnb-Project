from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.signup import UserSignupSerializer

User = get_user_model()


# 비교할 queryset은 User를 사용
# serializer는 UserSignupSerializer로 사용
class UserSignup(APIView):

    def get(self, request, format=None):
        user = User.objects.all()
        serializer = UserSignupSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

