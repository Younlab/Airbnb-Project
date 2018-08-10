from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.user import UserSerializer

User = get_user_model()


class UserList(APIView):

    def get(self, request):

        if request.user.is_superuser:
            user_list = User.objects.all()
            serializer = UserSerializer(user_list, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('볼수있는 권한이 없습니다.', status=status.HTTP_400_BAD_REQUEST)
