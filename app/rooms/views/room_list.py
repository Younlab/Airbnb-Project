from django.contrib.auth import get_user_model
from rest_framework import generics, status, serializers
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


class RoomsList(generics.ListAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomListSerializer
    pagination_class = LargeResultsSetPagination


class RoomsDetail(generics.RetrieveAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomDetailSerializer


class RoomReservation(generics.ListCreateAPIView):
    queryset = RoomReservation.objects.all()
    serializer_class = RoomReservationSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('room',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def create(self, request):
    #     data = request.data
    #     serializer = RoomReservationSerializer(data=data, many=True)
    #     if request.user.is_authenticated:
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         else:
    #             raise serializers.ValidationError('올바르지 않은 형식입니다.', status.HTTP_400_BAD_REQUEST)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
