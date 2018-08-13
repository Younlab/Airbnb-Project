from django.contrib.auth import get_user_model
from rest_framework import generics, status, serializers, permissions
import django_filters
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin
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


class RoomsList(generics.ListAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomListSerializer
    pagination_class = LargeResultsSetPagination


class RoomsDetail(generics.RetrieveAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomDetailSerializer


class RoomReservation(generics.ListCreateAPIView):
    queryset = RoomReservation.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = RoomReservationSerializer

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)

