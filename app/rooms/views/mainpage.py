from rest_framework import generics
from rest_framework.response import Response

from ..models import Rooms
from ..serializer.room_list import RoomListSerializer

__all__ = (
    'MainPageRoomsList',
)


class MainPageRoomsList(generics.ListAPIView):
    serializer_class = RoomListSerializer

    def list(self, request):
        limit_num = 4
        address_response = {}
        # city_list = ['서울특별시', '부산광역시', '대구광역시', '인천광역시',
        #              '광주광역시', '대전광역시', '울산광역시', '세종특별자치시',
        #              '경기도', '강원도']
        address_list = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기도', '강원도']
        # address_list = ['부산']
        for i in address_list:
            address_response[i] = RoomListSerializer(Rooms.objects.filter(address_city__contains=i)[:limit_num],
                                                     many=True).data
            # aws
            address_response[i].append({'link': f'https://leesoo.kr/rooms/list?address_city={i}'})
        return Response(address_response)
