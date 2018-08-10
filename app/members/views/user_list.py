from django.contrib.auth import get_user_model
from rest_framework import generics

from ..permissions import AdminUserReadOnly
from ..serializers.user import UserSerializer

User = get_user_model()


class UserList(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminUserReadOnly,)
