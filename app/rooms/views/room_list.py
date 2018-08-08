from rest_framework import generics
import django_filters
from ..models.rooms import RoomReservation
from ..serializer.room_list import RoomListSerializer, RoomDetailSerializer, RoomReservationSerializer
from ..models import Rooms


class RoomsList(generics.ListAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomListSerializer


class RoomsDetail(generics.ListAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomDetailSerializer

class RoomReservation(generics.ListCreateAPIView):
    queryset = RoomReservation.objects.all()
    serializer_class = RoomReservationSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('room',)