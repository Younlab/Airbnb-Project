from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
import django_filters
from rest_framework.pagination import PageNumberPagination

from ..models.rooms import RoomReservation
from ..serializer.room_list import RoomListSerializer, RoomDetailSerializer, RoomReservationSerializer
from ..models import Rooms

User = get_user_model()


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 18
    page_query_param = 'page'


class RoomsList(generics.ListAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomListSerializer
    pagination_class = LargeResultsSetPagination


class RoomsDetail(generics.RetrieveAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomDetailSerializer


class RoomReservation(generics.ListCreateAPIView):
    queryset = RoomReservation.objects.all()

    # 필터링, 해당 room 에대한 예약 출력, ex -> "?room=1"
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('room',)

    # login 인증을 통과하지 못하면 "인증오류" 발생
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = RoomReservationSerializer

    # login 한 유저만 예약 할 수 있도록 처리
    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)
