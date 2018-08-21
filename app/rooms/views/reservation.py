from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import RoomReservation
from ..serializer.room_list import RoomReservationSerializer

__all__ = (
    'RoomReservationAPI',
)


class RoomReservationAPI(generics.ListCreateAPIView):
    """
    예약 API
    """
    serializer_class = RoomReservationSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get(self, request, room_pk):
        room = RoomReservation.objects.filter(room=room_pk)
        serializer = RoomReservationSerializer(room, many=True)
        return Response(serializer.data)
    #
    # def perform_create(self, serializer):
    #     serializer.create()

