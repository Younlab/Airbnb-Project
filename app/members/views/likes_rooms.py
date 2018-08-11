from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rooms.serializer.room_list import RoomListSerializer

User = get_user_model()


class UserLikesRooms(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            likes_posts = user.likes_posts.all()
            serializer = RoomListSerializer(likes_posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)