from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from ..serializers.user import UserSerializer
from ..serializers.change_password import ChangePasswordSerializer

User = get_user_model()


class ChangePassword(APIView):
    def post(self, request, uidb64):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None:
            serializer = ChangePasswordSerializer(instance=user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


