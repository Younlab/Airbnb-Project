from rest_framework import generics
from rest_framework.response import Response

from ..models import Rooms
from ..serializer.room_list import RoomListSerializer


class MainPageRoomsList(generics.ListAPIView):
    serializer_class = RoomListSerializer

    def list(self, request):
        limit_num = 4
        address_response = {}
        address_list = ['서울', '인천', '대구', '부산']
        for i in address_list:
            address_response[i] = RoomListSerializer(Rooms.objects.filter(address_city__contains=i)[:limit_num],
                                                     many=True).data
            # aws
            address_response[i].append({'link': f'https://leesoo.kr/rooms/list?address_city={i}'})
        return Response(address_response)
