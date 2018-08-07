from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Rooms

User = get_user_model()


class RoomsLikes(APIView):

    def post(self, request, pk):
        if request.user.is_authenticated:
            user = User.objects.get(user=request.user)
            room = Rooms.objects.get(pk=pk)

            if not user.likes_posts.filter(pk=room.pk).exists():

                user.likes_posts.add(room)

                return Response('퐐로우', status=status.HTTP_200_OK)

            else:
                user.likes_posts.remove(room)

                return Response('언퐐로우', status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
