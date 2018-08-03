from rest_framework import generics

from ..serializer.room_list import RoomListSerializer
from ..models import Rooms


class RoomsList(generics.ListAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomListSerializer
