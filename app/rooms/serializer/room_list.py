from rest_framework import serializers

from members.serializers.user import UserSerializer
from ..models.rooms import RoomReservation
from ..models import Rooms


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = (
            'rooms_host',
            'rooms_name',
            'rooms_tag',
            'days_price',
            # 'image_cover_thumbnail',

        )


class RoomDetailSerializer(serializers.ModelSerializer):
    rooms_host = UserSerializer()
    class Meta:
        model = Rooms
        fields = '__all__'


class RoomReservationSerializer(serializers.ModelSerializer):
    checkin = serializers.DateField()
    checkout = serializers.DateField()

    class Meta:
        model = RoomReservation
        fields = '__all__'
