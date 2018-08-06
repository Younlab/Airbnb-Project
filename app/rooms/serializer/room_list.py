from rest_framework import serializers

from ..models import Rooms


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = (
            'host',
            'rooms_name',
            'tag'
        )

class RoomDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rooms
        fields = (
            'rooms_name',
            'rooms_tag',
            'rooms_host',
            'image_cover',
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

        )