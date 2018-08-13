from django.conf import settings
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from members.serializers.user import UserSerializer
from ..models.rooms import RoomReservation, RoomFacilities, RoomRules, RoomImage
from ..models import Rooms


class RoomImageThumbnailSerializer(serializers.ModelSerializer):
    room_image_thumbnail = serializers.ImageField()

    class Meta:
        model = RoomImage
        fields = (
            'room_image_thumbnail',
        )


class RoomImageSerializer(serializers.ModelSerializer):
    room_image = serializers.ImageField()

    class Meta:
        model = RoomImage
        fields = (
            'room_image',
        )


class RoomListSerializer(serializers.ModelSerializer):
    room_images = RoomImageThumbnailSerializer(many=True)

    class Meta:
        model = Rooms
        fields = (
            'rooms_host',
            'rooms_name',
            'rooms_tag',
            'days_price',
            'room_images',

        )


class RoomReservationSerializer(serializers.ModelSerializer):
    room = Rooms.objects.all()
    guest = settings.AUTH_USER_MODEL
    checkin = serializers.DateField()
    checkout = serializers.DateField()



    class Meta:
        model = RoomReservation
        fields = (
            'room',
            'guest',
            'guest_personnel',
            'checkin',
            'checkout',
            'created_at',
        )

    def validate(self, value):
        if self.initial_data.get('room'):
            room_pk = self.initial_data.get('room')
            room = get_object_or_404(Rooms, pk=room_pk)
            value['room'] = room
        else:
            raise serializers.ValidationError('rooms 정보가 전달되지 않았습니다.')

        if value.get('guest_personnel') and room.rooms_personnel < value['guest_personnel']:
            raise serializers.ValidationError('숙박 허용인원을 초과했습니다.')
        print(value)
        return value

    def create(self, validated_data):
        reservation = super().create(validated_data)
        return reservation


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
    room_images = RoomImageSerializer(many=True)
    rooms_cover_image = serializers.ImageField()

    class Meta:
        model = Rooms
        fields = (
            'rooms_name',
            'rooms_tag',
            'rooms_host',
            'rooms_cover_image',
            'rooms_type',
            'room_images',
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
