from django.contrib.auth import get_user_model
from rest_framework import generics

from members.permissions import IsAuthenticated
from ..serializers.user import UserProfileSerializer

User = get_user_model()


class UserProfileModified(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    # permission.py IsAuthenticated로 request.user.is_authenticated 확인
    permission_classes = (IsAuthenticated,)

    # default로 pk를 가져오는 부분 customizing
    def get_object(self):
        return self.request.user
