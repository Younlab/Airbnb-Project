from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
import django_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.rooms import RoomReservation
from ..serializer.room_list import RoomListSerializer, RoomDetailSerializer, RoomReservationSerializer
from ..models import Rooms

User = get_user_model()


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 18
    page_query_param = 'page'


class RoomReservationAPI(generics.ListCreateAPIView):
    serializer_class = RoomReservationSerializer
    queryset = RoomReservation.objects.all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get(self, request, room_pk):
        room = RoomReservation.objects.filter(room=room_pk)
        serializer = RoomReservationSerializer(room, many=True)
        return Response(serializer.data)

    def post(self, request, room_pk):
        request.data['room'] = room_pk
        return self.create(request)

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomsList(generics.ListAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomListSerializer
    pagination_class = LargeResultsSetPagination


# class RoomsDetail(generics.RetrieveAPIView):
#     queryset = Rooms.objects.all()
#     serializer_class = RoomDetailSerializer

class RoomsDetail(APIView):
    def get(self, request, room_pk, format=None):
        room = Rooms.objects.filter(pk=room_pk)
        serializer = RoomDetailSerializer(room, many=True)
        return Response(serializer.data)

# class RoomReservation(generics.CreateAPIView, generics.RetrieveAPIView):
#     queryset = RoomReservation.objects.all()

# 필터링, 해당 room 에대한 예약 출력, ex -> "?room=1"
# filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
# filter_fields = ('room',)

# login 인증을 통과하지 못하면 "인증오류" 발생
# permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
# serializer_class = RoomReservationSerializer

# login 한 유저만 예약 할 수 있도록 처리
# def perform_create(self, serializer):
#     serializer.save(guest=self.request.user)
