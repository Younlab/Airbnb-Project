from django.conf import settings
from rest_framework import serializers

from members.serializers.user import UserSerializer
from ..models.rooms import RoomReservation, RoomFacilities, RoomRules
from ..models import Rooms


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = (
            'rooms_host',
            'rooms_name',
            'rooms_tag',
            'days_price',
            'image_cover_thumbnail',

        )


class RoomReservationSerializer(serializers.ModelSerializer):
    guest = settings.AUTH_USER_MODEL
    checkin = serializers.DateField()
    checkout = serializers.DateField()

    class Meta:
        model = RoomReservation
        fields = (
            'room',
            'guest',
            'checkin',
            'checkout',
            'created_at',
        )


class RoomFacilitieSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomFacilities
        fields = (
            'facilities',
        )


class RoomRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomRules
        fields = (
            'rule_list',
        )


class RoomDetailSerializer(serializers.ModelSerializer):
    rooms_host = UserSerializer()
    room_facilities = RoomFacilitieSerializer(many=True)
    room_reservations = RoomReservationSerializer(many=True)
    room_rules = RoomRuleSerializer(many=True)

    class Meta:
        model = Rooms
        fields = (
            'rooms_name',
            'rooms_tag',
            'rooms_host',
            'rooms_type',
            'image_cover',
            'rooms_amount',
            'rooms_bed',
            'rooms_personnel',
            'rooms_bathroom',
            'days_price',
            'room_rules',
            'room_facilities',
            'rooms_description',
            'check_in_minimum',
            'check_in_maximum',
            'room_reservations',
            'refund',
            'address_country',
            'address_city',
            'address_district',
            'address_detail',
            'address_latitude',
            'address_longitude',
            'created_at',
            'modified_date',

        )
