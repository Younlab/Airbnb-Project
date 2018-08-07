from rest_framework import generics
from rooms.models.rooms import RoomReservation
import django_filters
from ..serializer.room_list import RoomListSerializer, RoomDetailSerializer, RoomReservationSerializer
from ..models import Rooms


class RoomsList(generics.ListAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomListSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('rooms_tag', 'rooms_host')


class RoomsDetail(generics.RetrieveAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomDetailSerializer


class RoomReservation(generics.ListAPIView):
    queryset = RoomReservation.objects.all()
    serializer_class = RoomReservationSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('room',)

