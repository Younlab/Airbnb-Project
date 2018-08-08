from django.contrib.auth import get_user_model
from rest_framework import generics, status
import django_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from ..models.rooms import RoomReservation
from ..serializer.room_list import RoomListSerializer, RoomDetailSerializer, RoomReservationSerializer
from ..models import Rooms

User = get_user_model()


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 18
    page_size_query_param = 'page'
    max_page_size = 1000


class RoomsList(generics.ListAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomListSerializer
    pagination_class = LargeResultsSetPagination


class RoomsDetail(generics.ListAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomDetailSerializer


class RoomReservation(generics.ListCreateAPIView):
    queryset = RoomReservation.objects.all()
    serializer_class = RoomReservationSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('room',)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = RoomReservationSerializer(queryset, many=True)
        if request.user.is_authenticated:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
