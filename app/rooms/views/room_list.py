from django.contrib.auth import get_user_model
from rest_framework import generics
import django_filters
from ..models.rooms import RoomReservation
from ..serializer.room_list import RoomListSerializer, RoomDetailSerializer, RoomReservationSerializer
from ..models import Rooms

User = get_user_model()


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

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        login 한 유저만 예약신청을 할수 있도록,
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if request.user.is_authenticated:
            return self.create(request, *args, **kwargs)
