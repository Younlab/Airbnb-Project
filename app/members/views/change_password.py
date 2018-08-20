from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from ..serializers.user import UserSerializer
from ..serializers.change_password import ChangePasswordSerializer

__all__ = (
    'ChangePassword',
)

User = get_user_model()


class ChangePassword(APIView):
    def post(self, request, uidb64):
        try:
            # url에서의 uid를 받아 디코딩하여 값을 받아온다.
            uid = force_text(urlsafe_base64_decode(uidb64))
            # 디코딩된 uid를 이용하여 user를 불러온다
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        # serializer에 instance랑 data를 보내서 기존의 password값에서 새로운 password값으로
        # 변경하게끔 만듬
        if user is not None:
            serializer = ChangePasswordSerializer(instance=user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


