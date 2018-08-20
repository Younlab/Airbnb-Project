from rest_framework import generics, permissions, status
from rest_framework.response import Response

from ..models.rooms import RoomReservation
from ..serializer.room_list import RoomReservationSerializer


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

    def post(self, request, room_pk):
        request.data['room'] = room_pk
        return self.create(request)

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
