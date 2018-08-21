from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, filters
import django_filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .pagination import Pagination
from ..serializer.room_list import RoomListSerializer, RoomDetailSerializer, RoomCreateSerializer
from ..models import Rooms

User = get_user_model()

__all__ = (
    'RoomsCreate',
    'RoomsList',
    'RoomsDetail',

)


class RoomsCreate(generics.CreateAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomCreateSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


class RoomsFilter(django_filters.FilterSet):
    address_city = django_filters.CharFilter(field_name='address_city', lookup_expr='contains')
    rooms_personnel = django_filters.NumberFilter(field_name='rooms_personnel', lookup_expr='exact')

    class Meta:
        model = Rooms
        fields = ['address_city', 'rooms_personnel',]


class RoomsList(generics.ListAPIView):
    """
    전체 숙소 리스트 API
    """
    queryset = Rooms.objects.all()
    serializer_class = RoomListSerializer
    pagination_class = Pagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter)
    # filter_fields = ('address_city',)
    filter_class = RoomsFilter
    search_fields = ('address_country', 'address_city', 'address_district', 'address_detail', 'rooms_name')


class RoomsDetail(APIView):
    """
    숙소 상세페이지 API
    """

    def get(self, request, room_pk, format=None):
        room = Rooms.objects.filter(pk=room_pk)
        serializer = RoomDetailSerializer(room, many=True)
        return Response(serializer.data)
