from rest_framework import serializers

from members.serializers.user import UserSerializer
from rooms.models.rooms import RoomReservation
from ..models import Rooms


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = (
            'rooms_host',
            'rooms_name',
            'rooms_tag'
        )


class RoomDetailSerializer(serializers.ModelSerializer):
    rooms_host = UserSerializer(read_only=True)
    image_cover = serializers.ImageField(required=False)
    image_cover_thumbnail = serializers.ImageField(read_only=True)
    room_rules = serializers.CharField()

    class Meta:
        model = Rooms
        fields = (
            'pk',
            'rooms_name',
            'rooms_tag',
            'rooms_host',
            'image_cover',
            'image_cover_thumbnail',
            'days_price',
            'rooms_description',
            'rooms_amount',
            'rooms_bed',
            'rooms_personnel',
            'rooms_bathroom',
            'rooms_type',
            'check_in_minimum',
            'check_in_maximum',
            'refund',
            'address_country',
            'address_city',
            'address_district',
            'address_detail',
            'address_latitude',
            'address_longitude',
            'room_facilities',
            'room_rules',
            'room_reservations',
        )


class RoomReservationSerializer(serializers.ModelSerializer):
    checkin = serializers.DateField()
    checkout = serializers.DateField()

    class Meta:
        model = RoomReservation
        fields = (
            'pk',
            'room',
            'guest',
            'checkin',
            'checkout',
        )
